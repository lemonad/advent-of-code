"""
December 01, Advent of Code 2018 (Jonas Nockert / @lemonad)

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

    def solve_part_one(self):
        """Solution for part one."""
        freq = 0
        for x in self.lines():
            delta = int(x[1:])
            freq += delta if x[0] == "+" else -delta
        return freq

    def solve_part_two(self):
        """Solution for part two."""
        freq = 0
        freqs = {0: True}
        found = False
        while True:
            for x in self.lines():
                delta = int(x[1:])
                freq += delta if x[0] == "+" else -delta
                if freq in freqs:
                    found = True
                    break
                freqs[freq] = True
            if found:
                break
        return freq

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december01.input")
    (one, two) = s.solve()
    print("Resulting frequency: {:d}".format(one))
    print("First frequency reached first: {:d}".format(two))
