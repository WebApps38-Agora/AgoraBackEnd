import unittest

from utils.fenwick_tree import FenwickTree


class FenwickTest(unittest.TestCase):

    def setUp(self):
        self.ft = FenwickTree(10)

    def test_range_sum_and_retrieval(self):
        self.ft.add_range(0, 3, 10)
        self.ft.add_range(2, 4, 5)

        self.assertEqual(self.ft[0], 10)
        self.assertEqual(self.ft[2], 15)
        self.assertEqual(self.ft[3], 5)
        self.assertEqual(self.ft[4], 0)

    def test_index_check(self):
        self.assertRaises(TypeError, self.ft.__getitem__, "a")
        self.assertRaises(KeyError, self.ft.__getitem__, 10)
        self.assertRaises(TypeError, self.ft.__getitem__, slice(0, 2))
        self.assertRaises(KeyError, self.ft.add_range, -5, 2)
        try:
            self.ft.add_range(0, 10)
        except KeyError:
            self.fail("End idx == size shouldn't fail")
