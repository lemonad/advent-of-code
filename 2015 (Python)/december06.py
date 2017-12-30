"""
December 6, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import numpy as np

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PATTERN = "^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"

    def solve_part_one(self):
        """Solution for part one."""
        im = np.zeros((1000, 1000), dtype=np.bool)
        for m in self.lines_search(self.PATTERN):
            [op, r1x, r1y, r2x, r2y] = m.groups()
            r1y = int(r1y)
            r2y = int(r2y) + 1
            r1x = int(r1x)
            r2x = int(r2x) + 1
            if op == 'turn on':
                im[r1y:r2y, r1x:r2x] = True
            elif op == 'turn off':
                im[r1y:r2y, r1x:r2x] = False
            elif op == 'toggle':
                im[r1y:r2y, r1x:r2x] = ~im[r1y:r2y, r1x:r2x]
            else:
                raise ValueError("Invalid operation: %s" % op)
        return sum(sum(im))

    def solve_part_two(self):
        """Solution for part two."""
        im = np.zeros((1000, 1000), dtype=np.int16)
        for m in self.lines_search(self.PATTERN):
            [op, r1x, r1y, r2x, r2y] = m.groups()
            r1y = int(r1y)
            r2y = int(r2y) + 1
            r1x = int(r1x)
            r2x = int(r2x) + 1
            if op == 'turn on':
                im[r1y:r2y, r1x:r2x] = im[r1y:r2y, r1x:r2x] + 1
            elif op == 'turn off':
                im[r1y:r2y, r1x:r2x] = np.clip(im[r1y:r2y, r1x:r2x] - 1,
                                               0, np.iinfo(np.int16).max)
            elif op == 'toggle':
                im[r1y:r2y, r1x:r2x] = im[r1y:r2y, r1x:r2x] + 2
            else:
                raise ValueError("Invalid operation: %s" % op)
        return sum(sum(im))

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec06.in')
    (one, two) = s.solve()
    print("Number of lights that are lit: %d" % one)
    print("Total brightness of all lights: %d" % two)

    assert(one == 400410)
    assert(two == 15343601)
