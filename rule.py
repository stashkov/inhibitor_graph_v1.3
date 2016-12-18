def two_or_more_all_inhibited(graph_dict, v, bin_of_edges):
    for key, value in graph_dict.items():
        if v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + 'F'].add(v + 'T')  # CASE III.1
            bin_of_edges[key + 'T'].add(v + 'F')  # CASE III.4
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
    # bin_of_edges[u + 'F'].add(v + 'F')  # CASE II.4 Biologically this is nonsense
    for key, value in graph_dict.items():
        if key != u and v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + 'F'].add(v + 'T')  # CASE II.1
            # bin_of_edges[key + 'T'].add(v + 'F')  # CASE II.4 # biologically nonsense
    return bin_of_edges


def more_than_one_no_inhibited(graph_dict, v, bin_of_edges):
    for key, value in graph_dict.iteritems():
        if v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + 'T'].add(v + 'T')  # CASE VI.2
            bin_of_edges[key + 'F'].add(v + 'F')  # CASE VI.3 TODO add to latex
    return bin_of_edges


def exactly_one_no_inhibited(graph_dict, v, bin_of_edges):
    # CASE V
    for key, value in graph_dict.iteritems():
        if v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + 'T'].add(v + 'T')
            bin_of_edges[key + 'F'].add(v + 'F')
    return bin_of_edges

