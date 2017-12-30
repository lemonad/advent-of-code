import unittest

from december08 import Solver


class TestDec8(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertEqual(len(Solver.decode('""')), 0)
        self.assertEqual(len(Solver.decode('"abc"')), 3)
        self.assertEqual(len(Solver.decode('"aaa\\"aaa"')), 7)
        self.assertEqual(len(Solver.decode('"aaa\\\\aaa"')), 7)
        self.assertEqual(len(Solver.decode('"\\x27"')), 1)
        s = Solver(from_file='input/dec08-sample.in')
        assert(s.solve_part_one() == 12)

    def test_examples_for_part_two(self):
        self.assertEqual(Solver.encode('""'), '"\\"\\""')
        self.assertEqual(Solver.encode('"abc"'), '"\\"abc\\""')
        self.assertEqual(Solver.encode('"aaa\\"aaa"'),
                         '"\\"aaa\\\\\\"aaa\\""')
        self.assertEqual(Solver.encode('"\\x27"'), '"\\"\\\\x27\\""')
        self.assertEqual(len(Solver.encode('""')), 6)
        self.assertEqual(len(Solver.encode('"abc"')), 9)
        self.assertEqual(len(Solver.encode('"aaa\\"aaa"')), 16)
        self.assertEqual(len(Solver.encode('"\\x27"')), 11)
        s = Solver(from_file='input/dec08-sample.in')
        assert(s.solve_part_two() == 19)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec08.in').solve()
        self.assertEqual(one, 1350)
        self.assertEqual(two, 2085)


if __name__ == '__main__':
    unittest.main()
