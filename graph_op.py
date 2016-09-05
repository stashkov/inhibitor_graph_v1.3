import re
import itertools
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


def swap_true_and_false(nodes):
    if isinstance(nodes, list):
        return [n.replace('F', 'Z').replace('T', 'F').replace('Z', 'T') for n in nodes]
    if isinstance(nodes, str):
        return nodes.replace('F', 'Z').replace('T', 'F').replace('Z', 'T')


def split_composite_node(s):
    """given string 1T2F returns list ['1F', '2F']"""
    return re.findall(r'\d+[TF]', s)


def is_simple_node(node):
    counter = 0
    for i in node:
        if i in 'TF':
            counter += 1
            if counter > 1:
                return False
    return True


def incompatible_nodes(node):
    """given a node generate all incompatible with it nodes"""
    if is_simple_node(node):
        return [swap_true_and_false(node)]
    else:  # given '5T88F' return ['5F88T', '5T', '88F', '5F', '88T']
        node_list = [swap_true_and_false(node)]
        node_list.extend(split_composite_node(node))
        node_list.extend(split_composite_node(swap_true_and_false(node)))
        return node_list


def nodes_incompatible_with_dict(node, d):
    """
    given dict d and a node, generate all incompatible, with that node, nodes
    for a node '123F' incompatible nodes are '123T', '123F5T', '123T7T'
    for a node '1F2T' incompatible nodes are '1F', '2T', '1T2F', '1F2T99F', '1T2T'
    summary: given a node, incompatible nodes are those
    that contain, consists of, or negations of that node
    """

    res = set()
    inc_nodes_list = list(set(incompatible_nodes(node) + swap_true_and_false(d[node])))  # generate incompatible nodes
    existing_nodes_list = d.keys()
    for i in inc_nodes_list:
        i_flag = is_simple_node(i)
        for e in existing_nodes_list:
            e_flag = is_simple_node(e)
            if i_flag and e_flag:
                if i == e:
                    res.add(e)
            elif i_flag and not e_flag:
                for e1 in split_composite_node(e):
                    if i[:-1] == e1[:-1] and node != e:
                        res.add(e)
            elif not i_flag and e_flag:
                for i1 in split_composite_node(i):
                    if i1[:-1] == e[:-1]:
                        res.add(e)
            else:  # both are not simple
                for i1 in split_composite_node(i):
                    for e1 in split_composite_node(e):
                        if i1 == e1 and node != e:
                            res.add(e)
    return list(res)


def get_nodes_incompatible_inside_dict(d):
    """dict {'5T': '6F', '5F': '6T'} is incompatible with itself"""
    lst = d.keys()
    res = set()
    for n in lst:
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


def get_number_of_nodes(d):
    l = [split_composite_node(i) for i in d.keys()]
    return len({i[:-1] for i in itertools.chain.from_iterable(l)})


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