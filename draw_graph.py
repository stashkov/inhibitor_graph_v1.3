import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
import db_functions as df
import numpy
import draw_graph as dg
import graph_op as op
import graph as g


def draw_graph(adjacency_matrix, vertices='', name='img_1'):
    matrix = np.matrix(adjacency_matrix)
    graph = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph())
    if not vertices:
        vertices = xrange(1, len(adjacency_matrix) + 1)
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
    name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images/') + str(name) + '.png'
    plt.savefig(name, figsize=(20, 20), dpi=1200)
    plt.clf()
    return


def in_degree_statistics():
    with df.connect_to_db() as conn:
        c = conn.cursor()
        for row in c.execute('SELECT in_degree, running_time, number_of_nodes FROM inhibition'):
            in_degree, running_time, number_of_nodes = row
            d = eval(in_degree)
            print number_of_nodes, max(d.values()), min(d.values()), numpy.mean((d.values())), running_time


def draw_input_graph(row_id=''):
    with df.connect_to_db() as conn:
        c = conn.cursor()
        if row_id:
            query = 'SELECT id, input_matrix FROM inhibition WHERE id = ' + str(row_id)  # horrible insecure
        else:
            query = 'SELECT id, input_matrix FROM inhibition'
        for row in c.execute(query):
            row_id, input_matrix = row
            m = eval(input_matrix)
            dg.draw_graph(m, name='1input_' + str(row_id))


def draw_result_graph(row_id=''):
    with df.connect_to_db() as conn:
        c = conn.cursor()
        if row_id:
            query = 'SELECT id, results, input_graph FROM inhibition WHERE results IS NOT NULL AND id = ' + str(row_id)  # horrible insecure
        else:
            query = 'SELECT id, results, input_graph FROM inhibition WHERE results IS NOT NULL'
        for row in c.execute(query):
            row_id, result, input_graph = row
            results = eval(result)
            input_graph = eval(input_graph)
            for i, r in enumerate(results):
                r = op.convert_undirected_to_directed(r, input_graph)
                m = g.Graph.to_adj_matrix(r)
                dg.draw_graph(m, vertices=sorted(r.keys()), name='1input_' + str(row_id) + '_res_' + str(i+1) + '_of_' + str(len(results)))