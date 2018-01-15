import unittest

from december23 import Solver


class TestDec23(unittest.TestCase):

    def test_examples_for_part_one(self):
        s = Solver(from_file='input/dec23-sample.in')
        runvm = s.create_function()
        reg_a, reg_b = runvm(0, 0)
        self.assertEqual(reg_a, 2)
        self.assertEqual(reg_b, 0)

    def test_solution(self):
        s = Solver(from_file='input/dec23.in')
        (one, two) = s.solve()
        self.assertEqual(one, 184)
        self.assertEqual(two, 231)


if __name__ == '__main__':
    unittest.main()
