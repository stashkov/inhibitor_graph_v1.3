import graph_op as op
import rule as r
from collections import defaultdict
import copy
import itertools
import logging
import time
from multiprocessing import Process, Manager, cpu_count, current_process

NUMBER_OF_ALLOWED_PROCESSES = cpu_count() - 1
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG, filename='hello.log')
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


def generate_bin_of_edges(g, m):
    """given graph, its dict repr G and matrix repr m, generate bin of edges for it"""
    in_degree = op.in_degree(m)
    out_degree = op.out_degree(m)
    inhibited_edges, inhibition_degree = op.inhibited_edges(m)

    inhibited_vertices = set([edge[1] for edge in inhibited_edges])
    non_inhibited_vertices = list(set(g.keys()) - inhibited_vertices)

    logger.info('input graph --------------->%s' % g)
    logger.debug('in degree for each node --->%s' % in_degree)
    logger.debug('out degree for each node -->%s' % out_degree)
    logger.info('inhibited edges ----------->%s' % inhibited_edges)
    logger.debug('number of inhibited edges going into a node -->%s' % inhibition_degree)
    logger.debug('non inhibited vertices ---->%s' % non_inhibited_vertices)

    bin_of_edges = defaultdict(set)

    for edge in inhibited_edges:
        u, v = edge
        if in_degree[v] == 1:  # CASE I
            bin_of_edges = r.exactly_one_one_inhibited(g, u, v, bin_of_edges)
        if in_degree[v] > 1 and inhibition_degree[v] == 1:  # CASE II
            bin_of_edges = r.more_than_one_one_inhibited(g, u, v, bin_of_edges)
        # if in_degree[v] > 1 and inhibition_degree[v] == 2:  # CASE II
        #     # TODO
        # if in_degree[v] > 1 and inhibition_degree[v] > 1 and \
        #    in_degree[v] != inhibition_degree[v]:  # CASE not yet exists :)
        #     # TODO every possible combination of AND OR over input set
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


# def is_feasible(node_count, d):
#     return node_count < op.number_of_nodes_in(d)  # 6 < 7, we have 6 in original, and 7 in d, we still have a chance

def add_to_not_feasible(d, not_feasible):
    # not_feasible.setdefault(len(d), []).append(d)
    row = not_feasible[len(d)]
    row.append(d) # change it
    not_feasible[len(d)] = row  # copies the row back (otherwise parent process won't see the changes)
    return not_feasible


def recursive_teardown(node, d, node_count, result, not_feasible, pre_inc_nodes, recursion_level=0):
    global cnt_inc_nodes
    logger.debug('we got dict %s' % d)
    d = remove_incompatible_nodes(d, pre_inc_nodes[node])
    # length_d = len(d)
    # if length_d in not_feasible.keys() and d in not_feasible[length_d]:
    if d in not_feasible[len(d)]:
        logger.debug('this dict is incompatible because it was in inc list')
        return
    logger.debug('after removal we have %s' % d)
    if node_count > op.number_of_nodes_in(d):
        logger.debug('this dict is incompatible because original node count %i > current node count %i' % (node_count, op.number_of_nodes_in(d)))
        not_feasible = add_to_not_feasible(d, not_feasible)  # add to list of dict we know for sure to be not feasible
        return  # check if dict has the same number of nodes (even if they are now composite nodes)
    nodes_inside = op.nodes_incompatible_with_dict_itself(d)
    logger.debug('inc nodes_inside %s' % nodes_inside)
    if nodes_inside:  # check if d is incompatible with itself
        # if len(nodes_inside) > 100:
        #     cnt_inc_nodes.append(len(nodes_inside))
        #     logger.info('the number %s of inc nodes is too large %s' % (len(nodes_inside), nodes_inside))
        #     return
        for i in nodes_inside:
            logger.debug('inside recursive lvl %s, working with node %s' % (recursion_level, i))
            temp_dict = copy.deepcopy(d)
            recursive_teardown(i, temp_dict, node_count, result, not_feasible, pre_inc_nodes, recursion_level=recursion_level+1)
    else:
        if op.is_connected(d):
            logger.debug('HOORAY! WE GOT AN ANSWER \n %s' % d)
            if d not in result:
                result.append(d)
            logger.debug('--------------------')
            return d  # we got an answer!
        else:
            logger.debug('this dict is incompatible because it is not connected')
            not_feasible = add_to_not_feasible(d, not_feasible)  # add to list of dict we know for sure to be not feasible
            return  # if graph is disconnected, we don't want it
    #logger.debug('quitting the stack for node %s' % node)


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


