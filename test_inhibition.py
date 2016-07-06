from unittest import TestCase

import inhibition as i


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
        correct_answer = {'2T': [], '1F': ['2T'], '3F': []}
        self.assertEqual(i.remove_incompatible_nodes(d, inc_nodes), correct_answer)
