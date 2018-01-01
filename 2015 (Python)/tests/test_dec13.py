import unittest

from december13 import Solver


class TestDec13(unittest.TestCase):

    def test_examples_for_part_one(self):
        s = Solver(from_file='input/dec13-sample.in')
        self.assertEqual(s.solve_part_one(), 330)

    def test_solution(self):
        s = Solver(from_file='input/dec13.in')
        (one, two) = s.solve()
        self.assertEqual(one, 664)
        self.assertEqual(two, 640)


if __name__ == '__main__':
    unittest.main()
