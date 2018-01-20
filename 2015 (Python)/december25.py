"""
December 25, Advent of Code 2015 (Jonas Nockert / @lemonad)

Note that there was only one part to this puzzle.

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    @staticmethod
    def sum_of_natural_numbers(n):
        if n <= 0:
            return 0
        return int(n * (n + 1) / 2)

    @staticmethod
    def code_no_for_row_col(row, col):
        # Elements of first row is just sum of natural numbers 1 to col.
        first_row = Solver.sum_of_natural_numbers(col)
        colsum = (Solver.sum_of_natural_numbers(row + col - 2) -
                  Solver.sum_of_natural_numbers(col - 1))
        return first_row + colsum

    @staticmethod
    def code_for_row_col(row, col):
        code_no = Solver.code_no_for_row_col(row, col)
        first = 20151125
        multiplier = 252533
        divisor = 33554393

        code = first
        for n in range(1, code_no):
            code = (code * multiplier) % divisor
        return code

    def solve(self):
        PATTERN = "Enter the code at row (\d+), column (\d+)"
        m = self.search(PATTERN)
        row = int(m.group(1))
        col = int(m.group(2))
        return Solver.code_for_row_col(row, col)


if __name__ == '__main__':
    s = Solver(from_file='input/dec25.in')
    one = s.solve()
    print("%d" % one)

    assert(one == 19980801)
