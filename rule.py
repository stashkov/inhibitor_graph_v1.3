def two_or_more_all_inhibited(graph_dict, v, bin_of_edges):
    new_node = new_node_ = ''  # CASE III.2 and CASE III.3
    for key, value in graph_dict.items():
        if v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + 'F'].add(v + 'T')  # CASE III.1
            bin_of_edges[key + 'T'].add(v + 'F')  # CASE III.4
            new_node += key + 'F'  # CASE III.2
            new_node_ += key + 'T'  # CASE III.3
    bin_of_edges[new_node].add(v + 'T')  # CASE III.2
    bin_of_edges[new_node_].add(v + 'F')  # CASE III.3
    return bin_of_edges


def exactly_one_one_inhibited(graph_dict, u, v, bin_of_edges):
    bin_of_edges[u + 'F'].add(v + 'T')  # CASE I.1
    bin_of_edges[u + 'T'].add(v + 'F')  # CASE I.2
    for vertex in graph_dict[v]:
        bin_of_edges[v + 'T'].add(vertex + 'T')  # CASE I.1
        # TODO: in case A-|B-|C we get 'B0':['C1','C0']
        #bin_of_edges[v + 'T'].add(vertex + 'T')  # CASE I.2
    return bin_of_edges


def more_than_one_one_inhibited(graph_dict, u, v, bin_of_edges):
    bin_of_edges[u + 'T'].add(v + 'T')  # CASE II.1
    bin_of_edges[u + 'F'].add(v + 'F')  # CASE II.4
    new_node = new_node_ = ''  # CASE II.2 and CASE II.3
    for key, value in graph_dict.items():
        if v in value:  # find nodes, other than u, going to v
            if key != u:
                bin_of_edges[key + 'F'].add(v + 'T')  # CASE II.1
                bin_of_edges[key + 'T'].add(v + 'F')  # CASE II.4
                new_node += key + 'F'  # CASE II.2
                new_node_ += key + 'T'  # CASE II.3
    bin_of_edges[new_node + u + 'T'].add(v + 'T')  # CASE II.2
    bin_of_edges[new_node_ + u + 'F'].add(v + 'F')  # CASE II.3
    return bin_of_edges


def more_than_one_no_inhibited(graph_dict, v, bin_of_edges):
    new_node = ''  # CASE VI.1
    for key, value in graph_dict.iteritems():
        if v in value:  # find nodes, other than u, going to v
            new_node += key + 'T'  # CASE VI.1
            bin_of_edges[key + 'T'].add(v + 'T')  # CASE VI.2
            bin_of_edges[key + 'F'].add(v + 'F')  # CASE VI.3 TODO add to latex
    bin_of_edges[new_node].add(v + 'T')  # CASE VI.1
    return bin_of_edges


def exactly_one_no_inhibited(graph_dict, v, bin_of_edges):
    # CASE V
    for key, value in graph_dict.iteritems():
        if v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + 'T'].add(v + 'T')
            bin_of_edges[key + 'F'].add(v + 'F')
    return bin_of_edges

