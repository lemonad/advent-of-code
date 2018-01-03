import unittest

from december18 import Solver


class TestDec18(unittest.TestCase):

    def test_examples_for_part_one(self):
        one = Solver(from_file='input/dec18-sample.in').solve(4)
        self.assertEqual(one, 4)

    def test_examples_for_part_two(self):
        two = Solver(from_file='input/dec18-sample.in').solve(
                5, stuck_pixels=True)
        self.assertEqual(two, 17)

    def test_solution(self):
        # Too slow.
        pass


if __name__ == '__main__':
    unittest.main()
