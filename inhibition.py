import graph_op as op
import rule as r
from collections import defaultdict
import copy
import itertools

RESULT = []

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

    print 'input graph --------------->', g
    print 'in degree for each node --->', in_degree
    print 'out degree for each node -->', out_degree
    print 'inhibited edges ----------->', inhibited_edges
    print 'number of inhibited edges going into a node -->', inhibition_degree
    print 'non inhibited vertices ---->', non_inhibited_vertices

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

    #{'1':['2']} is not good enough, make it {'1':['2'], '2':[]}
    for i in list(itertools.chain.from_iterable(bin_of_edges.values())):
        if i not in bin_of_edges.keys():
            bin_of_edges[i] = set()

    # make a normal dict instead of default dict
    bin_of_edges = defaultdict(list, ((k, list(v)) for k, v in bin_of_edges.items()))
    bin_of_edges = dict(bin_of_edges)
    return bin_of_edges


def recursive_teardown(node, d, node_count):
    inc_n = op.nodes_incompatible_with_dict(node, d)
    print 'incompatible nodes are', inc_n
    if inc_n:
        d = remove_incompatible_nodes(d, inc_n)
    print 'after removal we have', d
    if node_count > op.number_of_nodes_in(d):
        print 'this dict is incompatible because original node count %i > current node count %i' % (node_count, op.number_of_nodes_in(d))
        return  # check if dict has the same number of nodes (even if they are now composite nodes)
    nodes_inside = op.nodes_incompatible_with_dict_itself(d)
    print 'inc nodes_inside', nodes_inside
    if nodes_inside:  # check if d is compatible with itself
        for i in nodes_inside:
            print 'inside recursive, working with node', i
            temp_dict = copy.deepcopy(d)
            recursive_teardown(i, temp_dict, node_count)
    else:
        if op.is_connected(d):
            print '\nHOORAY! WE GOT AN ANSWER'
            print d
            global RESULT
            if d not in RESULT:
                RESULT.append(d)
            print '--------------------'
            return d  # we got an answer!
        else:
            print 'this dict is incompatible because it is not connected'
            return  # if graph is disconnected, we don't want it


def remove_incompatible_nodes(d, incompatible_nodes):
    for i in incompatible_nodes:
        if i in d.keys():
            del d[i]
        for k, v in d.items():
            if i in v:
                d[k].remove(i)
    return d


#NUMBER_OF_NODES = 5
# g, m = generate_graph(5)
import example_graphs as ex
m = ex.graph_I
g = op.to_dict(m)
node_count = 3
b = generate_bin_of_edges(g, m)

print 'bin', b
for i in op.flatten_dict_to_list(b):
    print '\nnext iteration\n'
    print 'working with node', i
    a = recursive_teardown(i, b, node_count)

print '\nresults are:'
print RESULT
