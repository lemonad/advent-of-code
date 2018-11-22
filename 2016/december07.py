"""
December 07, Advent of Code 2016 (Jonas Nockert / @lemonad)

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
    def check_ababab(ip):
        hypernet_bab = []
        supernet_aba = []

        is_hypernet = False
        for i in range(len(ip) - 2):
            a = ip[i]
            b = ip[i + 1]
            c = ip[i + 2]
            if a == "[":
                is_hypernet = True
            elif a == "]":
                is_hypernet = False
            elif b == "[" or b == "]" or c == "[" or c == "]":
                # Skip "p]p", etc.
                continue
            elif ip[i + 2] == a and a != b:
                if is_hypernet:
                    hypernet_bab.append(a + b + a)
                else:
                    supernet_aba.append(a + b + a)

        for saba in supernet_aba:
            if hypernet_bab.count(saba[1] + saba[0] + saba[1]) > 0:
                return True
        return False

    @staticmethod
    def check_abba(ip):
        is_hypernet = False
        has_abba = False
        for i in range(len(ip) - 3):
            a = ip[i]
            b = ip[i + 1]
            if a == "[":
                is_hypernet = True
                continue
            if a == "]":
                is_hypernet = False
                continue
            if ip[i + 2] == b and ip[i + 3] == a and a != b:
                if is_hypernet:
                    return False
                else:
                    has_abba = True
        return has_abba

    def solve_part_one(self):
        """Solution for part one."""
        abba_counter = 0
        for ip in self.lines():
            if self.check_abba(ip):
                abba_counter += 1
        return abba_counter

    def solve_part_two(self):
        """Solution for part two."""
        aba_counter = 0
        for ip in self.lines():
            if self.check_ababab(ip):
                aba_counter += 1
        return aba_counter

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december07.input")
    (one, two) = s.solve()
    print("Number of IP's supporting TLS: {:d}".format(one))
    print("Number of IP's supporting SSL: {:d}".format(two))
