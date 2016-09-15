from unittest import TestCase
from collections import defaultdict
import graph as gr
import graph_op as op
import example_graphs as ex
import main as i
import bin_of_edges
from rule import exactly_one_one_inhibited, more_than_one_one_inhibited, exactly_one_no_inhibited, \
    more_than_one_no_inhibited, two_or_more_all_inhibited


class TestRemove_incompatible_nodes(TestCase):
    def test_remove_incompatible_nodes(self):
        d = {'1F': ['2T', '3T'],
             '1T': ['2F', '3F'],
             '2F': ['4F'],
             '2T': ['4T'],
             '3T2T': []}
        # given a node '2T'
        inc_nodes = ['2F', '3T2T']
        correct_answer = {'1F': ['2T', '3T'],
                          '1T': ['3F'],
                          '2T': ['4T']}
        self.assertEqual(i.remove_incompatible_nodes(d, inc_nodes), correct_answer)

    def test_remove_incompatible_nodes_1(self):
        d = {'2T': ['3T'], '3T': [], '3F': [], '1F': ['2T']}
        # given a node 3F
        inc_nodes = ['3T']
        correct_answer = {'2T': [], '1F': ['2T']}
        self.assertEqual(i.remove_incompatible_nodes(d, inc_nodes), correct_answer)


class TestOut_degree(TestCase):
    def test_out_degree_I(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_I), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_II(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_II), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_III(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_III), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_IV(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_IV), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_V(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_V), {'1': 1, '2': 0})

    def test_out_degree_VI(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_VI), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_X(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_X), {'1': 1, '2': 1, '3': 1, '4': 0})

    def test_out_degree_test(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_test), {'1': 1, '2': 1, '3': 2, '4': 0, '5': 1, '6': 1, '7': 0})

    def test_out_degree_XXI(self):
        self.assertEqual(gr.Graph.get_out_degree(ex.graph_XXI), {'1': 4, '2': 1, '3': 1, '4': 0, '5': 0})


class TestIn_degree(TestCase):
    def test_in_degree_I(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_I), {'1': 0, '2': 1, '3': 1})

    def test_in_degree_II(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_II), {'1': 0, '2': 0, '3': 2})

    def test_in_degree_III(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_III), {'1': 0, '2': 0, '3': 2})

    def test_in_degree_IV(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_IV), {'1': 0, '2': 1, '3': 1})

    def test_in_degree_V(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_V), {'1': 0, '2': 1})

    def test_in_degree_VI(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_VI), {'1': 0, '2': 0, '3': 2})

    def test_in_degree_X(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_X), {'1': 0, '2': 0, '3': 0, '4': 3})

    def test_in_degree_test(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_test), {'1': 0, '2': 0, '3': 2, '4': 1, '5': 1, '6': 1, '7': 1})

    def test_in_degree_XXI(self):
        self.assertEqual(gr.Graph.get_in_degree(ex.graph_XXI), {'1': 0, '2': 1, '3': 1, '4': 2, '5': 2})


class TestInhibited_edges(TestCase):
    def test_inhibited_edges_I(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_I), [('1', '2')])

    def test_inhibited_edges_II(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_II), [('2', '3')])

    def test_inhibited_edges_III(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_III), [('1', '3'), ('2', '3')])

    def test_inhibited_edges_IV(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_IV), [('1', '2'), ('2', '3')])

    def test_inhibited_edges_V(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_V), [])

    def test_inhibited_edges_VI(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_VI), [])

    def test_inhibited_edges_X(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_X), [('1', '4'), ('2', '4'), ('3', '4')])

    def test_inhibited_edges_test(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_test), [('3', '4'), ('5', '6')])

    def test_inhibited_edges_XXI(self):
        self.assertEqual(gr.Graph.get_inhibited_edges(ex.graph_XXI), [('1', '2'), ('3', '5')])


