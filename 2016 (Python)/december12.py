"""
December 12, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
from enum import Enum
import math
import os
import re
import string

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    def run(self, r):
        ip = 0
        ops = []
        operands = []
        for op, args in list(self.as_instructions(separator=' ')):
            ops.append(op)
            operands.append(args)

        while ip < len(ops):
            op = ops[ip]
            args = operands[ip]
            reg1 = None
            reg2 = None
            val1 = None
            val2 = None
            if args[0].isalpha():
                reg1 = ord(args[0]) - ord('a')
            else:
                val1 = int(args[0])

            if len(args) > 1:
                if args[1].isalpha():
                    reg2 = ord(args[1]) - ord('a')
                else:
                    val2 = int(args[1])

            if op == 'cpy':
                if reg1 is not None and reg2 is not None:
                    r[reg2] = r[reg1]
                elif reg1 is not None:
                    raise ValueError("copy from reg to val is not allowed")
                elif reg2 is not None:
                    r[reg2] = val1
                else:
                    raise ValueError("copy from val to val is not allowed")
            elif op == 'jnz':
                if reg2 is not None:
                    raise ValueError("second operand of jnz must be a value")
                if reg1 is not None:
                    if r[reg1] != 0:
                        ip += val2 - 1
                elif val1 != 0:
                    ip += val2 - 1
            elif op == 'inc':
                if reg1 is None:
                    raise ValueError("cannot increase val")
                r[reg1] += 1
            elif op == 'dec':
                if reg1 is None:
                    raise ValueError("cannot decrease val")
                r[reg1] -= 1
            ip += 1
        return r

    def solve_part_one(self):
        """Solution for part one."""
        r = self.run([0] * 4)
        return r[0]

    def solve_part_two(self):
        """Solution for part two."""
        r = self.run([0, 0, 1, 0])
        return r[0]

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december12.input")
    (one, two) = s.solve()
    print("Value left in register a (part 1):", one)
    print("Value left in register b (part 1):", two)
