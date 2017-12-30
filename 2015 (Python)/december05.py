"""
December 5, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import re

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    @classmethod
    def is_nice_string_one(cls, naughty_or_nice_string):
        # A string is nice if
        # (1) it contains at least three vowels (aeiou only),
        p1 = sum([naughty_or_nice_string.count(x) for x in 'aeiou']) >= 3
        # (2) it contains at least one letter that appears twice in a row,
        p2 = re.search('([a-z])\\1', naughty_or_nice_string) is not None
        # (3) it does not contain the strings ab, cd, pq, or xy.
        p3 = [x in naughty_or_nice_string
              for x in ['ab', 'cd', 'pq', 'xy']].count(True) == 0
        return p1 and p2 and p3

    def solve_part_one(self):
        """Solution for part one."""
        return [self.is_nice_string_one(x) for x in self.lines()].count(True)

    @classmethod
    def is_nice_string_two(cls, naughty_or_nice_string):
        # A string is nice if
        # (1) It contains a pair of any two letters that appears at least
        #     twice in the string without overlapping
        p1 = re.search('([a-z]{2}).*\\1', naughty_or_nice_string) is not None
        # (2) It contains at least one letter which repeats with exactly one
        #     letter between them
        p2 = re.search('([a-z]).\\1', naughty_or_nice_string) is not None
        return p1 and p2

    def solve_part_two(self):
        """Solution for part two."""
        return [self.is_nice_string_two(x) for x in self.lines()].count(True)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec05.in')
    (one, two) = s.solve()
    print("Number of nice strings (1): %d" % one)
    print("Number of nice strings (2): %d" % two)

    assert(one == 238)
    assert(two == 69)
