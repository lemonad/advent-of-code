import unittest

from december04 import Solver


class TestDec4(unittest.TestCase):

    def test_examples(self):
        self.assertLess(Solver.leading_hash_zeros(b'abcdef', 609042), 5)
        lz = Solver.leading_hash_zeros(b'abcdef', 609043)
        self.assertGreaterEqual(lz, 5)

        self.assertLess(Solver.leading_hash_zeros(b'pqrstuv', 1048969), 5)
        lz = Solver.leading_hash_zeros(b'pqrstuv', 1048970)
        self.assertGreaterEqual(lz, 5)

    def test_solution(self):
        # Part two takes too long time to solve.
        one = Solver(from_str=b'iwrupvqb').solve_part_one()
        self.assertEqual(one, 346386)


if __name__ == '__main__':
    unittest.main()
