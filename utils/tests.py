import unittest

from utils.fenwick_tree import FenwickTree


class FenwickTest(unittest.TestCase):

    def setUp(self):
        self.ft = FenwickTree(10)

    def test_range_sum(self):
        self.ft.add_range(0, 3, 10)
        self.ft.add_range(2, 4, 5)

        self.assertEqual(self.ft[0], 10)
        self.assertEqual(self.ft[2], 15)
        self.assertEqual(self.ft[3], 5)
        self.assertEqual(self.ft[4], 0)
