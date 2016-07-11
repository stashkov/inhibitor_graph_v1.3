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
    # if not all([isinstance(i, list) for i in d.values()]):
    #     print 'Encountered an error.'
    #     print 'inside dict:', d
    #     print 'values %s are not instances of a list' % str(d.values())
    #     raise ValueError
    #all_nodes_values = set(itertools.chain.from_iterable(d.values()))
    #all_nodes_keys = set(d.keys())
    #return sorted(list(all_nodes_values | all_nodes_keys))
    return d.keys()


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
        # TODO have to bring in node:[values] to generate even more inc nodes!
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
    existing_nodes_list = flatten_dict_to_list(d)
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


def nodes_incompatible_with_dict_itself(d):
    """dict {'5T': '6F', '5F': '6T'} is incompatible with itself"""
    lst = flatten_dict_to_list(d)
    res = set()
    for n in lst:
        res.update(nodes_incompatible_with_dict(n, d))
    return list(res)


def is_connected(d):
    return set(d.keys()) == set(_plain_bfs(convert_directed_to_undirected(d), d.keys()[0]))


def convert_directed_to_undirected(d):
    undirected_d = copy.deepcopy(d)
    for key, value in d.iteritems():
        for i in value:
            undirected_d[i].append(key)
    return undirected_d


def number_of_nodes_in(d):
    l = [split_composite_node(i) for i in flatten_dict_to_list(d)]
    return len({i[:-1] for i in itertools.chain.from_iterable(l)})


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


