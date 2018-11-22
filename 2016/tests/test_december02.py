"""
Unit tests for December 2, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december02 import Solver


class TestDecember02(unittest.TestCase):
    def test_bathroom_code(self):
        one = Solver(from_str="ULL\nRRDDD\nLURDL\nUUUUD").solve_part_one()
        self.assertEqual(one, "1985")

    def test_fancy_bathroom_code(self):
        two = Solver(from_str="ULL\nRRDDD\nLURDL\nUUUUD").solve_part_two()
        self.assertEqual(two, "5DB3")

    def test_solution(self):
        (one, two) = Solver(from_file="input/december02.input").solve()
        self.assertEqual(one, "52981")
        self.assertEqual(two, "74CD2")


if __name__ == "__main__":
    unittest.main()
