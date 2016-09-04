import sqlite3
import os
import platform


if platform.system() == 'Windows':
    path_to_db = 'D:\Dropbox\PyCharm_projects\inhibitor_graph_v1.1\inhibition.db'
    path_to_schema = 'D:\Dropbox\PyCharm_projects\inhibitor_graph_v1.1\sql\create_schema.sql'
else:
    path_to_db = '/Users/vstashkov/PycharmProjects/learning/inhibitor/inhibition.db'
    path_to_schema = '/Users/vstashkov/PycharmProjects/learning/inhibitor/sql/create_schema.sql'


def insert_into_db(row_id,
                   number_of_nodes=None,
                   input_graph=None,
                   input_matrix=None,
                   inhibited_edges=None,
                   in_degree=None,
                   out_degree=None,
                   inhibition_degree=None,
                   inhibited_vertices=None,
                   non_inhibited_vertices=None,
                   known_incompatible_nodes=None,
                   bin_of_edges=None,
                   not_feasible=None,
                   results=None,
                   number_of_results=None,
                   running_time=None):
    conn = connect_to_db()
    c = conn.cursor()

    if not is_id_in_db(row_id):
        c.execute("INSERT INTO inhibition(id) VALUES (?)", [row_id])

    if number_of_nodes:
        c.execute("UPDATE inhibition SET number_of_nodes = ? WHERE id = ?", [str(number_of_nodes), row_id])
    if input_graph:
        c.execute("UPDATE inhibition SET input_graph = ? WHERE id = ?", [str(input_graph), row_id])
    if input_matrix:
        c.execute("UPDATE inhibition SET input_matrix = ? WHERE id = ?", [str(input_matrix), row_id])
    if inhibited_edges:
        c.execute("UPDATE inhibition SET inhibited_edges = ? WHERE id = ?", [str(inhibited_edges), row_id])
    if in_degree:
        c.execute("UPDATE inhibition SET in_degree = ? WHERE id = ?", [str(in_degree), row_id])
    if out_degree:
        c.execute("UPDATE inhibition SET out_degree = ? WHERE id = ?", [str(out_degree), row_id])
    if inhibition_degree:
        c.execute("UPDATE inhibition SET inhibition_degree = ? WHERE id = ?", [str(inhibition_degree), row_id])
    if inhibited_vertices:
        c.execute("UPDATE inhibition SET inhibited_vertices = ? WHERE id = ?", [str(inhibited_vertices), row_id])
    if non_inhibited_vertices:
        c.execute("UPDATE inhibition SET non_inhibited_vertices = ? WHERE id = ?", [str(non_inhibited_vertices), row_id])
    if known_incompatible_nodes:
        c.execute("UPDATE inhibition SET known_incompatible_nodes = ? WHERE id = ?",
                  [str(known_incompatible_nodes), row_id])
    if bin_of_edges:
        c.execute("UPDATE inhibition SET bin_of_edges = ? WHERE id = ?", [str(bin_of_edges), row_id])
    if not_feasible:
        c.execute("UPDATE inhibition SET not_feasible = ? WHERE id = ?", [str(not_feasible), row_id])
    if results:
        c.execute("UPDATE inhibition SET results = ? WHERE id = ?", [str(results), row_id])
    if number_of_results:
        c.execute("UPDATE inhibition SET number_of_results = ? WHERE id = ?", [str(number_of_results), row_id])
    if running_time:
        c.execute("UPDATE inhibition SET running_time = ? WHERE id = ?", [str(running_time), row_id])

    conn.commit()
    conn.close()


def if_not_exists_create_database():
    global path_to_schema
    global path_to_db
    db_is_new = not os.path.exists(path_to_db)
    path_to_schema = ''
    with connect_to_db() as conn:
        if db_is_new:
            with open(path_to_schema, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
        else:
            pass


def connect_to_db():
    global path_to_db
    return sqlite3.connect(path_to_db)


def get_next_id_from_db():
    with connect_to_db() as conn:
        c = conn.cursor()
        c.execute('''select max(id) from inhibition''')
        max_id = c.fetchone()
    if max_id[0] is None:
        return 1
    else:
        return max_id[0] + 1


def is_id_in_db(row_id):
    with connect_to_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM inhibition WHERE id=?', [str(row_id)])
        if c.fetchone():
            return True
        else:
            return False
