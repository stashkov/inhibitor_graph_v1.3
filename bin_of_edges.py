from collections import defaultdict
import itertools
import rule as r


def generate_bin_of_edges(gg):
    bin_of_edges = defaultdict(set)
    for edge in gg.inhibited_edges:
        u, v = edge
        if gg.in_degree[v] == 1:  # CASE I
            bin_of_edges = r.exactly_one_one_inhibited(gg.dict_graph, u, v, bin_of_edges)
        if gg.in_degree[v] > 1 and gg.inhibition_degree[v] == 1:  # CASE II
            bin_of_edges = r.more_than_one_one_inhibited(gg.dict_graph, u, v, bin_of_edges)
        # if in_degree[v] > 1 and inhibition_degree[v] == 2:  # CASE II
        # TODO
        # if in_degree[v] > 1 and inhibition_degree[v] > 1 and \
        #    in_degree[v] != inhibition_degree[v]:  # CASE not yet exists :)
        # TODO every possible combination of AND OR over input set
        #     pass  # many AND OR cases
        if gg.in_degree[v] == gg.inhibition_degree[v] == 2:  # CASE III
            bin_of_edges = r.two_or_more_all_inhibited(gg.dict_graph, v, bin_of_edges)

    bin_of_edges = process_non_inhibited_vertices(gg, bin_of_edges)
    bin_of_edges = process_zero_out_degree_nodes(bin_of_edges)
    bin_of_edges = convert_to_regular_dict(bin_of_edges)

    return bin_of_edges


def convert_to_regular_dict(dct):
    dct = defaultdict(list, ((k, list(v)) for k, v in dct.iteritems()))
    return dict(dct)


def process_non_inhibited_vertices(gg, bin_of_edges):
    for v in gg.non_inhibited_vertices:
        if gg.in_degree[v] > 1:  # CASE VI
            bin_of_edges = r.more_than_one_no_inhibited(gg.dict_graph, v, bin_of_edges)
        if gg.in_degree[v] == 1:  # CASE V
            bin_of_edges = r.exactly_one_no_inhibited(gg.dict_graph, v, bin_of_edges)
    return bin_of_edges


def process_zero_out_degree_nodes(dct):
    """given {1:[2]} make it {1:[2], 2:[]}"""
    for i in set(itertools.chain.from_iterable(dct.values())):
        if i not in dct.keys():
            dct[i] = []
    return dct