def execute_algo(b, node_count):
    manager = Manager()
    result = manager.list()
    not_feasible = manager.list()
    for i in range(len(b)):
        not_feasible.append([])
    cnt_inc_nodes = manager.list()


    lst = [key for key, value in b.iteritems() if value != []]  # probably can remove leaf nodes?
    logger.info('Bin of edges:%s' % b)
    logger.info('We got %s nodes. Entire list is: %s' % (len(lst), lst))

    global pre_inc_nodes
    global cnt_inc_nodes
    # # sequential execution
    # for i in lst:
    #     temp_ = copy.deepcopy(b)
    #     logger.info('Next iteration. Working with node %s, which is #%s out of %s' % (i, lst.index(i)+1, len(lst)))
    #     recursive_teardown(i, temp_, node_count, result, not_feasible, pre_inc_nodes)

    jobs = []
    for i in lst:
        temp_ = copy.deepcopy(b)
        logger.info('Next iteration. Working with node %s, which is #%s out of %s' % (i, lst.index(i)+1, len(lst)))
        p = Process(target=recursive_teardown, args=(i, temp_, node_count, result, not_feasible, pre_inc_nodes))
        p.daemon = True  # make it a daemon so that sleep() in main does not affect other threads
        jobs.append(p)
        p.start()

        while len([1 for j in jobs if j.is_alive() == True]) >= NUMBER_OF_ALLOWED_PROCESSES:
            time.sleep(5)
    while any([j.is_alive() for j in jobs]):
        logger.debug([j for j in jobs if j.is_alive() == True])
        logger.info('Processes completed %s out of %s' % (len([j for j in jobs if j.is_alive() == False]), len(lst)))
        time.sleep(5)
    p.join()

    #logger.info('Processes completed %s out of %s' % (len([j for j in jobs if j.is_alive() == False]), len(lst)))
    logger.info('results are:\n%s' % result)
    logger.info('number of results: %s' % len(result))
    logger.info('We got infeasible dict %s' % not_feasible)
    logger.info('We got %s infeasible dicts' % len(not_feasible))


def set_up_random(num_of_nodes):
    g, m = generate_graph(num_of_nodes)
    node_count = num_of_nodes
    b = generate_bin_of_edges(g, m)
    b = op.convert_directed_to_undirected(b)
    return b, node_count


def set_up_preset():
    import example_graphs as ex
    m = ex.graph_II
    node_count = 3
    g = op.to_dict(m)
    b = generate_bin_of_edges(g, m)
    return b, node_count


def set_up_with_dict():
    # TODO preserve inhibited edges
    g = {'1': ['4', '5'], '3': ['6'], '2': ['3', '4', '6'], '5': ['6'], '4': ['5', '6'], '6': []}
    m = op.to_adj_matrix(g)
    node_count = 6
    b = generate_bin_of_edges(g, m)
    return b, node_count


if __name__ == '__main__':
    start = time.time();
    bin, n_count = set_up_random(100)
    #bin, n_count = set_up_preset()
    #bin, n_count = set_up_with_dict()
    logger.info('bin of nodes: %s' % bin)
    pre_inc_nodes = {i: op.nodes_incompatible_with_dict(i, bin) for i in bin.keys()}

    logger.info('dict of inc nodes: %s' % pre_inc_nodes)

    execute_algo(bin, n_count)
    logger.info('Execution time: %s' % str(time.time() - start))
    logger.info('cnt of inc nodes %s' % cnt_inc_nodes)



#main()