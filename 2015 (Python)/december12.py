"""
December 12, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import re

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def sum_json(some_json, exclude_red=False):
        total_sum = 0
        if type(some_json) is int:
            total_sum = some_json
        elif type(some_json) is list:
            for l in some_json:
                total_sum += Solver.sum_json(l, exclude_red)
        elif type(some_json) is dict:
            if not exclude_red or 'red' not in some_json.values():
                for key in some_json:
                    total_sum += Solver.sum_json(key, exclude_red)
                    total_sum += Solver.sum_json(some_json[key], exclude_red)

        return total_sum

    def solve_part_one(self):
        """Solution for part one."""
        # Note handling of both positive and negative numbers.
        return sum([int(x)
                    for x in re.findall('(\d+|\-\d+)', self.puzzle_input)])

    def solve_part_one_alternative(self):
        """Solution for part one."""
        return self.sum_json(self.as_json())

    def solve_part_two(self):
        """Solution for part two."""
        return self.sum_json(self.as_json(), exclude_red=True)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec12.in')
    (one, two) = s.solve()
    print("Sum of all numbers in the document: %d" % one)
    print("Sum of all non-red numbers in the document: %d" % two)
    one_alt = s.solve_part_one_alternative()

    assert(one == 191164)
    assert(one_alt == 191164)
    assert(two == 87842)
