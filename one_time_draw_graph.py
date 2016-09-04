# this files reads graph from db and draws it
# TODO later I will draw graphs by default

import db_functions as df
import numpy
import draw_graph as dg
import graph_op as op


def in_degree_statistics():
    with df.connect_to_db() as conn:
        c = conn.cursor()
        for row in c.execute('SELECT in_degree, running_time, number_of_nodes FROM inhibition'):
            in_degree, running_time, number_of_nodes = row
            d = eval(in_degree)
            print number_of_nodes, max(d.values()), min(d.values()), numpy.mean((d.values())), running_time


def draw_graph_for_every_input_matrix():
    with df.connect_to_db() as conn:
        c = conn.cursor()
        for row in c.execute('SELECT id, input_matrix FROM inhibition'):
            row_id, input_matrix = row
            m = eval(input_matrix)
            dg.draw_graph(m, name='input_' + str(row_id))


def draw_graph_for_every_non_empty_result():
    with df.connect_to_db() as conn:
        c = conn.cursor()
        for row in c.execute('SELECT id, results FROM inhibition WHERE results IS NOT NULL'):
            row_id, result = row
            results = eval(result)
            total = len(results)
            for i, r in enumerate(results):
                m = op.to_adj_matrix(r)
                dg.draw_graph(m, name='input_' + str(row_id) + '_res_' + str(i+1) + '_of_' + str(total))

if __name__ == '__main__':
    draw_graph_for_every_non_empty_result()