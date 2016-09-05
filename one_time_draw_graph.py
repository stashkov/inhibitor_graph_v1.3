# this files reads graph from db and draws it
# TODO later I will draw graphs by default

import db_functions as df
import numpy
import draw_graph as dg
import graph_op as op
import graph as g


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
            query = 'SELECT id, input_matrix FROM inhibition'
        else:
            query = 'SELECT id, input_matrix FROM inhibition WHERE id = ' + str(row_id)  # horrible insecure
        for row in c.execute(query):
            row_id, input_matrix = row
            m = eval(input_matrix)
            dg.draw_graph(m, name='input_' + str(row_id))


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
                dg.draw_graph(m, vertices=sorted(r.keys()), name='input_' + str(row_id) + '_res_' + str(i+1) + '_of_' + str(len(results)))