import unittest

from december05 import Solver


class TestDec5(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertTrue(Solver.is_nice_string_one('ugknbfddgicrmopn'))
        self.assertTrue(Solver.is_nice_string_one('aaa'))
        self.assertFalse(Solver.is_nice_string_one('jchzalrnumimnmhp'))
        self.assertFalse(Solver.is_nice_string_one('haegwjzuvuyypxyu'))
        self.assertFalse(Solver.is_nice_string_one('dvszwmarrgswjxmb'))

    def test_examples_for_part_two(self):
        self.assertTrue(Solver.is_nice_string_two('qjhvhtzxzqqjkmpb'))
        self.assertTrue(Solver.is_nice_string_two('xxyxx'))
        self.assertFalse(Solver.is_nice_string_two('uurcxstgmygtbstg'))
        self.assertFalse(Solver.is_nice_string_two('ieodomkazucvgmuy'))

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec05.in').solve()
        self.assertEqual(one, 238)
        self.assertEqual(two, 69)


if __name__ == '__main__':
    unittest.main()
