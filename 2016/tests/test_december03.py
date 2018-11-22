"""
Unit tests for December 03, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december03 import Solver


class TestDecember03(unittest.TestCase):
    def test_valid_triangle(self):
        self.assertFalse(Solver.is_valid([5, 10, 25]))

    def test_no_valid_triangles(self):
        valid_triangles = Solver(from_str="5 10 25").solve_part_one()
        self.assertEqual(valid_triangles, 0)

    def test_solution(self):
        (one, two) = Solver(from_file="input/december03.input").solve()
        self.assertEqual(one, 869)
        self.assertEqual(two, 1544)


if __name__ == "__main__":
    unittest.main()
