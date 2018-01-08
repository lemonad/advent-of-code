import unittest

from december21 import Solver


class TestDec21(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertTrue(Solver.does_player_win_fight(8, 5, 5, 12, 7, 2))

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec21.in').solve()
        self.assertEqual(one, 121)
        self.assertEqual(two, 201)


if __name__ == '__main__':
    unittest.main()
