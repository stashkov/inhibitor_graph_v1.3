import copy


class Graph(object):
    def __init__(self, matrix_graph):
        self.matrix_graph = matrix_graph
        self.dict_graph = self.to_dict(self.matrix_graph)
        self.in_degree = self.get_in_degree(self.matrix_graph)
        self.out_degree = self.get_out_degree(self.matrix_graph)
        self.vertices = Graph.get_vertices(self.matrix_graph)
        self.inhibited_edges = Graph.get_inhibited_edges(self.matrix_graph)
        self.inhibition_degree = Graph.get_inhibited_degree(self.matrix_graph)
        self.connected = Graph.is_connected(self.dict_graph)
        self.inhibited_vertices = set([edge[1] for edge in self.inhibited_edges])
        self.non_inhibited_vertices = list(set(self.dict_graph.keys()) - self.inhibited_vertices)

    @staticmethod
    def to_dict(matrix_graph):
        """convert graph from adj matrix to dict"""
        vertices = Graph.get_vertices(matrix_graph)
        graph_dict = {i: [] for i in vertices}
        for i in xrange(len(matrix_graph)):
            for j in xrange(len(matrix_graph)):
                if abs(matrix_graph[i][j]) == 1:
                    graph_dict[vertices[i]].append(vertices[j])
        return graph_dict

    @staticmethod
    def get_in_degree(matrix_graph):
        vertices = Graph.get_vertices(matrix_graph)
        dict_in_degree = {i: 0 for i in vertices}
        adjacency_matrix_transpose = [list(i) for i in zip(*matrix_graph)]
        for i, row in enumerate(adjacency_matrix_transpose):
            for value in row:
                if abs(value) == 1:
                    dict_in_degree[vertices[i]] += 1
        return dict_in_degree

    @staticmethod
    def get_out_degree(matrix_graph):
        vertices = Graph.get_vertices(matrix_graph)
        dict_out_degree = {i: 0 for i in vertices}
        for i, row in enumerate(matrix_graph):
            for value in row:
                if abs(value) == 1:
                    dict_out_degree[vertices[i]] += 1
        return dict_out_degree

    @staticmethod
    def get_vertices(matrix_graph):
        return [str(i) for i in xrange(1, len(matrix_graph) + 1)]

    @staticmethod
    def get_inhibited_edges(matrix_graph):
        vertices = Graph.get_vertices(matrix_graph)
        inh_edges = []
        for i in range(len(matrix_graph)):
            for j in range(len(matrix_graph)):
                if matrix_graph[i][j] == -1:
                    inh_edges.append((vertices[i], vertices[j]))
        return inh_edges

    @staticmethod
    def get_inhibited_degree(matrix_graph):
        vertices = Graph.get_vertices(matrix_graph)
        inh_degree_dict = dict()
        for i in range(len(matrix_graph)):
            for j in range(len(matrix_graph)):
                if matrix_graph[i][j] == -1:
                    inh_degree_dict[vertices[j]] = inh_degree_dict.get(vertices[j], 0) + 1
        return inh_degree_dict

    @staticmethod
    def to_adj_matrix(dict_graph):
        all_nodes = sorted(dict_graph.keys())
        matrix_graph = []
        for v in all_nodes:
            if v in dict_graph.keys():
                matrix_graph.append([1 if e in dict_graph[v] else 0 for e in all_nodes])
        return matrix_graph

    @staticmethod
    def is_connected(d):
        return set(d.keys()) == set(Graph._plain_bfs(Graph.convert_directed_to_undirected(d), d.keys()[0]))

    @staticmethod
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

    @staticmethod
    def convert_directed_to_undirected(dict_graph):
        undirected_d = copy.deepcopy(dict_graph)
        for key, value in dict_graph.iteritems():
            for i in value:
                undirected_d[i].append(key)
        return undirected_d
