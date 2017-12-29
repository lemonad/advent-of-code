"""
December 1, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def solve_part_one(self):
        return self.puzzle_input.count('(') - self.puzzle_input.count(')')

    def solve_part_two(self):
        pos = floor = 0
        for c in self.chars():
            pos += 1
            if c == '(':
                floor += 1
            else:
                floor -= 1

            if floor == -1:
                return pos

        raise RuntimeError("Error: Santa never enters basement!")

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_file='input/dec01.in')
    (floor, position) = s.solve()
    print("The instructions takes Santa to floor %d." % floor)
    print("Position of character causing Santa to enter the basement: %d." %
          position)

    assert(floor == 280)
    assert(position == 1797)
