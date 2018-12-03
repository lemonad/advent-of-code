"""
Unit tests for December 10, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december10 import Solver


class TestDecember10(unittest.TestCase):
    def test_sample(self):
        s = Solver(from_file="input/december10-sample.input")
        s.solve_part_one()
        self.assertEqual(s.outputs[0], 5)
        self.assertEqual(s.outputs[1], 2)
        self.assertEqual(s.outputs[2], 3)

    def test_solution(self):
        (one, two) = Solver(from_file="input/december10.input").solve()
        self.assertEqual(one, 101)
        self.assertEqual(two, 37789)


if __name__ == "__main__":
    unittest.main()
