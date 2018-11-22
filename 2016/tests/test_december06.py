"""
Unit tests for December 06, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december06 import Solver


class TestDecember06(unittest.TestCase):
    def test_error_corrected_version(self):
        (one, two) = Solver(from_file="input/december06-sample.input").solve()
        self.assertEqual(one, "easter")
        self.assertEqual(two, "advent")

    def test_solution(self):
        (one, two) = Solver(from_file="input/december06.input").solve()
        self.assertEqual(one, "tkspfjcc")
        self.assertEqual(two, "xrlmbypn")


if __name__ == "__main__":
    unittest.main()
