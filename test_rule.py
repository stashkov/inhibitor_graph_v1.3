from unittest import TestCase

from rule import exactly_one_one_inhibited, more_than_one_one_inhibited
import example_graphs as ex
import graph_op as op
from collections import defaultdict


class TestExactly_one_one_inhibited(TestCase):
    # CASE I.1 and I.2
    def test_exactly_one_one_inhibited_len_1(self):
        u, v = '1', '2'  # edge u-->v is inhibited
        g = op.to_dict(ex.graph_I)
        bin = defaultdict(list)
        self.assertEqual(exactly_one_one_inhibited(g, u, v, bin), {'2T': ['3T'], '1T': ['2F'], '1F': ['2T']})

    def test_exactly_one_one_inhibited_len_more_than_1(self):
        u, v = '123', '1'  # edge u-->v is inhibited
        g = {'123': ['1'], '1': ['125'], '125': []}
        bin = defaultdict(list)
        correct_answer = {'1T': ['125T'], '123T': ['1F'], '123F': ['1T']}
        self.assertEqual(exactly_one_one_inhibited(g, u, v, bin), correct_answer)

    def test_exactly_one_one_inhibited_len_more_than_1_reverse(self):
        u, v = '1', '123'  # edge u-->v is inhibited
        g = {'1': ['123'], '123': ['125'], '125': []}
        bin = defaultdict(list)
        correct_answer = {'123T': ['125T'], '1T': ['123F'], '1F': ['123T']}
        self.assertEqual(exactly_one_one_inhibited(g, u, v, bin), correct_answer)

class TestMore_than_one_one_inhibited(TestCase):
    # CASE II
    def test_more_than_one_one_inhibited_len_1(self):
        u, v = '2', '3'  # edge u-->v is inhibited
        g = op.to_dict(ex.graph_II)
        bin = defaultdict(list)
        correct_answer = {'2T': ['3T'], '1T': ['3F'], '1F2T': ['3T'], '1F': ['3T'], '2F': ['3F'], '1T2F': ['3F']}
        self.assertEqual(more_than_one_one_inhibited(g, u, v, bin), correct_answer)

    def test_more_than_one_one_inhibited_len_more_than_1(self):
        u, v = '123', '1'  # edge u-->v is inhibited
        g = {'123': ['1'], '125': ['1'], '1': []}
        bin = defaultdict(list)
        correct_answer = {'123T': ['1T'], '123F': ['1F'], '125T': ['1F'], '125F': ['1T'], '125T123F': ['1F'], '125F123T': ['1T']}
        self.assertEqual(more_than_one_one_inhibited(g, u, v, bin), correct_answer)


    def test_more_than_one_one_inhibited_len_more_than_1_reverse(self):
        u, v = '1', '123'  # edge u-->v is inhibited
        g = {'1': ['123'], '12': ['123'], '123': []}
        bin = defaultdict(list)
        correct_answer = {'1T': ['123T'], '1F': ['123F'], '12T': ['123F'], '12F': ['123T'], '12T1F': ['123F'], '12F1T': ['123T']}
        self.assertEqual(more_than_one_one_inhibited(g, u, v, bin), correct_answer)