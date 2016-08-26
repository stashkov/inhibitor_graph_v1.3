import graph_op as op
import rule as r
from collections import defaultdict
import copy
import itertools
import logging
import time
from multiprocessing import Process, Manager, cpu_count, current_process
import example_graphs as ex
import db_functions as d

NUMBER_OF_ALLOWED_PROCESSES = cpu_count() - 1
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO, filename='hello.log')
logging.basicConfig(level=logging.INFO)


# create a file handler
# handler = logging.FileHandler('hello.log')
# handler.setLevel(logging.DEBUG)
#
# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
#
# # add the handlers to the logger
# logger.addHandler(handler)


def generate_graph(n_of_nodes):
    flag = False
    while not flag:
        m = op.generate_adj_matrix(n_of_nodes)
        g = op.to_dict(m)
        flag = op.is_connected(g)
    return g, m


def get_graph_stats(dict_graph, matrix_graph):
    in_degree = op.in_degree(matrix_graph)
    out_degree = op.out_degree(matrix_graph)
    inhibited_edges, inhibition_degree = op.inhibited_edges(matrix_graph)

    inhibited_vertices = set([edge[1] for edge in inhibited_edges])
    non_inhibited_vertices = list(set(dict_graph.keys()) - inhibited_vertices)

    global row_id
    d.insert_into_db(id=row_id, in_degree=in_degree,
                   out_degree=out_degree,
                   inhibited_edges=inhibited_edges,
                   inhibition_degree=inhibition_degree,
                   inhibited_vertices=inhibited_vertices,
                   non_inhibited_vertices=non_inhibited_vertices)

    logger.info('input graph --------------->%s' % dict_graph)
    logger.debug('in degree for each node --->%s' % in_degree)
    logger.debug('out degree for each node -->%s' % out_degree)
    logger.info('inhibited edges ----------->%s' % inhibited_edges)
    logger.debug('number of inhibited edges going into a node -->%s' % inhibition_degree)
    logger.debug('non inhibited vertices ---->%s' % non_inhibited_vertices)
    return in_degree, out_degree, inhibited_edges, inhibition_degree, inhibited_vertices, non_inhibited_vertices


def generate_bin_of_edges(g, m):
    in_degree, out_degree, \
        inhibited_edges, inhibition_degree, \
        inhibited_vertices, non_inhibited_vertices = get_graph_stats(g, m)

    bin_of_edges = defaultdict(set)
    for edge in inhibited_edges:
        u, v = edge
        if in_degree[v] == 1:  # CASE I
            bin_of_edges = r.exactly_one_one_inhibited(g, u, v, bin_of_edges)
        if in_degree[v] > 1 and inhibition_degree[v] == 1:  # CASE II
            bin_of_edges = r.more_than_one_one_inhibited(g, u, v, bin_of_edges)
        # if in_degree[v] > 1 and inhibition_degree[v] == 2:  # CASE II
        # TODO
        # if in_degree[v] > 1 and inhibition_degree[v] > 1 and \
        #    in_degree[v] != inhibition_degree[v]:  # CASE not yet exists :)
        # TODO every possible combination of AND OR over input set
        #     pass  # many AND OR cases
        if in_degree[v] == inhibition_degree[v] == 2:  # CASE III
            bin_of_edges = r.two_or_more_all_inhibited(g, v, bin_of_edges)

    for v in non_inhibited_vertices:
        if in_degree[v] > 1:  # CASE VI
            bin_of_edges = r.more_than_one_no_inhibited(g, v, bin_of_edges)
        if in_degree[v] == 1:  # CASE V
            bin_of_edges = r.exactly_one_no_inhibited(g, v, bin_of_edges)

    bin_of_edges = helper_deadend_nodes(bin_of_edges)

    # make a normal dict instead of default dict
    bin_of_edges = defaultdict(list, ((k, list(v)) for k, v in bin_of_edges.iteritems()))
    bin_of_edges = dict(bin_of_edges)
    return bin_of_edges


def helper_deadend_nodes(bin_of_edges):
    """given {1:[2]} make it {1:[2], 2:[]}"""
    for i in set(itertools.chain.from_iterable(bin_of_edges.values())):
        if i not in bin_of_edges.keys():
            bin_of_edges[i] = []
    return bin_of_edges


def add_to_not_feasible(d, not_feasible):
    # not_feasible.setdefault(len(d), []).append(d)
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
            time.sleep(.5)
    while any([j.is_alive() for j in jobs]):
        logger.debug([j for j in jobs if j.is_alive() == True])
        logger.info('Processes completed %s out of %s' % (len([j for j in jobs if j.is_alive() == False]), len(b.keys())))
        time.sleep(1)
    p.join()

    # logger.info('Processes completed %s out of %s' % (len([j for j in jobs if j.is_alive() == False]), len(b.keys())))
    # logger.info('We got infeasible dict %s' % not_feasible)
    logger.info('We got %s infeasible dicts' % len(not_feasible))
    logger.info('results are:\n%s' % result)
    logger.info('number of results: %s' % len(result))
    global row_id
    d.insert_into_db(row_id, not_feasible=not_feasible, results=result, number_of_results=len(result))
    return result


def set_up_random(num_of_nodes):
    dict_graph, matrix_graph = generate_graph(num_of_nodes)
    node_count = num_of_nodes
    b = generate_bin_of_edges(dict_graph, matrix_graph)
    b = op.convert_directed_to_undirected(b)  # DOMINATING!
    d.insert_into_db(id=row_id, input_graph=dict_graph, input_matrix=matrix_graph, bin_of_edges=b)
    return b, node_count


def set_up_preset(matrix_graph):
    global row_id
    node_count = len(matrix_graph)
    dict_graph = op.to_dict(matrix_graph)
    b = generate_bin_of_edges(dict_graph, matrix_graph)
    d.insert_into_db(id=row_id, input_graph=dict_graph, input_matrix=matrix_graph, bin_of_edges=b)
    #b = op.convert_directed_to_undirected(b)  # DOMINATING!
    return b, node_count


def get_known_incompatible(bin_of_edges):
    return {i: op.nodes_incompatible_with_dict(i, bin_of_edges) for i in bin_of_edges.keys()}

if __name__ == '__main__':
    #for i in range(100):
    # d.create_database()
    start = time.time()
    row_id = d.get_next_id_from_db()
    bin_of_edges, n_count = set_up_random(100)
    #bin_of_edges, n_count = set_up_preset(ex.graph_II)
    # logger.info('bin of nodes: %s' % bin_of_edges)
    # logger.info('We got %s nodes. Entire list is: %s' % (len(bin_of_edges.keys()), bin_of_edges.keys()))

    known_incompatible_nodes = get_known_incompatible(bin_of_edges)
    # logger.info('known incompatible nodes : %s' % known_incompatible_nodes)

    execute_algo(bin_of_edges, n_count)
    logger.info('Execution time: %s' % str(time.time() - start))
    d.insert_into_db(row_id, running_time=str(time.time() - start), known_incompatible_nodes=known_incompatible_nodes)
    # logger.info('cnt of inc nodes %s' % cnt_inc_nodes)
    # main()
