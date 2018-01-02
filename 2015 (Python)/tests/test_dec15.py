import unittest

from december15 import Solver


class TestDec15(unittest.TestCase):

    def test_examples(self):
        (one, two) = Solver(from_file='input/dec15-sample.in').solve()
        self.assertEqual(one, 62842880)
        self.assertEqual(two, 57600000)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec15.in').solve()
        self.assertEqual(one, 13882464)
        self.assertEqual(two, 11171160)


if __name__ == '__main__':
    unittest.main()
