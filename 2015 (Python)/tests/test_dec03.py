import unittest

from december03 import Solver


class TestDec3(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertEqual(Solver.santa_deliveries('>'), 2)
        self.assertEqual(Solver.santa_deliveries('^>v<'), 4)
        self.assertEqual(Solver.santa_deliveries('^v^v^v^v^v'), 2)

    def test_examples_for_part_two(self):
        self.assertEqual(Solver.robo_santa_deliveries('^v'), 3)
        self.assertEqual(Solver.robo_santa_deliveries('^>v<'), 3)
        self.assertEqual(Solver.robo_santa_deliveries('^v^v^v^v^v'), 11)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec03.in').solve()
        self.assertEqual(one, 2081)
        self.assertEqual(two, 2341)


if __name__ == '__main__':
    unittest.main()
