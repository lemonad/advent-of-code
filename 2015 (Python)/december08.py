"""
December 8, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import re

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    @staticmethod
    def decode(line):
        line = line[1:-1]
        line = re.sub('\\\\\\\\', '_', line)
        line = re.sub('\\\\"', '"', line)
        return re.sub('\\\\x..', '_', line)

    @staticmethod
    def encode(line):
        line = re.sub('\\\\', '\\\\\\\\', line)
        line = re.sub('"', '\\\\"', line)
        return '"' + line + '"'

    @staticmethod
    def space_delta_decoded(line):
        line = line.strip()
        return len(line) - len(Solver.decode(line))

    @staticmethod
    def space_delta_encoded(line):
        line = line.strip()
        return len(Solver.encode(line)) - len(line)

    def solve_part_one(self):
        """Solution for part one."""
        total = 0
        for line in self.lines():
            total += self.space_delta_decoded(line)
        return total

    def solve_part_two(self):
        """Solution for part two."""
        total = 0
        for line in self.lines():
            total += self.space_delta_encoded(line)
        return total

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec08.in')
    (one, two) = s.solve()
    print("len - decoded_len = %d" % one)
    print("encoded_len - len = %d" % two)

    assert(one == 1350)
    assert(two == 2085)
