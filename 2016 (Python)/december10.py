"""
December 10, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
from enum import Enum
import math
import os
import re
import string

import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    class DestType(Enum):
        bot = 1
        output = 2

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)
        self.bots = {}
        self.outputs = {}
        self.rules = {}

    def assign(self, dest_type, dest, value):
        if dest_type == self.DestType.bot:
            if dest in self.bots:
                self.bots[dest].append(value)
            else:
                self.bots[dest] = [value]
        else:
            self.outputs[dest] = value

    def initialize_values_and_rules(self):
        p1 = re.compile(
            r"bot (\d+) gives low to (bot|output) (\d+) and high to "
            "(bot|output) (\d+)"
        )
        p2 = re.compile(r"value (\d+) goes to bot (\d+)")

        for line in self.lines():
            m1 = p1.match(line)
            m2 = p2.match(line)
            if m1:
                bot = int(m1.group(1))
                low_type = (
                    self.DestType.bot if m1.group(2) == "bot" else self.DestType.output
                )
                dest_low = int(m1.group(3))
                high_type = (
                    self.DestType.bot if m1.group(4) == "bot" else self.DestType.output
                )
                dest_high = int(m1.group(5))
                self.rules[bot] = [low_type, dest_low, high_type, dest_high]
            elif m2:
                value = int(m2.group(1))
                bot = int(m2.group(2))
                if bot in self.bots:
                    self.bots[bot].append(value)
                else:
                    self.bots[bot] = [value]
            else:
                print("Error", line)

    def solve_part_one(self):
        """Solution for part one."""
        self.initialize_values_and_rules()
        current_bot = None
        ret = None
        while True:
            for k in self.bots:
                if len(self.bots[k]) == 2:
                    current_bot = k
            if current_bot is None:
                break

            low_type, dest_low, high_type, dest_high = self.rules[current_bot]
            chips = sorted(self.bots[current_bot])
            if chips[0] == 17 and chips[1] == 61:
                ret = current_bot

            del self.bots[current_bot]
            current_bot = None

            self.assign(low_type, dest_low, chips[0])
            self.assign(high_type, dest_high, chips[1])
        return ret

    def solve_part_two(self):
        """Solution for part two."""
        return self.outputs[0] * self.outputs[1] * self.outputs[2]

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december10.input")
    (one, two) = s.solve()
    print(
        "Bot comparing value-61 microchips with value-17 microchips: {:d}".format(one)
    )
    print("Product of first three outputs: {:d}".format(two))
