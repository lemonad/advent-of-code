"""
December 24, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from functools import reduce
from itertools import combinations
import operator

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def quantum_entanglement(group):
        return reduce(operator.mul, group)

    @staticmethod
    def partition(weights, min_size, first_sum, n_remaining_partitions):
        if n_remaining_partitions == 0:
            return True
        elif n_remaining_partitions == 1:
            return sum(weights) == first_sum and len(weights) >= min_size

        upper_bound = len(weights) - min_size * (n_remaining_partitions - 1)
        for i in range(min_size, upper_bound + 1):
            for r in combinations(weights, i):
                part = set(r)
                part_sum = sum(part)
                rest = weights - part
                rest_sum = sum(rest)
                if (first_sum != part_sum or
                        rest_sum != first_sum * (n_remaining_partitions - 1)):
                    continue

                if Solver.partition(
                        rest,
                        min_size,
                        first_sum,
                        n_remaining_partitions - 1):
                    return True
        return False

    def get_first_group_quantum_entanglement(self, n_partitions):
        weights = set(sorted(self.lines(conversion=int), reverse=True))
        max_package = max(weights)
        # Since we're looking for the smallest first group, there's
        # no point in evaluating partitions where the first group
        # is larger than the smallest of groups two and three.
        avg = len(weights) // n_partitions
        found = False
        min_qt = None
        for i in range(1, min(avg + 1, len(weights) - 1)):
            # No point in checking longer first groups if
            # we already found a short one.
            if found:
                break
            for c in combinations(weights, i):
                first = set(c)
                qt = Solver.quantum_entanglement(first)
                first_sum = sum(first)
                if first_sum < max_package:
                    continue
                if min_qt and qt >= min_qt:
                    continue
                rest = weights - first
                rest_sum = sum(rest)
                # If, after picking group one, the rest of the
                # packages must sum to twice that of group one.
                if (first_sum * (n_partitions - 1)) != rest_sum:
                    continue

                if Solver.partition(rest,
                                    len(first),
                                    first_sum,
                                    n_partitions - 1):
                    if not min_qt or qt < min_qt:
                        min_qt = qt
                    found = True

        return min_qt

    def solve_part_one(self):
        """Solution for part two."""
        return self.get_first_group_quantum_entanglement(3)

    def solve_part_two(self):
        """Solution for part two."""
        return self.get_first_group_quantum_entanglement(4)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec24.in')
    (one, two) = s.solve()
    print("Quantum entanglement (three groups): %d" % one)
    print("Quantum entanglement (four groups): %d" % two)

    assert(one == 11846773891)
    assert(two == 80393059)
