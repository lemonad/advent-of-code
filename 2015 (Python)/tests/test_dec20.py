import unittest

from december20 import Solver


class TestDec20(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertEqual(Solver.get_count(1), 10)
        self.assertEqual(Solver.get_count(2), 30)
        self.assertEqual(Solver.get_count(3), 40)
        self.assertEqual(Solver.get_count(4), 70)
        self.assertEqual(Solver.get_count(5), 60)
        self.assertEqual(Solver.get_count(6), 120)
        self.assertEqual(Solver.get_count(7), 80)
        self.assertEqual(Solver.get_count(8), 150)
        self.assertEqual(Solver.get_count(9), 130)


if __name__ == '__main__':
    unittest.main()
