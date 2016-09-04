import sqlite3


def insert_into_db(id,
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
    conn = acquire_connection_to_db()
    c = conn.cursor()

    if not is_id_in_db(id):
        c.execute("INSERT INTO inhibition(id) VALUES (?)", [id])

    if number_of_nodes:
        c.execute("UPDATE inhibition SET number_of_nodes = ? WHERE id = ?", [str(number_of_nodes), id])
    if input_graph:
        c.execute("UPDATE inhibition SET input_graph = ? WHERE id = ?", [str(input_graph), id])
    if input_matrix:
        c.execute("UPDATE inhibition SET input_matrix = ? WHERE id = ?", [str(input_matrix), id])
    if inhibited_edges:
        c.execute("UPDATE inhibition SET inhibited_edges = ? WHERE id = ?", [str(inhibited_edges), id])
    if in_degree:
        c.execute("UPDATE inhibition SET in_degree = ? WHERE id = ?", [str(in_degree), id])
    if out_degree:
        c.execute("UPDATE inhibition SET out_degree = ? WHERE id = ?", [str(out_degree), id])
    if inhibition_degree:
        c.execute("UPDATE inhibition SET inhibition_degree = ? WHERE id = ?", [str(inhibition_degree), id])
    if inhibited_vertices:
        c.execute("UPDATE inhibition SET inhibited_vertices = ? WHERE id = ?", [str(inhibited_vertices), id])
    if non_inhibited_vertices:
        c.execute("UPDATE inhibition SET non_inhibited_vertices = ? WHERE id = ?", [str(non_inhibited_vertices), id])
    if known_incompatible_nodes:
        c.execute("UPDATE inhibition SET known_incompatible_nodes = ? WHERE id = ?",
                  [str(known_incompatible_nodes), id])
    if bin_of_edges:
        c.execute("UPDATE inhibition SET bin_of_edges = ? WHERE id = ?", [str(bin_of_edges), id])
    if not_feasible:
        c.execute("UPDATE inhibition SET not_feasible = ? WHERE id = ?", [str(not_feasible), id])
    if results:
        c.execute("UPDATE inhibition SET results = ? WHERE id = ?", [str(results), id])
    if number_of_results:
        c.execute("UPDATE inhibition SET number_of_results = ? WHERE id = ?", [str(number_of_results), id])
    if running_time:
        c.execute("UPDATE inhibition SET running_time = ? WHERE id = ?", [str(running_time), id])

    conn.commit()
    conn.close()


def create_database():
    conn = acquire_connection_to_db()
    c = conn.cursor()
    c.execute("DROP TABLE inhibition")
    c.execute('''CREATE TABLE inhibition
                 (
                 id INTEGER,
                 number_of_nodes TEXT,
                 input_graph TEXT,
                 input_matrix TEXT,
                 inhibited_edges TEXT,
                 in_degree TEXT,
                 out_degree TEXT,
                 inhibition_degree TEXT,
                 inhibited_vertices TEXT,
                 non_inhibited_vertices TEXT,
                 known_incompatible_nodes TEXT,
                 bin_of_edges TEXT,
                 not_feasible TEXT,
                 results TEXT,
                 number_of_results INT,
                 running_time REAL
                 )''')
    conn.commit()
    conn.close()


def acquire_connection_to_db():
    return sqlite3.connect('/Users/vstashkov/PycharmProjects/learning/inhibitor/inhibition.db')


def get_next_id_from_db():
    conn = acquire_connection_to_db()
    c = conn.cursor()
    c.execute('''select max(id) from inhibition''')
    max_id = c.fetchone()
    conn.close()
    if max_id[0] is None:
        return 1
    else:
        return max_id[0] + 1


def is_id_in_db(row_id):
    conn = acquire_connection_to_db()
    c = conn.cursor()
    c.execute('SELECT id FROM inhibition WHERE id=?', [str(row_id)])
    if c.fetchone():
        return True
    else:
        return False