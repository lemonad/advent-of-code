"""
Unit tests for December 05, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december05 import Solver


class TestDecember05(unittest.TestCase):
    def test_valid_password(self):
        (one, two) = Solver(from_str="abc").solve()
        self.assertEqual(one, "18f47a30")
        self.assertEqual(two, "05ace8e3")

    def test_solution(self):
        s = Solver(from_str="reyedfim")
        (one, two) = s.solve()
        self.assertEqual(one, "f97c354d")
        self.assertEqual(two, "863dde27")


if __name__ == "__main__":
    unittest.main()