class TestConvert_adj_matrix_to_dict(TestCase):
    def test_convert_adj_matrix_to_dict_I(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_I), {'1': ['2'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_II(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_II), {'1': ['3'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_III(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_III), {'1': ['3'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_IV(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_IV), {'1': ['2'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_V(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_V), {'1': ['2'], '2': []})

    def test_convert_adj_matrix_to_dict_VI(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_VI), {'1': ['3'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_X(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_X), {'1': ['4'], '2': ['4'], '3': ['4'], '4': []})

    def test_convert_adj_matrix_to_dict_test(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_test),
                         {'1': ['3'], '2': ['3'], '3': ['4', '5'], '4': [], '5': ['6'], '6': ['7'], '7': []})

    def test_convert_adj_matrix_to_dict_XXI(self):
        self.assertEqual(gr.Graph.to_dict(ex.graph_XXI),
                         {'1': ['2', '3', '4', '5'], '2': ['4'], '3': ['5'], '4': [], '5': []})


class TestGenerate_adj_matrix(TestCase):
    def test_generate_adj_matrix_1(self):
        n = 10
        matrix = [list(i) for i in zip(*op.generate_adj_matrix(n))]
        self.assertTrue(all([row.count(-1) <= 2 for row in matrix]))


class TestInc_nodes(TestCase):
    def test_inc_nodes_composite_node(self):
        n = '5T88F'
        correct_answer = ['5F88T', '5T', '88F', '5F', '88T']
        self.assertEqual(op.incompatible_nodes(n), correct_answer)

    def test_inc_nodes_simple_node(self):
        n = '5T'
        correct_answer = ['5F']
        self.assertEqual(op.incompatible_nodes(n), correct_answer)


class TestInc_nodes(TestCase):
    def test_nodes_incompatible_with_dict_simple_node_incompatible(self):
        n = '123F'
        d = {'1F': ['123T'],
             '5F': ['123F5T', '1F'],
             '88T12F': ['123F7T', '5F'],
             '123F': [],
             '123T': [],
             '123F7T': [],
             '123F5T': []}
        correct_answer = ['123T', '123F7T', '123F5T']
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_simple_node_compatible(self):
        n = '123F'
        d = {'1F': ['12T'], '5F': ['12F5T', '16T'], '88T12F': ['12T7T', '5F'], '123F': []}
        correct_answer = []
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_comp_node_incompatible(self):
        n = '12F8T'
        d = {'1F': ['123T'], '5F': ['123F5T', '16T'], '88T12F': ['123T7T', '12F'], '12F8T': [], '12F': []}
        correct_answer = ['12F', '88T12F']
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_comp_node_incompatible_1(self):
        n = '12F8T'
        d = {'1F': ['123T'], '5F': ['123F5T', '16T'], '88T12F': ['123T7T', '12F'], '12F8T': []}
        correct_answer = ['88T12F']
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_comp_node_compatible(self):
        n = '12F8T'
        d = {'12F8T': ['123T'], '1F': ['123T'], '5F': ['123F5T', '16T'], '88F13F': ['123T7T', '5F']}
        correct_answer = []
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)


class Testis_connected(TestCase):
    def test_is_connected_false(self):
        d = {'1': ['2', '3'], '4': ['6', '7'], '3': [], '2': [], '6': [], '7': []}  # two disconnected components
        self.assertFalse(op.is_connected(d))

    def test_is_connected_false_1(self):
        d = {'1': [], '3': []}  # two disconnected components
        self.assertFalse(op.is_connected(d))

    def test_is_connected_true(self):
        d = {'1': ['2', '3'], '3': ['6', '7'], '2': [], '6': [], '7': []}
        self.assertTrue(op.is_connected(d))

    def test_is_connected_false_1(self):
        d = {'2T': [], '1F': ['2T'], '3F': []}  # not connected
        self.assertFalse(op.is_connected(d))

    def test_is_connected_true_1(self):
        d = {'2T': ['3T'], '1F': ['2T'], '3T': []}
        self.assertTrue(op.is_connected(d))


class Testconvert_directed_to_undirected(TestCase):
    def test_convert_directed_to_undirected(self):
        d = {'1': ['2', '3'], '3': ['6', '7'], '2': [], '6': [], '7': []}
        correct_answer = {'1': ['2', '3'], '3': ['6', '7', '1'], '2': ['1'], '7': ['3'], '6': ['3']}
        self.assertEqual(op.convert_directed_to_undirected(d), correct_answer)

    def test_convert_directed_to_undirected_1(self):
        d = {'1': ['2', '3'], '2': [], '3': []}
        correct_answer = {'1': ['2', '3'], '2': ['1'], '3': ['1']}
        self.assertEqual(op.convert_directed_to_undirected(d), correct_answer)


class TestExactly_one_one_inhibited(TestCase):
    # CASE I.1 and I.2
    def test_exactly_one_one_inhibited_len_1(self):
        u, v = '1', '2'  # edge u-->v is inhibited
        g = gr.Graph.to_dict(ex.graph_I)
        bin = defaultdict(set)
        correct_answer = {'2T': set(['3T']), '1T': set(['2F']), '1F': set(['2T'])}
        self.assertEqual(exactly_one_one_inhibited(g, u, v, bin), correct_answer)

    def test_exactly_one_one_inhibited_len_more_than_1(self):
        u, v = '123', '1'  # edge u-->v is inhibited
        g = {'123': ['1'], '1': ['125'], '125': []}
        bin = defaultdict(set)
        correct_answer = {'1T': ['125T'], '123T': ['1F'], '123F': ['1T']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(exactly_one_one_inhibited(g, u, v, bin), correct_answer)

    def test_exactly_one_one_inhibited_len_more_than_1_reverse(self):
        u, v = '1', '123'  # edge u-->v is inhibited
        g = {'1': ['123'], '123': ['125'], '125': []}
        bin = defaultdict(set)
        correct_answer = {'123T': ['125T'], '1T': ['123F'], '1F': ['123T']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(exactly_one_one_inhibited(g, u, v, bin), correct_answer)


class TestMore_than_one_one_inhibited(TestCase):
    # CASE II
    def test_more_than_one_one_inhibited_len_1(self):
        u, v = '2', '3'  # edge u-->v is inhibited
        g = gr.Graph.to_dict(ex.graph_II)
        bin = defaultdict(set)
        correct_answer = {'2T': ['3T'], '1T': ['3F'], '1F2T': ['3T'], '1F': ['3T'], '2F': ['3F'], '1T2F': ['3F']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(more_than_one_one_inhibited(g, u, v, bin), correct_answer)

    def test_more_than_one_one_inhibited_len_more_than_1(self):
        u, v = '123', '1'  # edge u-->v is inhibited
        g = {'123': ['1'], '125': ['1'], '1': []}
        bin = defaultdict(set)
        correct_answer = {'123T': ['1T'], '123F': ['1F'], '125T': ['1F'], '125F': ['1T'], '125T123F': ['1F'],
                          '125F123T': ['1T']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(more_than_one_one_inhibited(g, u, v, bin), correct_answer)

    def test_more_than_one_one_inhibited_len_more_than_1_reverse(self):
        u, v = '1', '123'  # edge u-->v is inhibited
        g = {'1': ['123'], '12': ['123'], '123': []}
        bin = defaultdict(set)
        correct_answer = {'1T': ['123T'], '1F': ['123F'], '12T': ['123F'], '12F': ['123T'], '12T1F': ['123F'],
                          '12F1T': ['123T']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(more_than_one_one_inhibited(g, u, v, bin), correct_answer)


class TestExactly_one_no_inhibited(TestCase):
    # CASE V
    def test_exactly_one_no_inhibited(self):
        v = '2'
        g = gr.Graph.to_dict(ex.graph_V)
        bin = defaultdict(set)
        correct_answer = {'1T': ['2T'], '1F': ['2F']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(exactly_one_no_inhibited(g, v, bin), correct_answer)

    def test_exactly_one_no_inhibited_len_more_than_1(self):
        v = '2'
        g = {'123': ['2']}
        bin = defaultdict(set)
        correct_answer = {'123T': ['2T'], '123F': ['2F']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(exactly_one_no_inhibited(g, v, bin), correct_answer)

    def test_exactly_one_no_inhibited_len_more_than_1_reverse(self):
        v = '123'
        g = {'2': ['123']}
        bin = defaultdict(set)
        correct_answer = {'2T': ['123T'], '2F': ['123F']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(exactly_one_no_inhibited(g, v, bin), correct_answer)


class Testmore_than_one_no_inhibited(TestCase):
    # CASE VI
    def test_more_than_one_no_inhibited(self):
        v = '1'
        g = {'123': ['1'], '125': ['1'], '1': []}
        bin = defaultdict(set)
        correct_answer = {'123T': ['1T'], '125F': ['1F'], '123F': ['1F'], '125T': ['1T'], '123T125T': ['1T']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(more_than_one_no_inhibited(g, v, bin), correct_answer)

    def test_more_than_one_no_inhibited_len_more_1(self):
        v = '123'
        g = {'1': ['123'], '12': ['123'], '123': []}
        bin = defaultdict(set)
        correct_answer = {'1T12T': ['123T'],
                          '12T': ['123T'], '12F': ['123F'],
                          '1F': ['123F'], '1T': ['123T']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(more_than_one_no_inhibited(g, v, bin), correct_answer)


class Testtwo_or_more_all_inhibited(TestCase):
    # CASE III
    def test_two_or_more_all_inhibited(self):
        v = '3'
        g = gr.Graph(ex.graph_III).dict_graph
        bin = defaultdict(set)
        correct_answer = {'2T': ['3F'], '2F': ['3T'],
                          '1F': ['3T'], '1T': ['3F'],
                          '1F2F': ['3T'], '1T2T': ['3F']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(two_or_more_all_inhibited(g, v, bin), correct_answer)

    def test_two_or_more_all_inhibited_len_more_1(self):
        v = '123'
        g = {'1': ['123'], '12': ['123'], '123': []}
        bin = defaultdict(set)
        correct_answer = {'1F12F': ['123T'], '1T12T': ['123F'],
                          '1T': ['123F'], '1F': ['123T'],
                          '12F': ['123T'], '12T': ['123F']}
        for key, value in correct_answer.iteritems():
            correct_answer[key] = set(value)
        self.assertEqual(two_or_more_all_inhibited(g, v, bin), correct_answer)


class TestTo_adj_matrix(TestCase):
    def test_to_adj_matrix(self):
        g = {'1': ['3'], '2': ['3'], '3': []}
        self.assertEqual(gr.Graph.to_adj_matrix(g), [[0, 0, 1], [0, 0, 1], [0, 0, 0]])


class Testget_number_of_nodes(TestCase):
    def test_get_number_of_nodes(self):
        d = {'1T': ['3T'], '2T': ['3T'], '3T': []}
        self.assertEqual(op.get_number_of_nodes(d), 3)

    def test_get_number_of_nodes_composite(self):
        d = {'1T6T': ['3T'], '2T': ['3T'], '3T': []}
        self.assertEqual(op.get_number_of_nodes(d), 4)

    def test_get_number_of_nodes_composite_1(self):
        d = {'1T': ['2T'], '2T': []}
        self.assertEqual(op.get_number_of_nodes(d), 2)


class TestGet_nodes_incompatible_inside_dict(TestCase):
    def test_get_nodes_incompatible_inside_dict(self):
        d = {'5T': ['6F'], '5F': ['6T'], '6F': [], '6T': []}
        self.assertEqual(op.get_nodes_incompatible_inside_dict(d), ['5T', '5F', '6T', '6F'])


class TestGenerate_graph(TestCase):
    def test_generate_graph(self):
        # since function is random, at least we can test the size of the returning obj
        self.assertEqual(len(i.generate_connected_graph(5).matrix_graph), 5)
        self.assertEqual(len(i.generate_connected_graph(5).matrix_graph), 5)


class TestGenerate_bin_of_edges(TestCase):
    def test_generate_bin_of_edges(self):
        m = [[0, 0, 1], [0, 0, 1], [0, 0, 0]]
        gg = gr.Graph(m)
        correct_answer = {'2T': ['3T'], '2F': ['3F'], '1T': ['3T'], '1T2T': ['3T'], '1F': ['3F'], '3F': [], '3T': []}
        self.assertEqual(bin_of_edges.generate_bin_of_edges(gg), correct_answer)

    def test_generate_bin_of_edges_inhib(self):
        # g = {'1': ['3'], '2': ['3'], '3': []}
        m = [[0, 0, 1], [0, 0, -1], [0, 0, 0]]
        gg = gr.Graph(m)
        correct_answer = {'2T': ['3T'], '1T': ['3F'], '1F2T': ['3T'], '3T': [],
                          '1F': ['3T'], '2F': ['3F'], '1T2F': ['3F'], '3F': []}
        self.assertEqual(bin_of_edges.generate_bin_of_edges(gg), correct_answer)

    def test_generate_bin_of_edges_inhib_degree_2(self):
        # g = {'1': ['3'], '2': ['3'], '3': []}
        m = [[0, 0, -1], [0, 0, -1], [0, 0, 0]]
        gg = gr.Graph(m)
        correct_answer = {'2T': ['3F'], '1F2F': ['3T'], '1T2T': ['3F'], '2F': ['3T'],
                          '1F': ['3T'], '1T': ['3F'], '3F': [], '3T': []}
        self.assertEqual(bin_of_edges.generate_bin_of_edges(gg), correct_answer)

    def test_generate_bin_of_edges_inhib_degree_1(self):
        # g = {'1': ['2'], '2': []}
        m = [[0, -1], [0, 0]]
        gg = gr.Graph(m)
        correct_answer = {'2T': [], '2F': [], '1T': ['2F'], '1F': ['2T']}
        self.assertEqual(bin_of_edges.generate_bin_of_edges(gg), correct_answer)

    def test_generate_bin_of_edges_inhib_degree_0(self):
        # g = {'1': ['2'], '2': []}
        m = [[0, 1], [0, 0]]
        gg = gr.Graph(m)
        correct_answer = {'2T': [], '2F': [], '1T': ['2T'], '1F': ['2F']}
        self.assertEqual(bin_of_edges.generate_bin_of_edges(gg), correct_answer)


# class TestExecute_algo(TestCase):
#     def test_execute_algo(self):
#         node_count = 3  # ex.graph_II
#         b = {'2T': ['3T'], '1T': ['3F'], '1F2T': ['3T'], '3T': [], '1F': ['3T'], '2F': ['3F'], '1T2F': ['3F'], '3F': []}
#         correct_answer = {'2T': ['3T'], '1F': ['3T'], '3T': [],
#                           '2F': ['3F'], '1T': ['3F'], '3F': [],
#                           '1F2T': ['3T'], '3T': [],
#                           '3F': [], '1T2F': ['3F']}
#         self.assertEqual(i.process_parallel(b, node_count), correct_answer)


class TestAdd_to_not_feasible(TestCase):
    def test_add_to_not_feasible(self):
        d = {'1T': ['2T'], '2F': []}
        nf = [[], [], []]
        correct_answer = [[], [], [{'2F': [], '1T': ['2T']}]]
        self.assertEqual(i.add_to_list_of_not_feasible_dicts(d, nf), correct_answer)


class TestRecursive_teardown(TestCase):
    def test_recursive_teardown_none(self):
        node = '2F'
        d = {'1T': ['2T'], '2F': [], '2T': []}
        node_count = 2
        result = []
        not_feasible = [[], [], []]
        pre_inc_nodes = {'2F': ['2T']}
        # this should return none, because if we remove 2T then the dict is incompatible
        self.assertEqual(
            i.recursive_teardown(node, d, node_count, result, not_feasible, pre_inc_nodes, recursion_level=0), None)

    def test_recursive_teardown_return_non_empty(self):
        node = '2T'
        d = {'1T': ['2T'], '2F': [], '2T': []}
        node_count = 2
        result = []
        not_feasible = [[], [], []]
        pre_inc_nodes = {'2F': ['2T'], '2T': ['2F']}
        correct_answer = {'2T': [], '1T': ['2T']}
        self.assertEqual(
            i.recursive_teardown(node, d, node_count, result, not_feasible, pre_inc_nodes, recursion_level=0),
            correct_answer)

    def test_recursive_teardown_return_recursion(self):
        node = '1T'
        d = {'1T': ['2T'], '2F': [], '2T': []}
        node_count = 2
        result = []
        not_feasible = [[], [], [], []]
        pre_inc_nodes = {'2F': ['2T'], '2T': ['2F'], '1T': []}
        self.assertEqual(
            i.recursive_teardown(node, d, node_count, result, not_feasible, pre_inc_nodes, recursion_level=0),
            None)

    def test_recursive_teardown_return_disconnected(self):
        # this dict is compatible with itself but is disconnected
        node = '1T'
        d = {'1T': [], '2F': []}
        node_count = 2
        result = []
        not_feasible = [[], [], [], []]
        pre_inc_nodes = {'2F': ['2T'], '2T': ['2F'], '1T': []}
        self.assertEqual(
            i.recursive_teardown(node, d, node_count, result, not_feasible, pre_inc_nodes, recursion_level=0),
            None)

    def test_recursive_teardown_return_not_feasible(self):
        # this dict is compatible with itself but is disconnected
        node = '1T'
        d = {'1T': [], '2F': []}
        node_count = 2
        result = []
        not_feasible = [[], [], [{'1T': [], '2F': []}], []]
        pre_inc_nodes = {'2F': ['2T'], '2T': ['2F'], '1T': []}
        self.assertEqual(
            i.recursive_teardown(node, d, node_count, result, not_feasible, pre_inc_nodes, recursion_level=0),
            None)

# class TestSet_up_preset(TestCase):
#     def test_set_up_preset(self):
#         correct_answer = (
#             {'2T': ['3T'], '1T': ['3F'], '1F2T': ['3T'], '3T': [],
#              '1F': ['3T'], '2F': ['3F'], '1T2F': ['3F'], '3F': []}, 3)
#         self.assertEqual(i.set_up_preset(ex.graph_II), correct_answer)


class TestConvert_undirected_to_directed(TestCase):
    def setUp(self):
        self.initial_example_II = {'1': ['3'], '3': [], '2': ['3']}
        self.initial_2_node = {'1': ['2'], '2': []}

    def tearDown(self):
        del self.initial_example_II

    def test_example_II_1(self):
        graph = {'1F2T': ['3T'], '3T': ['1F2T']}
        result = {'1F2T': ['3T'], '3T': []}
        self.assertEqual(op.convert_undirected_to_directed(graph, self.initial_example_II), result)

    def test_example_II_2(self):
        graph = {'2F': ['3F'], '1T': ['3F'], '3F': ['1T', '2F']}
        result = {'2F': ['3F'], '1T': ['3F'], '3F': []}
        self.assertEqual(op.convert_undirected_to_directed(graph, self.initial_example_II), result)

    def test_example_II_3(self):
        graph = {'2T': ['3T'], '1F': ['3T'], '3T': ['2T', '1F']}
        result = {'2T': ['3T'], '1F': ['3T'], '3T': []}
        self.assertEqual(op.convert_undirected_to_directed(graph, self.initial_example_II), result)

    def test_example_II_4(self):
        graph = {'3F': ['1T2F'], '1T2F': ['3F']}
        result = {'3F': [], '1T2F': ['3F']}
        self.assertEqual(op.convert_undirected_to_directed(graph, self.initial_example_II), result)

    def test_2_node(self):
        graph = {'1T': ['2T'], '2T': ['1F']}
        result = {'1T': ['2T'], '2T': []}
        self.assertEqual(op.convert_undirected_to_directed(graph, self.initial_2_node), result)