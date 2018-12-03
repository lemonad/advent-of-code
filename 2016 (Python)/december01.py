"""
December 01, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import math
import os
import string

import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)
        self.reset()

    def reset(self):
        self.pos = np.array([0, 0])
        self.dir = np.array([0, 1])
        self.visited = {(0, 0): True}
        self.check_visited = False

    def update(self, move_str):
        move_len = int(move_str[1:])

        x = self.dir[0]
        if move_str[0] == "L":
            self.dir[0] = -self.dir[1]
            self.dir[1] = x
        else:
            self.dir[0] = self.dir[1]
            self.dir[1] = -x

        for i in range(move_len):
            self.pos += self.dir
            if self.check_visited:
                t = (self.pos[0], self.pos[1])
                if t in self.visited:
                    return True
                self.visited[t] = True
        return False

    def dist(self):
        return int(np.linalg.norm(self.pos, ord=1))

    def solve_part_one(self):
        """Solution for part one."""
        self.reset()
        for d in self.as_list():
            self.update(d)
        return self.dist()

    def solve_part_two(self):
        """Solution for part two."""
        self.reset()
        self.check_visited = True
        for d in self.as_list():
            if self.update(d):
                break
        return self.dist()

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december01.input")
    (one, two) = s.solve()
    print("Distance to Easter Bunny HQ: {:d}".format(one))
    print("Distance to twice visited block: {:d}".format(two))
