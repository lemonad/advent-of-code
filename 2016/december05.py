"""
December 05, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import hashlib
import math
import os
import string

import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    def find_next_hash(self, start_index):
        index = start_index
        while True:
            key = "{:s}{:d}".format(self.puzzle_input, index).encode('utf-8')
            s = hashlib.md5(key).hexdigest()
            if s[0:5] == "00000":
                return (s, index)
            index += 1

    def solve_part_one(self):
        """Solution for part one."""
        password = ""
        index = 0
        while len(password) < 8:
            (s, found_index) = self.find_next_hash(index)
            password += s[5]
            index = found_index + 1
        return password

    def solve_part_two(self):
        """Solution for part two."""
        password = list("XXXXXXXX")
        index = 0
        counter = 0
        while counter < 8:
            (s, found_index) = self.find_next_hash(index)
            index = found_index + 1
            offset = ord(s[5]) - ord('0')
            # Offset invalid or password character already set previously?
            if offset >= 8 or password[offset] != 'X':
                continue
            password[offset] = s[6]
            counter += 1
        return "".join(password)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


def main(input_data):
    s = Solver(from_str='abc')
    assert(s.solve_part_one() == "18f47a30")
    s = Solver(from_str='abc')
    assert(s.solve_part_two() == "05ace8e3")

    s = Solver(from_str=input_data)
    (one, two) = s.solve()
    assert(one == "f97c354d")
    assert(two == "863dde27")

    print("Password: {:s}".format(one))
    print("Password (new method): {:s}".format(two))


if __name__ == '__main__':
    input_data = """
reyedfim
    """.strip()
    main(input_data)
