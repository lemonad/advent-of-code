"""
December 16, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    # Sue 1: goldfish: 9, cars: 0, samoyeds: 9
    PATTERN = '^Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)'

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)
        self.mfcsam = {
            'children': 3,
            'cats': 7,
            'samoyeds': 2,
            'pomeranians': 3,
            'akitas': 0,
            'vizslas': 0,
            'goldfish': 5,
            'trees': 3,
            'cars': 2,
            'perfumes': 1
        }

        self.sues = {}
        for m in self.lines_search(self.PATTERN):
            self.sues[int(m.group(1))] = {
                m.group(2): int(m.group(3)),
                m.group(4): int(m.group(5)),
                m.group(6): int(m.group(7))
            }

    @staticmethod
    def subproblem(indata):
        pass

    def solve_part_one(self):
        """Solution for part one."""
        for key in self.sues:
            found = True
            for k, v in self.sues[key].items():
                if self.mfcsam[k] != v:
                    found = False
                    break
            if found:
                return key
        raise RuntimeError('No matching Sue')

    def solve_part_two(self):
        """Solution for part two."""
        for key in self.sues:
            found = True
            for k, v in self.sues[key].items():
                if k == 'cats' or k == 'trees':
                    if v <= self.mfcsam[k]:
                        found = False
                        break
                elif k == 'pomeranians' or k == 'goldfish':
                    if v >= self.mfcsam[k]:
                        found = False
                        break
                elif self.mfcsam[k] != v:
                    found = False
                    break
            if found:
                return key
        raise RuntimeError('No matching Sue')

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec16.in')
    (one, two) = s.solve()
    print("What is the number of the Sue that got you the gift: %d" % one)
    print("What is the number of the real Aunt Sue: %d" % two)

    assert(one == 40)
    assert(two == 241)
