"""
December 2, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    @classmethod
    def present_area(cls, l, w, h):
        """Given box dimensions, return how much wrapping paper to order.

        The of wrapping paper required is the surface area of the box
        plus a little extra (the area of the smallest side).
        """
        topbottom = l * w
        leftright = w * h
        frontback = h * l
        return (2 * (topbottom + leftright + frontback) +
                min(topbottom, leftright, frontback))

    @classmethod
    def ribbon_len(cls, l, w, h):
        """Given box dimensions, return how much ribbon to order.

        The ribbon required to wrap a present is the shortest distance around
        its sides plus bow length (equal to the cubic feet of volume of the
        present).
        """
        wh = 2 * (w + h)
        lh = 2 * (l + h)
        lw = 2 * (w + l)
        return min(wh, lh, lw) + l * w * h

    def solve_part_one(self):
        area = 0
        for l, w, h in self.lines_split('x', conversion=int):
            area += self.present_area(l, w, h)
        return area

    def solve_part_two(self):
        ribbon = 0
        for l, w, h in self.lines_split('x', conversion=int):
            ribbon += self.ribbon_len(l, w, h)
        return ribbon

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec02.in')
    (one, two) = s.solve()
    print("Square feet of wrapping paper to order: %d." % one)
    print("Amount of ribbon to order: %d." % two)

    assert(one == 1598415)
    assert(two == 3812909)
