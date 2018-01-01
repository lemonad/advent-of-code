import unittest

from december14 import Solver


class TestDec14(unittest.TestCase):

    def test_examples(self):
        s = Solver(from_file='input/dec14-sample.in')
        (one, two) = s.solve(1000)
        self.assertEqual(one, 1120)
        self.assertEqual(two, 689)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec14.in').solve(2503)
        self.assertEqual(one, 2655)
        self.assertEqual(two, 1059)


if __name__ == '__main__':
    unittest.main()
