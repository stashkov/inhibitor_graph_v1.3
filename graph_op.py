import re
import itertools
import copy


def out_degree(adj_matrix):
    vertices = range(1, len(adj_matrix) + 1)
    vertices = [str(i) for i in vertices]
    dict_out_degree = {i: 0 for i in vertices}
    row_number = 0
    for row in adj_matrix:
        for value in row:
            if abs(value) == 1:
                dict_out_degree[vertices[row_number]] += 1
        row_number += 1
    return dict_out_degree


def in_degree(adj_matrix):
    vertices = range(1, len(adj_matrix) + 1)
    vertices = [str(i) for i in vertices]
    dict_in_degree = {i: 0 for i in vertices}
    adjacency_matrix_transpose = [list(i) for i in zip(*adj_matrix)]
    row_number = 0
    for row in adjacency_matrix_transpose:
        for value in row:
            if abs(value) == 1:
                dict_in_degree[vertices[row_number]] += 1
        row_number += 1
    return dict_in_degree


def inhibited_edges(adj_matrix):
    """get list of inhibited edges [(A,B), (C,D)]
    and dict of inhibited degrees {B:1, D:1}"""
    vertices = range(1, len(adj_matrix) + 1)
    vertices = [str(i) for i in vertices]
    inh_edges = []
    inh_degree_dict = {}
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if adj_matrix[i][j] == -1:
                inh_edges.append((vertices[i], vertices[j]))
                inh_degree_dict[vertices[j]] = inh_degree_dict.get(vertices[j], 0) + 1
    return inh_edges, inh_degree_dict


def generate_adj_matrix(vertices, inhibition_degree=2):
    """generate square matrix with max inihigibiton degree
    currently several restrictions are in place, they need to be lifted later"""
    import random as rnd
    matrix = [[0 for x in range(vertices)] for y in range(vertices)]
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            if i > j:
                if row.count(-1) + row.count(1) >= 2 and row.count(-1) != 0:
                    matrix[i][j] = 0
                elif row.count(-1) == 1:
                    matrix[i][j] = rnd.choice([-1, 1, 0])
                elif row.count(-1) == 2:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = rnd.choice([-1, 1, 0])
    matrix = [list(i) for i in zip(*matrix)]
    return matrix


def to_dict(adj_matrix):
    """convert graph from adj matrix to dict"""
    vertices = range(1, len(adj_matrix) + 1)
    vertices = [str(i) for i in vertices]
    graph_dict = {i: [] for i in vertices}
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if abs(adj_matrix[i][j]) == 1:
                graph_dict[vertices[i]].append(vertices[j])
    return graph_dict


def to_adj_matrix(d):
    """convert graph from dict to adj matrix"""
    all_nodes = flatten_dict_to_list(d)
    m = []
    for v in all_nodes:
        if v in d.keys():
            m.append([1 if e in d[v] else 0 for e in all_nodes])
        else:
            m.append([0] * len(all_nodes))
    return m


def flatten_dict_to_list(d):
    """return sorted list of unique nodes"""
    # TODO write test this
    if not all([isinstance(i, list) for i in d.values()]):
        print 'Encountered an error.'
        print 'inside dict:', d
        print 'values %s are not instances of a list' % str(d.values())
        raise ValueError
    all_nodes_values = set(itertools.chain.from_iterable(d.values()))
    all_nodes_keys = set(d.keys())
    return sorted(list(all_nodes_values | all_nodes_keys))


def swap_true_and_false(nodes):
    if isinstance(nodes, list):
        return [n.replace('F', 'Z').replace('T', 'F').replace('Z', 'T') for n in nodes]
    if isinstance(nodes, str):
        return nodes.replace('F', 'Z').replace('T', 'F').replace('Z', 'T')


def split_composite_node(s):
    """given string 1T2F returns list ['1F', '2F']"""
    return re.findall(r'\d+[TF]', s)


def is_compatible(d):
    # '123F12T': ['1T', '12T'] is incompatible, because '12T' in '123F12T'
    # '123F12T': ['1T', '12F'] is incompatible, because '12F' is a negation of '123F12T'
    pass


def is_simple_node(node):
    if node.count('F') + node.count('T') == 1:
        return True
    else:
        return False


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
    inc_nodes_list = incompatible_nodes(node)  # generate incompatible nodes
    existing_nodes_list = flatten_dict_to_list(d)
    for i in inc_nodes_list:
        for e in existing_nodes_list:
            if is_simple_node(i) and is_simple_node(e):
                if i == e:
                    res.add(e)
            elif is_simple_node(i) and not is_simple_node(e):
                for e1 in split_composite_node(e):
                    if i[:-1] == e1[:-1] and node != e:
                        res.add(e)
            elif not is_simple_node(i) and is_simple_node(e):
                for i1 in split_composite_node(i):
                    if i1[:-1] == e[:-1]:
                        res.add(e)
            else:  # both are not simple
                for i1 in split_composite_node(i):
                    for e1 in split_composite_node(e):
                        if i1 == e1 and node != e:
                            res.add(e)
    return list(res)


def nodes_incompatible_with_dict_itself(d):
    """dict {'5T': '6F', '5F': '6T'} is incompatible with itself"""
    lst = flatten_dict_to_list(d)
    res = set()
    for n in lst:
        res.update(nodes_incompatible_with_dict(n, d))
    return list(res)


def is_compatible_dict(d):
    return not bool(nodes_incompatible_with_dict_itself(d))


def is_connected(d):
    """check whether graph is connected"""
    # TODO test cases
    seen = set()
    nodes = flatten_dict_to_list(d)
    for n in nodes:
        seen.add(_plain_bfs(d, n))
    if len(seen) == len(nodes):
        return True
    else:
        return False


def number_of_nodes_in(d):
    """if #nodes in source dict != #nodes in results dict, we can disregard it"""
    l = [split_composite_node(i) for i in flatten_dict_to_list(d)]
    return len(list(itertools.chain.from_iterable(l)))


def _plain_bfs(G, source):
    """A fast BFS node generator"""
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                yield v
                seen.add(v)
                nextlevel.update(G[v])


def recursive_teardown(node, d):
    node_count = number_of_nodes_in(d)  # given a node, remove incompatible nodes from dict
    inc_n = nodes_incompatible_with_dict(node, d)
    # TODO del inc_n from d
    print d
    print inc_n
    if node_count != number_of_nodes_in(d):
        return  # check if dict has the same number of nodes (even if they are now composite nodes)
    if not is_connected(d):
        return  # if graph is disconnected, we don't want it
    nodes_inside = nodes_incompatible_with_dict_itself(d)
    if nodes_inside:  # check if d is compatible with itself
        for i in nodes_inside:
            temp_dict = copy.deepcopy(d)
            recursive_teardown(i, temp_dict)
    else:
        return d  # we got an answer!
