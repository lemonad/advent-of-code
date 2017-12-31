import unittest

from december10 import Solver


class TestDec10(unittest.TestCase):

    def test_examples(self):
        self.assertEqual(Solver.elves_look_elves_say('1'), '11')
        self.assertEqual(Solver.elves_look_elves_say('11'), '21')
        self.assertEqual(Solver.elves_look_elves_say('21'), '1211')
        self.assertEqual(Solver.elves_look_elves_say('1211'), '111221')
        self.assertEqual(Solver.elves_look_elves_say('111221'), '312211')

    def test_solution(self):
        # Part two takes too long time to calculate.
        self.assertEqual(Solver(from_str='1113222113').solve_part_one(),
                         252594)


if __name__ == '__main__':
    unittest.main()
