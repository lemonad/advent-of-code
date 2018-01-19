import unittest

from december24 import Solver


class TestDec24(unittest.TestCase):

    def test_examples(self):
        (one, two) = Solver(from_file='input/dec24-sample.in').solve()
        self.assertEqual(one, 99)
        self.assertEqual(two, 44)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec24.in').solve()
        self.assertEqual(one, 11846773891)
        self.assertEqual(two, 80393059)


if __name__ == '__main__':
    unittest.main()
