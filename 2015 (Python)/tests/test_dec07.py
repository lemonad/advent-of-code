import unittest

from december07 import Solver


class TestDec7(unittest.TestCase):

    def test_examples_for_part_one(self):
        s = Solver(from_file='input/dec07-sample.in')
        s.step()
        self.assertEqual(s.wires['d'], 72)
        self.assertEqual(s.wires['e'], 507)
        self.assertEqual(s.wires['f'], 492)
        self.assertEqual(s.wires['g'], 114)
        self.assertEqual(s.wires['h'], 65412)
        self.assertEqual(s.wires['i'], 65079)
        self.assertEqual(s.wires['x'], 123)
        self.assertEqual(s.wires['y'], 456)

    def test_solution(self):
        (one, two) = Solver(from_file='input/dec07.in').solve()
        self.assertEqual(one, 16076)
        self.assertEqual(two, 2797)


if __name__ == '__main__':
    unittest.main()
