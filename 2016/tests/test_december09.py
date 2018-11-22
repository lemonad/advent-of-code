"""
Unit tests for December 09, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december09 import Solver


class TestDecember09(unittest.TestCase):
    def test_compression(self):
        one = Solver(from_str="ADVENT").solve_part_one()
        self.assertEqual(one, 6)
        one = Solver(from_str="A(1x5)BC").solve_part_one()
        self.assertEqual(one, 7)
        one = Solver(from_str="(3x3)XYZ").solve_part_one()
        self.assertEqual(one, 9)
        one = Solver(from_str="A(2x2)BCD(2x2)EFG").solve_part_one()
        self.assertEqual(one, 11)
        one = Solver(from_str="(6x1)(1x3)A").solve_part_one()
        self.assertEqual(one, 6)
        one = Solver(from_str="X(8x2)(3x3)ABCY").solve_part_one()
        self.assertEqual(one, 18)

    def test_improved_compression(self):
        two = Solver(from_str="(3x3)XYZ").solve_part_two()
        self.assertEqual(two, 9)
        two = Solver(from_str="X(8x2)(3x3)ABCY").solve_part_two()
        self.assertEqual(two, 20)
        two = Solver(from_str="(27x12)(20x12)(13x14)(7x10)(1x12)A").solve_part_two()
        self.assertEqual(two, 241920)
        two = Solver(
            from_str="(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
        ).solve_part_two()
        self.assertEqual(two, 445)

    def test_solution(self):
        (one, two) = Solver(from_file="input/december09.input").solve()
        self.assertEqual(one, 152851)
        self.assertEqual(two, 11797310782)


if __name__ == "__main__":
    unittest.main()
