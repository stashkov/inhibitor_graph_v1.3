import networkx as nx
import numpy as np
import string
import matplotlib.pyplot as plt
import random
import os


def draw_graph(adjacency_matrix, vertices='', name='img_1'):
    matrix = np.matrix(adjacency_matrix)
    graph = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph())
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
    plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images/') + str(name) + '.png')
    plt.clf()
    return

