import unittest

from december09 import Solver


class TestDec9(unittest.TestCase):

    def test_examples(self):
        s = Solver(from_file='input/dec09-sample.in')
        (one, two) = s.solve()
        self.assertEqual(one, 605)
        self.assertEqual(two, 982)

    def test_solution(self):
        s = Solver(from_file='input/dec09.in')
        (one, two) = s.solve()
        self.assertEqual(one, 251)
        self.assertEqual(two, 898)


if __name__ == '__main__':
    unittest.main()
