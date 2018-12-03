"""
December 03, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def is_valid(maybe_triangle):
        x = sorted(maybe_triangle)
        return x[2] < x[0] + x[1]

    def solve_part_one(self):
        """Solution for part one."""
        valid = 0
        for s in self.lines_split(None, int):
            if self.is_valid(s):
                valid += 1
        return valid

    def solve_part_two(self):
        """Solution for part two."""
        valid = 0
        data = []
        for s in self.lines_split(None, int):
            data.append([s[0], s[1], s[2]])

        for i in range(0, len(data), 3):
            for j in range(3):
                if self.is_valid([data[i + 0][j], data[i + 1][j], data[i + 2][j]]):
                    valid += 1
        return valid

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == "__main__":
    s = Solver(from_file="input/december03.input")
    (one, two) = s.solve()
    print("Valid triangles (columns): {:d}".format(one))
    print("Valid triangles (rows): {:d}".format(two))
