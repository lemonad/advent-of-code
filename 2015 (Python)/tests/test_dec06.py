import unittest

from december06 import Solver


class TestDec6(unittest.TestCase):

    def test_examples_for_part_one(self):
        s = 'turn on 0,0 through 999,999'
        self.assertEqual(Solver(from_str=s).solve_part_one(), 1000000)

        s = 'toggle 0,0 through 999,0'
        self.assertEqual(Solver(from_str=s).solve_part_one(), 1000)

        s = 'toggle 0,0 through 999,0\ntoggle 0,0 through 999,0'
        self.assertEqual(Solver(from_str=s).solve_part_one(), 0)

        s = 'turn on 0,0 through 999,999\nturn off 499,499 through 500,500'
        self.assertEqual(Solver(from_str=s).solve_part_one(), 1000000 - 4)

    def test_examples_for_part_two(self):
        s = 'turn on 0,0 through 0,0'
        self.assertEqual(Solver(from_str=s).solve_part_two(), 1)

        s = 'toggle 0,0 through 999,999'
        self.assertEqual(Solver(from_str=s).solve_part_two(), 2000000)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec06.in').solve()
        self.assertEqual(one, 400410)
        self.assertEqual(two, 15343601)


if __name__ == '__main__':
    unittest.main()
