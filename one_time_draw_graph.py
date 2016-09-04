import db_functions as df
import numpy
import draw_graph as dg
import graph_op as op

conn = df.acquire_connection_to_db()

c = conn.cursor()

# c.execute('SELECT input_matrix FROM inhibition')
# print c.fetchone()


def in_degree_statistics():
    for row in c.execute('SELECT in_degree, running_time, number_of_nodes FROM inhibition'):
        in_degree, running_time, number_of_nodes = row
        d = eval(in_degree)
        print number_of_nodes, max(d.values()), min(d.values()), numpy.mean((d.values())), running_time


def draw_graph_for_every_input_matrix():
    for row in c.execute('SELECT id, input_matrix FROM inhibition'):
        row_id, input_matrix = row
        m = eval(input_matrix)
        dg.draw_graph(m)


def draw_graph_for_every_non_empty_result():
    for row in c.execute('SELECT id, results FROM inhibition WHERE results IS NOT NULL'):
        row_id, result = row
        results = eval(result)
        for r in results:
            m = op.to_adj_matrix(r)
            dg.draw_graph(m)

conn.close()
