import unittest

from december17 import Solver


class TestDec17(unittest.TestCase):

    def test_examples(self):
        (one, two) = Solver(from_file='input/dec17-sample.in').solve(25)
        self.assertEqual(one, 4)
        self.assertEqual(two, 3)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec17.in').solve(150)
        self.assertEqual(one, 4372)
        self.assertEqual(two, 4)


if __name__ == '__main__':
    unittest.main()
