"""
December 4, Advent of Code 2015 (Jonas Nockert / @lemonad)

Part two takes 80 seconds to solve. Maybe there is
some property of md5 that could be used? Seems unlikely.

"""
import hashlib
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    @classmethod
    def leading_hash_zeros(cls, secret_key, num):
        m = hashlib.md5()
        hstr = secret_key + b'%d' % num
        m.update(hstr)
        hexstr = m.hexdigest()
        n_zeros = len(hexstr) - len(hexstr.lstrip('0'))
        return n_zeros

    def solve_part_one(self, n_0=0):
        """Solution for part one."""
        secret_key = self.puzzle_input
        n = n_0
        while self.leading_hash_zeros(secret_key, n) < 5:
            n += 1
        return n

    def solve_part_two(self, n_0=0):
        """Solution for part two."""
        secret_key = self.puzzle_input
        n = n_0
        while self.leading_hash_zeros(secret_key, n) < 6:
            n += 1
        return n

    def solve(self):
        one = self.solve_part_one()
        two = self.solve_part_two(one)
        return (one, two)


if __name__ == '__main__':
    s = Solver(from_str=b'iwrupvqb')
    (one, two) = s.solve()
    print("Advent coin hash (>=5): %d." % one)
    print("Advent coin hash (>=6): %d." % two)

    assert(one == 346386)
    assert(two == 9958218)
