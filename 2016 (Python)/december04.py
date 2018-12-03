"""
December 04, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
import math
import operator
import os
import string

import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def get_room_data(room):
        [code, cksum] = room.split("[")
        cksum = cksum[:-1]
        words = code.split("-")
        sector_id = int(words.pop())
        return (words, sector_id, cksum)

    @staticmethod
    def is_real_room(words, cksum):
        letters = sorted("".join(words))
        chars = set(letters)
        d = {}
        for c in chars:
            d[c] = letters.count(c)
        check = sorted(d.items(), key=lambda kv: kv[0])
        check = sorted(check, key=lambda kv: kv[1], reverse=True)
        test_cksum = ""
        for i in range(5):
            test_cksum += check[i][0]
        return test_cksum == cksum

    def solve_part_one(self):
        """Solution for part one."""
        sector_id_sum = 0
        for room in self.lines():
            words, sector_id, cksum = self.get_room_data(room)
            if self.is_real_room(words, cksum):
                sector_id_sum += sector_id

        return sector_id_sum

    def solve_part_two(self):
        """Solution for part two."""
        chars = "abcdefghijklmnopqrstuvwxyz"
        offsets = np.array([ord(x) - ord("a") for x in chars])

        for room in self.lines():
            words, sector_id, cksum = self.get_room_data(room)
            name = " ".join(words)
            re_chars = [chr(x + ord("a")) for x in np.mod(offsets + sector_id, 26)]
            new_name = ""
            for n in name:
                if n.isspace():
                    new_name += " "
                    continue

                o = ord(n) - ord("a")
                new_name += re_chars[o]
            if new_name == "northpole object storage":
                return sector_id

        return None

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december04.input")
    (one, two) = s.solve()
    print("Sum of sector IDs:", one)
    print("Sector id:", two)
