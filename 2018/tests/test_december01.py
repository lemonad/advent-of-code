import unittest

from december01 import Solver


class TestDecember01(unittest.TestCase):
    def test_solution(self):
        (one, two) = Solver(from_file="input/december01.input").solve()
        self.assertEqual(one, 425)
        self.assertEqual(two, 57538)


if __name__ == "__main__":
    unittest.main()
