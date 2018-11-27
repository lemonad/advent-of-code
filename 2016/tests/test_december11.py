"""
Unit tests for December 11, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import unittest

from december11 import Solver


class TestDecember11(unittest.TestCase):

    def test_check_states(self):
        s = Solver(from_str='...')
        cs = s.get_check_state((1, [1 << 16 | 1 << 17, 1 << 0, 1 << 1, 0]))
        hs = "1" + "00030000" + "00000001" + "00000002" + "00000000"
        self.assertEqual(s.hash_state(cs), hs)
        cs = s.get_check_state((1, [1 << 18 | 1 << 19, 1 << 2, 1 << 3, 0]))
        self.assertEqual(s.hash_state(cs), hs)

        cs = s.get_check_state((1, [1 << 0, 1 << 16, 1 << 1 | 1 << 17, 0]))
        hs = "1" + "00000001" + "00010000" + "00020002" + "00000000"
        self.assertEqual(s.hash_state(cs), hs)
        cs = s.get_check_state((1, [ 1 << 1, 1 << 17, 1 << 0 | 1 << 16, 0]))
        self.assertEqual(s.hash_state(cs), hs)

    def test_example(self):
        # 4
        # 3          LG
        # 2    HG
        # 1 E     HM    LM
        #      0  16  1 17
        test_data = [
                1 << 16 | 1 << 17,
                1 << 0,
                1 << 1,
                0]
        s = Solver(from_str='...')
        self.assertEqual(s.explore(test_data), 11)

    def test_part_one(self):
        # 4
        # 3                     XG XM RG RM
        # 2            PM    SM
        # 1 E TG TM PG    SG
        #      0 16  1 17  2 18  3 19  4 20
        part1_data = [
                1 << 0 | 1 << 1 | 1 << 2 | 1 << 16,
                1 << 17 | 1 << 18,
                1 << 3 | 1 << 4 | 1 << 19 | 1 << 20,
                0]
        s = Solver(from_str='...')
        self.assertEqual(s.explore(part1_data), 31)

    def test_part_two(self):
        # 4
        # 3                     XG XM RG RM
        # 2            PM    SM
        # 1 E TG TM PG    SG                EG EM DG DM
        #      0 16  1 17  2 18  3 19  4 20  5 21  6 22
        part2_data = [
                1 << 0 | 1 << 1 | 1 << 2 | 1 << 5 | 1 << 6 | 1 << 16 | 1 << 21 | 1 << 22,
                1 << 17 | 1 << 18,
                1 << 3 | 1 << 4 | 1 << 19 | 1 << 20,
                0]
        s = Solver(from_str='...')
        self.assertEqual(s.explore(part2_data), 55)


if __name__ == "__main__":
    unittest.main()
