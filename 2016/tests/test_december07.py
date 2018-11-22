"""
Unit tests for December 07, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december07 import Solver


class TestDecember07(unittest.TestCase):
    def test_ip_tls(self):
        one = Solver(from_str="abba[mnop]qrst").solve_part_one()
        self.assertEqual(one, 1)
        one = Solver(from_str="abcd[bddb]xyyx").solve_part_one()
        self.assertEqual(one, 0)
        one = Solver(from_str="aaaa[qwer]tyui").solve_part_one()
        self.assertEqual(one, 0)
        one = Solver(from_str="ioxxoj[asdfgh]zxcvbn").solve_part_one()
        self.assertEqual(one, 1)

    def test_ip_ssl(self):
        two = Solver(from_str="aba[bab]xyz").solve_part_two()
        self.assertEqual(two, 1)
        two = Solver(from_str="xyx[xyx]xyx").solve_part_two()
        self.assertEqual(two, 0)
        two = Solver(from_str="aaa[kek]eke").solve_part_two()
        self.assertEqual(two, 1)
        two = Solver(from_str="zazbz[bzb]cdb").solve_part_two()
        self.assertEqual(two, 1)

    def test_solution(self):
        (one, two) = Solver(from_file="input/december07.input").solve()
        self.assertEqual(one, 105)
        self.assertEqual(two, 258)


if __name__ == "__main__":
    unittest.main()
