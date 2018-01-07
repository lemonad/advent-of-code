"""
December 19, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import re

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PATTERN = "^(\w+) => (\w+)"

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)
        self.replacements = []
        self.electrons = []
        self.molecule = ""
        for line in self.lines():
            m = re.search(self.PATTERN, line)
            if m:
                rep = (m.group(1), m.group(2))
                if m.group(1) == 'e':
                    self.electrons.append(rep)
                else:
                    self.replacements.append(rep)
            else:
                # last line
                self.molecule = line.strip()
        assert(self.molecule)

        # Since we're going for a greedy solution in part two, sort the
        # replacements according to length (longest replacement first).
        self.replacements.sort(key=lambda k: len(k[1]), reverse=True)

    def solve_part_one(self):
        """Solution for part one."""
        memo = {}

        for k, r in self.replacements:
            lk = len(k)
            indexes = []
            index = 0
            while True:
                index = self.molecule.find(k, index)
                if index == -1:
                    break
                indexes.append(index)
                index += 1

            for index in indexes:
                a = self.molecule[0:index] + r + self.molecule[index + lk:]
                if a not in memo:
                    memo[a] = True

        return len(memo)

    def solve_part_two(self):
        """Solution for part two.

        Greedy solution works here (possibly this can be seen in the
        input grammar) but generally we would have to do a BFS to find
        out shortest number of steps. This is "impossible" here due
        to branching factor.

        """
        count = 1
        a = self.molecule

        while True:
            for k, r in self.replacements:
                lr = len(r)
                index = a.rfind(r)
                if index == -1:
                    continue
                a = a[0:index] + k + a[index + lr:]
                count += 1
                for e in self.electrons:
                    if a == e[1]:
                            return count
                break

        return None

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec19.in')
    (one, two) = s.solve()
    print("How many distinct molecules can be created? %d" % one)
    print("How long will it take to make the medicine? %d steps" % two)

    assert(one == 518)
    assert(two == 200)
