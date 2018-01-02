import unittest

from december16 import Solver


class TestDec16(unittest.TestCase):

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec16.in').solve()
        self.assertEqual(one, 40)
        self.assertEqual(two, 241)


if __name__ == '__main__':
    unittest.main()
