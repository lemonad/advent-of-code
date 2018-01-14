import unittest

from december22 import BossState, PlayerState, Solver


class TestDec22(unittest.TestCase):

    def test_examples_for_part_one(self):
        s = Solver(from_file='input/dec22.in')
        player = PlayerState(10, 250)
        boss = BossState(13, 8)
        self.assertLess(s.does_player_win_fight(player, boss), s.LARGE_SPENT)

        s = Solver(from_file='input/dec22.in')
        player = PlayerState(10, 250)
        boss = BossState(14, 8)
        self.assertLess(s.does_player_win_fight(player, boss), s.LARGE_SPENT)

    def test_solution(self):
        s = Solver(from_file='input/dec22.in')
        one = s.solve()

        # Solver is relying on class attributes during recursion so
        # we need to instantiate new solver.
        s = Solver(from_file='input/dec22.in', level='hard')
        two = s.solve()

        self.assertEqual(one, 953)
        self.assertEqual(two, 1289)


if __name__ == '__main__':
    unittest.main()
