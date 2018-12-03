"""
December 06, Advent of Code 2016 (Jonas Nockert / @lemonad)

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

    def get_repetition_code(self, method):
        C = self.as_char_numpy_array()
        (_, n_cols) = np.shape(C)
        message = ""
        for n in range(n_cols):
            unique, counts = np.unique(C[:, n], return_counts=True)
            max_index = method(counts)
            message += unique[max_index].decode("utf-8")
        return message

    def solve_part_one(self):
        """Solution for part one."""
        return self.get_repetition_code(np.argmax)

    def solve_part_two(self):
        """Solution for part two."""
        return self.get_repetition_code(np.argmin)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december06.input")
    (one, two) = s.solve()
    print("Repetition code: {:s}".format(one))
    print("Modified repetition code: {:s}".format(two))
