import re
import random as rnd
import copy


def generate_adj_matrix(vertices, inhibition_degree=2):
    """generate square matrix with max inihigibiton degree
    currently several restrictions are in place, they need to be lifted later"""
    value_pool = [-1, 1, 0] + [0]*10 + [1]*2
    matrix = [[0 for _ in xrange(vertices)] for _ in xrange(vertices)]
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            if i > j:
                if row.count(-1) + row.count(1) >= 2 and row.count(-1) != 0:
                    matrix[i][j] = 0
                elif row.count(-1) == 1:
                    matrix[i][j] = rnd.choice(value_pool)
                elif row.count(-1) == 2:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = rnd.choice(value_pool)
    matrix = [list(i) for i in zip(*matrix)]
    return matrix


def swap_true_false(nodes):
    if isinstance(nodes, list):
        return [n.replace('F', 'Z').replace('T', 'F').replace('Z', 'T') for n in nodes]
    if isinstance(nodes, str):
        return [nodes.replace('F', 'Z').replace('T', 'F').replace('Z', 'T')]


def nodes_incompatible_with_dict(node, d):
    inc_nodes_list = list(set(swap_true_false(node) + swap_true_false(d[node])))
    return [i for i in inc_nodes_list if i in d.keys()]


def nodes_incompatible_within_dict(d):
    """dict {'5T': '6F', '5F': '6T'} is incompatible with itself"""
    res = set()
    for n in d.keys():
        res.update(nodes_incompatible_with_dict(n, d))
    return list(res)


def convert_undirected_to_directed(graph, helper):
    for k, v in helper.iteritems():
        if not v:
            if k + 'T' in graph.keys():
                graph[k + 'T'] = []
            else:
                graph[k + 'F'] = []
    return graph


def number_of_nodes(d):
    return len({i[:-1] for i in d.keys()})


def is_connected(d):
    return set(d.keys()) == set(_plain_bfs(convert_directed_to_undirected(d), d.keys()[0]))


def _plain_bfs(graph, source):
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                yield v
                seen.add(v)
                nextlevel.update(graph[v])


def convert_directed_to_undirected(dict_graph):
    undirected_d = copy.deepcopy(dict_graph)
    for key, value in dict_graph.iteritems():
        for i in value:
            undirected_d[i].append(key)
    return undirected_d