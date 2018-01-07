import unittest

from december19 import Solver


class TestDec19(unittest.TestCase):

    def test_examples_for_part_one(self):
        one = Solver(from_file='input/dec19-sample.in').solve_part_one()
        self.assertEqual(one, 4)

    def test_examples_for_part_two(self):
        two = Solver(from_file='input/dec19-sample2.in').solve_part_two()
        self.assertEqual(two, 6)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec19.in').solve()
        self.assertEqual(one, 518)
        self.assertEqual(two, 200)


if __name__ == '__main__':
    unittest.main()
