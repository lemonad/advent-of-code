"""
Unit tests for December 04, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december04 import Solver


class TestDecember04(unittest.TestCase):
    def test_sum_of_natural_numbers(self):
        s = Solver(
            from_str="aaaaa-bbb-z-y-x-123[abxyz]\n"
            "a-b-c-d-e-f-g-h-987[abcde]\n"
            "not-a-real-room-404[oarel]\n"
            "totally-real-room-200[decoy]"
        )
        self.assertEqual(s.solve_part_one(), 1514)

    def test_solution(self):
        (one, two) = Solver(from_file="input/december04.input").solve()
        self.assertEqual(one, 245102)
        self.assertEqual(two, 324)


if __name__ == "__main__":
    unittest.main()
