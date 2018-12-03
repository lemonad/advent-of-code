"""
Unit tests for December 08, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

import numpy as np

from december08 import Solver


class TestDecember08(unittest.TestCase):
    def test_operations(self):
        s = Solver(rows=3, cols=7, from_str="...")
        s.operate("rect 3x2")
        s.operate("rotate column x=1 by 1")
        s.operate("rotate row y=0 by 4")
        s.operate("rotate column x=1 by 1")
        ref = np.array(
            [
                [False, True, False, False, True, False, True],
                [True, False, True, False, False, False, False],
                [False, True, False, False, False, False, False],
            ],
            dtype="bool",
        )
        self.assertTrue(np.array_equal(ref, s.screen))

    def test_solution(self):
        one = Solver(from_file="input/december08.input").solve()
        self.assertEqual(one, 123)


if __name__ == "__main__":
    unittest.main()
