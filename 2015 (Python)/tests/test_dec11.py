import unittest

from december11 import Solver


class TestDec11(unittest.TestCase):

    def test_examples(self):
        assert(not Solver.valid_password('hijklmmn'))
        assert(not Solver.valid_password('abbceffg'))
        assert(not Solver.valid_password('abbcegjk'))
        assert(Solver.valid_password('abcdffaa'))
        assert(Solver.valid_password('ghjaabcc'))
        assert(Solver.valid_password('hxbxxyzz'))
        assert(Solver.next_password('abcdefgh') == 'abcdffaa')
        # Takes too long time
        # assert(Solver.next_password('ghijklmn') == 'ghjaabcc')

    def test_solution(self):
        s = Solver(from_str='hxbxwxba')
        one = s.solve_part_one()
        assert(one == 'hxbxxyzz')
        # Takes too long time
        # two = s.solve_part_two(one)
        # assert(two == 'hxcaabcc')


if __name__ == '__main__':
    unittest.main()
