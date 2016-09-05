import graph_op as op
from collections import defaultdict
import copy
import itertools
import logging
import time
from multiprocessing import Process, Manager, cpu_count
import example_graphs as ex
import db_functions as d
import draw_graph as dg
import one_time_draw_graph as one_time
import graph as g
import bin_of_edges as b



NUMBER_OF_ALLOWED_PROCESSES = cpu_count() - 1
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO, filename='hello.log')
logging.basicConfig(level=logging.INFO)


def add_to_not_feasible(d, not_feasible):
    row = not_feasible[len(d)]
    row.append(d)  # change it
    not_feasible[len(d)] = row  # copies the row back (otherwise parent process won't see the changes)
    return not_feasible


def recursive_teardown(node, dict_graph, node_count, result, not_feasible, known_incompatible, recursion_level=0):
    logger.debug('we got dict %s' % dict_graph)
    dict_graph = remove_incompatible_nodes(dict_graph, known_incompatible[node])
    logger.debug('after removal we have %s' % dict_graph)
    if dict_graph in not_feasible[len(dict_graph)]:
        logger.debug('this dict is incompatible because it was in inc list')
        return
    if node_count > op.get_number_of_nodes(dict_graph):
        logger.debug('this dict is incompatible because original node count %i > current node count %i' % (
            node_count, op.get_number_of_nodes(dict_graph)))
        not_feasible = add_to_not_feasible(dict_graph, not_feasible)  # add to list of dict we know for sure to be not feasible
        return
    nodes_inside = op.get_nodes_incompatible_inside_dict(dict_graph)
    logger.debug('incompatible nodes inside dict: %s' % nodes_inside)
    if nodes_inside:  # check if d is incompatible with itself
        for i in nodes_inside:
            logger.debug('inside recursive lvl %s, working with node %s' % (recursion_level, i))
            temp_dict = copy.deepcopy(dict_graph)
            recursive_teardown(i, temp_dict, node_count, result, not_feasible, known_incompatible,
                               recursion_level=recursion_level + 1)
    else:
        if op.is_connected(dict_graph):
            logger.debug('HOORAY! WE GOT AN ANSWER \n %s' % dict_graph)
            if dict_graph not in result:
                result.append(dict_graph)
            logger.debug('--------------------')
            return dict_graph  # we got an answer!
        else:
            logger.debug('this dict is incompatible because it is not connected')
            not_feasible = add_to_not_feasible(dict_graph,
                                               not_feasible)  # add to list of dict we know for sure to be not feasible
            return  # if graph is disconnected, we don't want it
            # logger.debug('quitting the stack for node %s' % node)


def remove_incompatible_nodes(d, incompatible_nodes):
    mark_for_deletion = []
    for i in incompatible_nodes:
        if i in d.keys():
            del d[i]
        for k, v in d.iteritems():
            if i in v:
                d[k].remove(i)
            # if we have a node {n:[]} that means
            # it has out_degree=0 which means it must have in_degree at least 1
            # otherwise it is an isolated node and can be removed
            if d[k] == [] and k not in itertools.chain.from_iterable(d.values()):
                mark_for_deletion.append(k)
    for i in mark_for_deletion:
        if i in d.keys():
            del d[i]
    return d

# def process_sequentially(bin_of_edges, ):
#     for i in b.keys():
#         temp_ = copy.deepcopy(b)
#         logger.info('Next iteration. Working with node %s, which is #%s out of %s' % (i, lst.index(i)+1, len(lst)))
#         recursive_teardown(i, temp_, node_count, result, not_feasible, known_incompatible_nodes)


def execute_algo(b, node_count):
    result = Manager().list()
    not_feasible = Manager().list()
    for i in range(len(b)):  # empty list of lists to hold corresponding length incompatible dictionaries
        not_feasible.append([])

    global known_incompatible_nodes
    # # parallel execution
    jobs = []
    for i in b.keys():
        temp_ = copy.deepcopy(b)
        logger.info('Next iteration. Working with node %s, which is #%s out of %s' % (i, b.keys().index(i) + 1, len(b.keys())))
        p = Process(target=recursive_teardown, args=(i, temp_, node_count, result, not_feasible, known_incompatible_nodes))
        p.daemon = True  # make it a daemon so that sleep() in main does not affect other threads
        jobs.append(p)
        p.start()

        while len([1 for j in jobs if j.is_alive() == True]) >= NUMBER_OF_ALLOWED_PROCESSES:
            time.sleep(1)
    while any([j.is_alive() for j in jobs]):
        logger.debug([j for j in jobs if j.is_alive() == True])
        logger.info('Processes completed %s out of %s' % (len([j for j in jobs if j.is_alive() == False]), len(b.keys())))
        time.sleep(2)
    p.join()

    logger.info('We got %s infeasible dicts' % len(not_feasible))
    logger.info('results are:\n%s' % result)
    logger.info('number of results: %s' % len(result))
    global row_id
    d.insert_into_db(row_id,
                     number_of_not_feasible=len(not_feasible),
                     results=result, number_of_results=len(result))
    return result


def get_known_incompatible(bin_of_edges):
    return {i: op.nodes_incompatible_with_dict(i, bin_of_edges) for i in bin_of_edges.keys()}


def generate_connected_graph(number_of_nodes):
    flag = False
    while not flag:
        matrix = op.generate_adj_matrix(number_of_nodes)
        gg = g.Graph(matrix)
        flag = gg.connected
    return gg


if __name__ == '__main__':
    d.if_not_exists_create_database()
    row_id = d.get_max_id_from_db() + 1
    start = time.time()

    number_of_nodes = 7
    graph_instance = generate_connected_graph(number_of_nodes)
    # graph_instance = g.Graph(ex.graph_II)
    bin_of_edges = b.generate_bin_of_edges(graph_instance)
    known_incompatible_nodes = get_known_incompatible(bin_of_edges)
    result = execute_algo(bin_of_edges, number_of_nodes)

    duration = str(time.time() - start)
    logger.info('Execution time: %s' % duration)

    d.insert_into_db(row_id=row_id,
                     bin_of_edges=bin_of_edges,

                     number_of_nodes=number_of_nodes,
                     running_time=duration,
                     known_incompatible_nodes=known_incompatible_nodes,

                     input_graph=graph_instance.dict_graph,
                     input_matrix=graph_instance.matrix_graph,
                     in_degree=graph_instance.in_degree,
                     out_degree=graph_instance.out_degree,
                     inhibited_edges=graph_instance.inhibited_edges,
                     inhibition_degree=graph_instance.inhibition_degree,
                     inhibited_vertices=graph_instance.inhibited_vertices,
                     non_inhibited_vertices=graph_instance.non_inhibited_vertices)

    one_time.draw_graph_for_every_input_matrix(row_id)
    one_time.draw_graph_for_every_non_empty_result(row_id)

