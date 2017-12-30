"""
December 3, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    @classmethod
    def make_move(cls, move, pos):
        if move == '^':
            pos = (pos[0], pos[1] + 1)
        elif move == 'v':
            pos = (pos[0], pos[1] - 1)
        elif move == '>':
            pos = (pos[0] + 1, pos[1])
        elif move == '<':
            pos = (pos[0] - 1, pos[1])
        else:
            raise RuntimeError('No such move')
        return pos

    @classmethod
    def santa_deliveries(cls, indata):
        pos = (0, 0)
        grid = {pos: 1}

        for move in indata:
            pos = cls.make_move(move, pos)
            if pos in grid:
                grid[pos] = grid[pos] + 1
            else:
                grid[pos] = 1

        return len(grid)

    @classmethod
    def robo_santa_deliveries(cls, indata):
        pos = [(0, 0), (0, 0)]
        grid = {pos[0]: 2}

        for index, move in enumerate(indata):
            p = cls.make_move(move, pos[index % 2])
            if p in grid:
                grid[p] = grid[p] + 1
            else:
                grid[p] = 1
            pos[index % 2] = p

        return len(grid)

    def solve_part_one(self):
        """Solution for part one."""
        return self.santa_deliveries(self.puzzle_input)

    def solve_part_two(self):
        """Solution for part two."""
        return self.robo_santa_deliveries(self.puzzle_input)

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    assert(Solver.santa_deliveries('>') == 2)
    assert(Solver.santa_deliveries('^>v<') == 4)
    assert(Solver.santa_deliveries('^v^v^v^v^v') == 2)

    assert(Solver.robo_santa_deliveries('^v') == 3)
    assert(Solver.robo_santa_deliveries('^>v<') == 3)
    assert(Solver.robo_santa_deliveries('^v^v^v^v^v') == 11)

    s = Solver(from_file='input/dec03.in')
    (one, two) = s.solve()
    print("Houses that received at least one present: %d." % one)
    print("Houses that received at least one present: %d." % two)

    assert(one == 2081)
    assert(two == 2341)
