"""
December 15, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from copy import copy

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PATTERN = ("^(\w+): capacity (\-?\d+), durability (\-?\d+), "
               "flavor (\-?\d+), texture (\-?\d+), calories (\-?\d+)")
    N_TEASPOONS = 100

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)
        # Parse input to ingredients, where each ingredient
        # has the properties:
        #     (1) capacity,
        #     (2) durability,
        #     (3) flavor,
        #     (4) texture, and
        #     (5) calories.
        # e.g. row 1, butterscotch and row 2, cinnamon:
        #     [[-1, -2, 6, 3, 8],
        #      [2, 3, -2, -1, 3]]
        ingredients = []
        for m in self.lines_search(self.PATTERN):
            # Skip name of ingredient as it is not used.
            ingredients.append([int(m.group(2)),
                                int(m.group(3)),
                                int(m.group(4)),
                                int(m.group(5)),
                                int(m.group(6))])
        # Transpose ingredients to list of properties, where
        # each row is the property for all ingredients.
        # e.g. column 1, butterscotch and column 2, cinnamon:
        #     [[-1, 2],
        #      [-2, 3],
        #      [6, -2],
        #      [3, -1],
        #      [8, 3]]
        self.properties = []
        for i in range(len(ingredients[0])):
            p = []
            for ingredient in ingredients:
                p.append(ingredient[i])
            self.properties.append(p)

    @staticmethod
    def partitions(n, k_parts, p):
        """Generate all partitions of integer n in k parts."""
        if k_parts == 1:
            p.append(n)
            yield p
        else:
            for i in range(0, n + 1):
                pcopy = copy(p)
                pcopy.append(i)
                yield from Solver.partitions(n - i, k_parts - 1, pcopy)

    def cookie_calories(self, partition):
        """Calculate calories given a partition of ingredients."""
        return sum([p * c for p, c in zip(partition, self.properties[-1])])

    def cookie_score(self, partition):
        """Calculate cookie score given a partition of ingredients."""
        total = 1
        # Four properties excluding calories.
        for i in range(4):
            t = sum([p * x for p, x in zip(partition, self.properties[i])])
            if t <= 0:
                return 0
            total *= t
        return total

    def solve(self):
        """Solution for both parts."""
        n = self.N_TEASPOONS
        m = len(self.properties[0])
        max_total = 0
        max_total_500_cal = 0

        for part in self.partitions(n, m, []):
            total = self.cookie_score(part)
            if total > max_total:
                max_total = total
            if (self.cookie_calories(part) == 500 and
                    total > max_total_500_cal):
                max_total_500_cal = total

        return (max_total, max_total_500_cal)


if __name__ == '__main__':
    s = Solver(from_file='input/dec15.in')
    (one, two) = s.solve()
    print("Total score of the highest-scoring cookie: %d" % one)
    print("total score of the highest-scoring 500 calorie cookie: %d" % two)

    assert(one == 13882464)
    assert(two == 11171160)
