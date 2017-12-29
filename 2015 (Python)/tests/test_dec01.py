import unittest

from december01 import Solver


class TestDec1(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertEqual(Solver(from_str='(())').solve_part_one(), 0)
        self.assertEqual(Solver(from_str='()()').solve_part_one(), 0)
        self.assertEqual(Solver(from_str='(((').solve_part_one(), 3)
        self.assertEqual(Solver(from_str='(()(()(').solve_part_one(), 3)
        self.assertEqual(Solver(from_str='))(((((').solve_part_one(), 3)
        self.assertEqual(Solver(from_str='())').solve_part_one(), -1)
        self.assertEqual(Solver(from_str='))(').solve_part_one(), -1)
        self.assertEqual(Solver(from_str=')))').solve_part_one(), -3)
        self.assertEqual(Solver(from_str=')())())').solve_part_one(), -3)

    def test_examples_for_part_two(self):
        self.assertEqual(Solver(from_str=')').solve_part_two(), 1)
        self.assertEqual(Solver(from_str='()())').solve_part_two(), 5)

    def test_throws_if_santa_never_enters_basement(self):
        with self.assertRaises(RuntimeError):
            Solver(from_str='(').solve_part_two()

    def test_solution(self):
        (floor, position) = Solver(from_file='input/dec01.in').solve()
        self.assertEqual(floor, 280)
        self.assertEqual(position, 1797)


if __name__ == '__main__':
    unittest.main()
