"""
December 18, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import numpy as np

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def subproblem(indata):
        pass

    @staticmethod
    def stuck_corners(m):
        (height, width) = m.shape
        m[0, 0] = True
        m[height - 1, 0] = True
        m[0, width - 1] = True
        m[height - 1, width - 1] = True

    def solve(self, n_iterations=100, stuck_pixels=False):
        """Solution for part one."""
        m = self.as_bool_numpy_array()
        if stuck_pixels:
            self.stuck_corners(m)

        (height, width) = m.shape
        for i in range(n_iterations):
            next_m = np.zeros([height, width], '?')
            if stuck_pixels:
                self.stuck_corners(next_m)

            for h in range(height):
                for w in range(width):
                    n_on = sum(sum(m[max(0, h - 1):min(height, h + 2),
                                     max(0, w - 1):min(width, w + 2)]))
                    if m[h, w]:
                        n_on -= 1
                        if n_on == 2 or n_on == 3:
                            next_m[h, w] = True
                    elif n_on == 3:
                        next_m[h, w] = True
            m = next_m
        return sum(sum(m))


if __name__ == '__main__':
    s = Solver(from_file='input/dec18.in')
    one = s.solve()
    two = s.solve(stuck_pixels=True)
    print("How many lights are on after 100 steps? %d" % one)
    print("how many lights are on after 100 steps with stuck pixels? %d" % two)

    assert(one == 1061)
    assert(two == 1006)
