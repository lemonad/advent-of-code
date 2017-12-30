import unittest

from december06 import Solver


class TestDec6(unittest.TestCase):

    def test_examples_for_part_one(self):
        on = Solver(from_str='turn on 0,0 through 999,999').solve_part_one()
        self.assertEqual(on, 1000000)
        on = Solver(from_str='toggle 0,0 through 999,0').solve_part_one()
        self.assertEqual(on, 1000)
        on = Solver(from_str='toggle 0,0 through 999,0\n'
                             'toggle 0,0 through 999,0').solve_part_one()
        self.assertEqual(on, 0)
        on = Solver(from_str='turn on 0,0 through 999,999\n'
                             'turn off 499,499 through 500,500').solve_part_one()
        self.assertEqual(on, 1000000 - 4)

    def test_examples_for_part_two(self):
        brightness = Solver(from_str='turn on 0,0 through 0,0').solve_part_two()
        self.assertEqual(brightness, 1)
        brightness = Solver(from_str='toggle 0,0 through 999,999')\
                     .solve_part_two()
        self.assertEqual(brightness, 2000000)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec06.in').solve()
        self.assertEqual(one, 400410)
        self.assertEqual(two, 15343601)


if __name__ == '__main__':
    unittest.main()
