import graph_op as op
import rule as r
from collections import defaultdict
import copy
import itertools
import logging
import time
from multiprocessing import Process, Manager


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# create a file handler
#handler = logging.FileHandler('hello.log')
#handler.setLevel(logging.INFO)

# create a logging format
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#handler.setFormatter(formatter)

# add the handlers to the logger
#logger.addHandler(handler)


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

    # make a normal dict instead of default dict
    bin_of_edges = defaultdict(list, ((k, list(v)) for k, v in bin_of_edges.iteritems()))
    bin_of_edges = dict(bin_of_edges)
    return bin_of_edges


def recursive_teardown(node, d, node_count, result, recursion_level=0):
    #logger.info('if you see this it means I am not blocked by sleep')
    inc_n = op.nodes_incompatible_with_dict(node, d)
    logger.debug('Leonardo is currently %s levels deep' % recursion_level)
    logger.debug('given node %s incompatible nodes are %s' % (node, inc_n))
    if inc_n:
        d = remove_incompatible_nodes(d, inc_n)
    logger.debug('after removal we have %s' % d)
    if node_count > op.number_of_nodes_in(d):
        logger.debug('this dict is incompatible because original node count %i > current node count %i' % (node_count, op.number_of_nodes_in(d)))
        return  # check if dict has the same number of nodes (even if they are now composite nodes)
    nodes_inside = op.nodes_incompatible_with_dict_itself(d)
    logger.debug('inc nodes_inside %s' % nodes_inside)
    if nodes_inside:  # check if d is compatible with itself
        for i in nodes_inside:
            logger.debug('inside recursive, working with node %s' % i)
            temp_dict = copy.deepcopy(d)
            recursive_teardown(i, temp_dict, node_count, result, recursion_level=recursion_level+1)
    else:
        if op.is_connected(d):
            logger.debug('HOORAY! WE GOT AN ANSWER \n %s' % d)
            if d not in result:
                result.append(d)
            logger.debug('--------------------')
            return d  # we got an answer!
        else:
            logger.debug('this dict is incompatible because it is not connected')
            return  # if graph is disconnected, we don't want it
    logger.debug('quitting the stack for node %s' % node)


def remove_incompatible_nodes(d, incompatible_nodes):
    for i in incompatible_nodes:
        if i in d.keys():
            del d[i]
        for k, v in d.iteritems():
            if i in v:
                d[k].remove(i)
    return d


def execute_algo(b, node_count):
    manager = Manager()
    result = manager.list()

    lst = op.flatten_dict_to_list(b)
    logger.info('Bin of edges:%s' % b)
    logger.info('We got %s nodes. Entire list is: %s' % (len(lst), lst))

    # # sequential execution
    for i in lst:
        temp_ = copy.deepcopy(b)
        logger.info('Next iteration. Working with node %s, which is #%s out of %s' % (i, lst.index(i)+1, len(lst)))
        recursive_teardown(i, temp_, node_count, result)

    # jobs = []
    # for i in lst:
    #     temp_ = copy.deepcopy(b)
    #     logger.info('Next iteration. Working with node %s, which is #%s out of %s' % (i, lst.index(i)+1, len(lst)))
    #     p = Process(target=recursive_teardown, args=(i, temp_, node_count, result))
    #     p.daemon = True  # make it a daemon so that sleep() in main does not affect other threads
    #     jobs.append(p)
    #     p.start()
    # while any([j.is_alive() for j in jobs]):
    #     logger.debug([j for j in jobs if j.is_alive() == True])
    #     logger.info('Processes completed %s out of %s' % (len([j for j in jobs if j.is_alive() == False]), len(lst)))
    #     time.sleep(5)
    # p.join()

    #logger.info('Processes completed %s out of %s' % (len([j for j in jobs if j.is_alive() == False]), len(lst)))
    logger.info('results are:\n%s' % result)
    logger.info('number of results: %s' % len(result))


def set_up_random(num_of_nodes):
    g, m = generate_graph(num_of_nodes)
    node_count = num_of_nodes
    b = generate_bin_of_edges(g, m)
    return b, node_count


def set_up_preset():
    import example_graphs as ex
    m = ex.graph_II
    node_count = 3
    g = op.to_dict(m)
    b = generate_bin_of_edges(g, m)
    return b, node_count


def set_up_with_dict():
    g = {'1': ['3', '5', '7'], '3': ['4', '6', '7'], '2': ['3', '4', '6'], '5': [], '4': ['5'], '7': [], '6': []}  #INFO:__main__:Execution time: 169, 166
    m = op.to_adj_matrix(g)
    node_count = 7
    b = generate_bin_of_edges(g, m)
    return b, node_count


if __name__ == '__main__':
    start = time.time();
    #bin, n_count = set_up_random(7)
    #bin, n_count = set_up_preset()
    bin, n_count = set_up_with_dict()
    execute_algo(bin, n_count)
    logger.info('Execution time: %s' % str(time.time() - start))


#main()
