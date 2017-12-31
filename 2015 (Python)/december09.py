"""
December 9, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from itertools import permutations

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)
        self.distances = {}
        self.locations = set()

        # Distances of all pairs of locations.
        for m in self.lines_search('^(\w+) to (\w+) = (\d+)'):
            loc1 = m.group(1)
            loc2 = m.group(2)
            self.locations.add(loc1)
            self.locations.add(loc2)
            dist = int(m.group(3))
            self.distances[(loc1, loc2)] = dist
            self.distances[(loc2, loc1)] = dist

    def all_distances(self):
        perms = permutations(self.locations)
        for perm in perms:
            dist = 0
            for i in range(len(perm) - 1):
                locs = (perm[i], perm[i + 1])
                dist += self.distances[locs]
            yield dist

    def solve_part_one(self):
        """Solution for part one."""
        return min(self.all_distances())

    def solve_part_two(self):
        """Solution for part two."""
        return max(self.all_distances())

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec09.in')
    (one, two) = s.solve()
    print("Distance of the shortest route: %d" % one)
    print("Distance of the shortest route: %d" % two)

    assert(one == 251)
    assert(two == 898)
