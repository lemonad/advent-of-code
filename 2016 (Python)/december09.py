"""
December 09, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import math
import os
import re
import string

import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def decomp(s, recurse=False):
        decomp_len = 0
        i = 0
        while i < len(s):
            if s[i] == "(":
                m = re.match(r"(\d+)x(\d+)\)", s[(i + 1) :])
                # Skip over marker (+1 is the initial parenthesis).
                i += len(m.group(0)) + 1
                replen = int(m.group(1))
                reps = int(m.group(2))
                if recurse:
                    total = Solver.decomp(s[i : i + replen], recurse)
                    decomp_len += total * reps
                else:
                    decomp_len += replen * reps
                # Skip over the decompressed section.
                i += replen
            else:
                decomp_len += 1
                i += 1
        return decomp_len

    def solve_part_one(self):
        """Solution for part one."""
        return self.decomp(self.puzzle_input)

    def solve_part_two(self):
        """Solution for part two."""
        return self.decomp(self.puzzle_input, recurse=True)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december09.input")
    (one, two) = s.solve()
    print("Decompressed length: {:d}".format(one))
    print("Improved decompression length: {:d}".format(two))
