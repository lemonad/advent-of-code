"""
Unit tests for December 12, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december12 import Solver


class TestDecember12(unittest.TestCase):

    def test_example(self):
        test_input = """
            cpy 41 a
            inc a
            inc a
            dec a
            jnz a 2
            dec a
            """
        s = Solver(from_str=test_input)
        self.assertEqual(s.solve_part_one(), 42)

    def test_solution(self):
        (one, two) = Solver(from_file='input/december12.input').solve()
        self.assertEqual(one, 318117)
        self.assertEqual(two, 9227771)


if __name__ == "__main__":
    unittest.main()
