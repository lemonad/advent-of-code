"""
December 08, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import math
import os
import re
import string

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        if "rows" in kwargs:
            n_rows = kwargs.pop("rows")
        else:
            n_rows = 6
        if "cols" in kwargs:
            n_cols = kwargs.pop("cols")
        else:
            n_cols = 50
        super(Solver, self).__init__(*args, **kwargs)
        self.screen = np.zeros([n_rows, n_cols], dtype="bool")

    def operate(self, command):
        m1 = re.search(r"rect (\d+)x(\d+)", command)
        m2 = re.search(r"rotate row y=(\d+) by (\d+)", command)
        m3 = re.search(r"rotate column x=(\d+) by (\d+)", command)
        if m1:
            w = int(m1.group(1))
            h = int(m1.group(2))
            self.screen[:h, :w] = 1
        elif m2:
            row = int(m2.group(1))
            shift = int(m2.group(2))
            row_pixels = self.screen[row, :]
            new_row = np.concatenate([row_pixels[-shift:], row_pixels[:-shift]])
            self.screen[row, :] = new_row
        elif m3:
            col = int(m3.group(1))
            shift = int(m3.group(2))
            col_pixels = self.screen[:, col]
            new_col = np.concatenate([col_pixels[-shift:], col_pixels[:-shift]])
            # print(new_col)
            self.screen[:, col] = new_col
        else:
            print("Error", command)

    def lit_pixels(self):
        return np.sum(np.sum(self.screen))

    def solve_part_one(self):
        """Solution for part one."""
        for line in self.lines():
            self.operate(line)
        return self.lit_pixels()

    def solve(self):
        return self.solve_part_one()


if __name__ == "__main__":
    s = Solver(from_file="input/december08.input")
    one = s.solve()
    print("Number of lit pixels: {:d}".format(one))
    plt.imshow(s.screen)
    plt.title("Solution to part two")
    plt.show()
