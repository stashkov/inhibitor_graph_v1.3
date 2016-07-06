import graph_op as op
import rule as r
from collections import defaultdict


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

    # make a normal dict instead of default dict
    bin_of_edges = defaultdict(list, ((k, list(v)) for k, v in bin_of_edges.items()))
    bin_of_edges = dict(bin_of_edges)
    return bin_of_edges

