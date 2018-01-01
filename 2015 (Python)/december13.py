"""
December 13, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from itertools import permutations
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PATTERN = ("^(\w+) would (gain|lose) (\d+) happiness units "
               "by sitting next to (\w+).")

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    def as_pairs(self):
        pairs = {}
        for m in self.lines_search(self.PATTERN):
            g = int(m.group(3))
            gain = g if (m.group(2) == 'gain') else -g
            pairs[(m.group(1), m.group(4))] = gain
        return pairs

    def happiness_delta(self, include_myself=False):
        pairs = self.as_pairs()
        persons = list(set([p1 for p1, p2 in pairs.keys()]))

        if include_myself:
            for p in persons:
                pairs[('myself', p)] = 0
                pairs[(p, 'myself')] = 0
            persons.insert(0, 'myself')

        max_happiness_delta = 0
        for perm in permutations(persons[1:]):
            happiness_delta = 0
            for i in range(len(perm) - 1):
                happiness_delta += (pairs[(perm[i], perm[i + 1])] +
                                    pairs[(perm[i + 1], perm[i])])
            happiness_delta += (pairs[(persons[0], perm[0])] +
                                pairs[(perm[0], persons[0])] +
                                pairs[(perm[-1], persons[0])] +
                                pairs[(persons[0], perm[-1])])
            if happiness_delta > max_happiness_delta:
                max_happiness_delta = happiness_delta
        return max_happiness_delta

    def solve_part_one(self):
        """Solution for part one."""
        return self.happiness_delta()

    def solve_part_two(self):
        """Solution for part two."""
        return self.happiness_delta(include_myself=True)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec13.in')
    (one, two) = s.solve()
    print("Total change in happiness: %d" % one)
    print("Total change in happiness, including myself: %d" % two)

    assert(one == 664)
    assert(two == 640)
