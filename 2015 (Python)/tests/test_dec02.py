import unittest

from december02 import Solver


class TestDec2(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertEqual(Solver.present_area(2, 3, 4), 58)
        self.assertEqual(Solver.present_area(1, 1, 10), 43)

    def test_examples_for_part_two(self):
        self.assertEqual(Solver.ribbon_len(2, 3, 4), 34)
        self.assertEqual(Solver.ribbon_len(1, 1, 10), 14)

    def test_solution(self):
        (paper, ribbon) = Solver(from_file='input/dec02.in').solve()
        self.assertEqual(paper, 1598415)
        self.assertEqual(ribbon, 3812909)


if __name__ == '__main__':
    unittest.main()
