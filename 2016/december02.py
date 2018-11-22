"""
December 02, Advent of Code 2016 (Jonas Nockert / @lemonad)

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

    @staticmethod
    def subproblem(indata):
        pass

    def solve_part_one(self):
        """Solution for part one."""
        board = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        pos = (1, 1)

        code = ""
        for line in self.lines():
            for c in line:
                if c == 'U':
                    pos = (pos[0], max(pos[1] - 1, 0))
                elif c == 'D':
                    pos = (pos[0], min(pos[1] + 1, 2))
                elif c == 'L':
                    pos = (max(pos[0] - 1, 0), pos[1])
                else:
                    pos = (min(pos[0] + 1, 2), pos[1])
            code = code + str(board[pos[1], pos[0]])
        return code

    def solve_part_two(self):
        """Solution for part two."""
        board = np.array([[0, 0, '1', 0, 0],
                          [0, '2', '3', '4', 0],
                          ['5', '6', '7', '8', '9'],
                          [0, 'A', 'B', 'C', 0],
                          [0, 0, 'D', 0, 0]])
        pos = (0, 2)

        code = ""
        for line in self.lines():
            for c in line:
                if c == 'U':
                    if pos[1] > 0 and board[pos[1] - 1, pos[0]] != '0':
                        pos = (pos[0], pos[1] - 1)
                elif c == 'D':
                    if pos[1] < 4 and board[pos[1] + 1, pos[0]] != '0':
                        pos = (pos[0], pos[1] + 1)
                elif c == 'L':
                    if pos[0] > 0 and board[pos[1], pos[0] - 1] != '0':
                        pos = (pos[0] - 1, pos[1])
                else:
                    if pos[0] < 4 and board[pos[1], pos[0] + 1] != '0':
                        pos = (pos[0] + 1, pos[1])
            code = code + str(board[pos[1], pos[0]])
        return code

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    # assert(Solver.subproblem('') == 0)

    s = Solver(from_str='ULL\nRRDDD\nLURDL\nUUUUD')
    assert(s.solve_part_one() == "1985")
    s = Solver(from_str='ULL\nRRDDD\nLURDL\nUUUUD')
    assert(s.solve_part_two() == "5DB3")

    s = Solver(from_file='input/december02.input')
    (one, two) = s.solve()
    assert(one == "52981")
    assert(two == "74CD2")

    print("Code part 1:", one)
    print("Code part 2:", two)
