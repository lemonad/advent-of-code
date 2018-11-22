import unittest

from december01 import Solver


class TestDecember07(unittest.TestCase):

    def r2_l3_leaves_you_2_blocks_east_and_3_blocks_north(self):
        s = Solver(from_str='R2, L3')
        s.solve_part_one()
        self.assertEqual(s.pos[0], 2)
        self.assertEqual(s.pos[1], 3)
        self.assertEqual(s.dist() == 5)

    def r2_r2_r2_leaves_you_2_blocks_due_south_of_your_starting_position(self):
        s = Solver(from_str='R2, R2, R2')
        s.solve_part_one()
        self.assertEqual(s.pos[0], 0)
        self.assertEqual(s.pos[1], -2)
        self.assertEqual(s.dist() == 2)

    def r5_l5_r5_r3_leaves_you_12_blocks_away(self):
        s = Solver(from_str='R5, L5, R5, R3')
        s.solve_part_one()
        self.assertEqual(s.dist() == 12)

    def r8_r4_r4_r8_the_first_location_you_visit_twice_is_4_blocks_away(self):
        s = Solver(from_str='R8, R4, R4, R8')
        s.solve_part_two()
        self.assertEqual(s.pos[0], 4)
        self.assertEqual(s.pos[1], 0)
        self.assertEqual(s.dist() == 4)

    def test_solution(self):
        (one, two) = Solver(from_file='input/december01.input').solve()
        self.assertEqual(one, 332)
        self.assertEqual(two, 166)


if __name__ == '__main__':
    unittest.main()
