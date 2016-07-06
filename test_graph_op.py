from unittest import TestCase

import graph_op as op
import example_graphs as ex


class TestOut_degree(TestCase):
    def test_out_degree_I(self):
        self.assertEqual(op.out_degree(ex.graph_I), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_II(self):
        self.assertEqual(op.out_degree(ex.graph_II), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_III(self):
        self.assertEqual(op.out_degree(ex.graph_III), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_IV(self):
        self.assertEqual(op.out_degree(ex.graph_IV), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_V(self):
        self.assertEqual(op.out_degree(ex.graph_V), {'1': 0, '2': 1})

    def test_out_degree_VI(self):
        self.assertEqual(op.out_degree(ex.graph_VI), {'1': 1, '2': 1, '3': 0})

    def test_out_degree_X(self):
        self.assertEqual(op.out_degree(ex.graph_X), {'1': 1, '2': 1, '3': 1, '4': 0})

    def test_out_degree_test(self):
        self.assertEqual(op.out_degree(ex.graph_test), {'1': 1, '2': 1, '3': 2, '4': 0, '5': 1, '6': 1, '7': 0})

    def test_out_degree_XXI(self):
        self.assertEqual(op.out_degree(ex.graph_XXI), {'1': 4, '2': 1, '3': 1, '4': 0, '5': 0})


class TestOut_degree(TestCase):
    def test_in_degree_I(self):
        self.assertEqual(op.in_degree(ex.graph_I), {'1': 0, '2': 1, '3': 1})

    def test_in_degree_II(self):
        self.assertEqual(op.in_degree(ex.graph_II), {'1': 0, '2': 0, '3': 2})

    def test_in_degree_III(self):
        self.assertEqual(op.in_degree(ex.graph_III), {'1': 0, '2': 0, '3': 2})

    def test_in_degree_IV(self):
        self.assertEqual(op.in_degree(ex.graph_IV), {'1': 0, '2': 1, '3': 1})

    def test_in_degree_V(self):
        self.assertEqual(op.in_degree(ex.graph_V), {'1': 0, '2': 1})

    def test_in_degree_VI(self):
        self.assertEqual(op.in_degree(ex.graph_VI), {'1': 0, '2': 0, '3': 2})

    def test_in_degree_X(self):
        self.assertEqual(op.in_degree(ex.graph_X), {'1': 0, '2': 0, '3': 0, '4': 3})

    def test_in_degree_test(self):
        self.assertEqual(op.in_degree(ex.graph_test), {'1': 0, '2': 0, '3': 2, '4': 1, '5': 1, '6': 1, '7': 1})

    def test_in_degree_XXI(self):
        self.assertEqual(op.in_degree(ex.graph_XXI), {'1': 0, '2': 1, '3': 1, '4': 2, '5': 2})


class TestInhibited_edges(TestCase):
    def test_inhibited_edges_I(self):
        self.assertEqual(op.inhibited_edges(ex.graph_I), ([('1', '2')], {'2': 1}))

    def test_inhibited_edges_II(self):
        self.assertEqual(op.inhibited_edges(ex.graph_II), ([('2', '3')], {'3': 1}))

    def test_inhibited_edges_III(self):
        self.assertEqual(op.inhibited_edges(ex.graph_III), ([('1', '3'), ('2', '3')], {'3': 2}))

    def test_inhibited_edges_IV(self):
        self.assertEqual(op.inhibited_edges(ex.graph_IV), ([('1', '2'), ('2', '3')], {'2': 1, '3': 1}))

    def test_inhibited_edges_V(self):
        self.assertEqual(op.inhibited_edges(ex.graph_V), ([], {}))

    def test_inhibited_edges_VI(self):
        self.assertEqual(op.inhibited_edges(ex.graph_VI), ([], {}))

    def test_inhibited_edges_X(self):
        self.assertEqual(op.inhibited_edges(ex.graph_X), ([('1', '4'), ('2', '4'), ('3', '4')], {'4': 3}))

    def test_inhibited_edges_test(self):
        self.assertEqual(op.inhibited_edges(ex.graph_test), ([('3', '4'), ('5', '6')], {'4': 1, '6': 1}))

    def test_inhibited_edges_XXI(self):
        self.assertEqual(op.inhibited_edges(ex.graph_XXI), ([('1', '2'), ('3', '5')], {'2': 1, '5': 1}))


class TestConvert_adj_matrix_to_dict(TestCase):
    def test_convert_adj_matrix_to_dict_I(self):
        self.assertEqual(op.to_dict(ex.graph_I), {'1': ['2'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_II(self):
        self.assertEqual(op.to_dict(ex.graph_II), {'1': ['3'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_III(self):
        self.assertEqual(op.to_dict(ex.graph_III), {'1': ['3'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_IV(self):
        self.assertEqual(op.to_dict(ex.graph_IV), {'1': ['2'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_V(self):
        self.assertEqual(op.to_dict(ex.graph_V), {'1': ['2'], '2': []})

    def test_convert_adj_matrix_to_dict_VI(self):
        self.assertEqual(op.to_dict(ex.graph_VI), {'1': ['3'], '2': ['3'], '3': []})

    def test_convert_adj_matrix_to_dict_X(self):
        self.assertEqual(op.to_dict(ex.graph_X), {'1': ['4'], '2': ['4'], '3': ['4'], '4': []})

    def test_convert_adj_matrix_to_dict_test(self):
        self.assertEqual(op.to_dict(ex.graph_test), {'1': ['3'], '2': ['3'], '3': ['4', '5'], '4': [], '5': ['6'], '6': ['7'], '7': []})

    def test_convert_adj_matrix_to_dict_XXI(self):
        self.assertEqual(op.to_dict(ex.graph_XXI), {'1': ['2', '3', '4', '5'], '2': ['4'], '3': ['5'], '4': [], '5': []})


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
        d = {'1F': ['123T'], '5F': ['123F5T', '16T'], '88T12F': ['123F7T', '5F']}
        correct_answer = ['123T', '123F7T', '123F5T']
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_simple_node_compatible(self):
        n = '123F'
        d = {'1F': ['12T'], '5F': ['12F5T', '16T'], '88T12F': ['12T7T', '5F']}
        correct_answer = []
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_comp_node_incompatible(self):
        n = '12F8T'
        d = {'1F': ['123T'], '5F': ['123F5T', '16T'], '88T12F': ['123T7T', '12F']}
        correct_answer = ['12F', '88T12F']
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_comp_node_incompatible_1(self):
        n = '12F8T'
        d = {'1F': ['123T'], '5F': ['123F5T', '16T'], '88F12F': ['123T7T', '5F']}
        correct_answer = ['88F12F']
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)

    def test_nodes_incompatible_with_dict_comp_node_compatible(self):
        n = '12F8T'
        d = {'12F8T': ['123T'], '1F': ['123T'], '5F': ['123F5T', '16T'], '88F13F': ['123T7T', '5F']}
        correct_answer = []
        self.assertEqual(op.nodes_incompatible_with_dict(n, d), correct_answer)


class Testis_connected(TestCase):
    def test_is_connected_false(self):
        d = {'1':['2', '3'], '4':['6','7'], '3':[], '2':[], '6':[], '7':[]} # two disconnected components
        self.assertFalse(op.is_connected(d))

    def test_is_connected_false_1(self):
        d = {'1': [], '3': []} # two disconnected components
        self.assertFalse(op.is_connected(d))

    def test_is_connected_true(self):
        d = {'1': ['2', '3'], '3': ['6', '7'], '2':[], '6':[], '7':[]}
        self.assertTrue(op.is_connected(d))

    def test_is_connected_false_1(self):
        d = {'2T': [], '1F': ['2T'], '3F': []} # not connected
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
