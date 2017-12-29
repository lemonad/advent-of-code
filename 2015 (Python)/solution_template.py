"""
December _, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def solve_part_one(self):
        """Solution for part one."""
        return None

    def solve_part_two(self):
        """Solution for part two."""
        return None

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec__.in')
    (one, two) = s.solve()
    print("%s." % one)
    print("%s." % two)

    assert(one == 0)
    assert(two == 0)
