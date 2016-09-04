import networkx as nx
import numpy as np
import string
import matplotlib.pyplot as plt
import random


def draw_graph(adjacency_matrix, vertices=''):
    matrix = np.matrix(adjacency_matrix)
    graph = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph())
    # print matrix
    if vertices == '':
        # vertices = list(string.ascii_uppercase[0:len(adjacency_matrix)])
        vertices = range(len(adjacency_matrix))
    labels = {i: vertex for (i, vertex) in enumerate(vertices)}

    edge_color = ['b' if x == 1 else 'r' for row in adjacency_matrix for x in row if x in [-1, 1]]
    width = [1]
    node_color = ['w' for _ in edge_color]

    nx.draw(graph,
            layout=nx.spring_layout(graph),
            node_size=1000,
            labels=labels,
            with_labels=True,
            font_size=16,
            edge_color=edge_color,
            width=width,
            node_color=node_color)
    # plt.show()
    name = random.choice(range(100000))
    plt.savefig(str(name) + '.png')
    plt.clf()
    return

