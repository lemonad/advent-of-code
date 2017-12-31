"""
December 10, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def elves_look_elves_say(seq):
        new_seq = ""
        last_s = None
        counter = 0
        for s in seq:
            if s != last_s:
                if last_s:
                    new_seq += "%d%c" % (counter, last_s)
                last_s = s
                counter = 0
            counter += 1
        new_seq += "%d%c" % (counter, last_s)
        return new_seq

    def sequence_len(self, N):
        seq = self.puzzle_input
        for i in range(N):
            seq = self.elves_look_elves_say(seq)
        return len(seq)

    def solve_part_one(self):
        """Solution for part one.

        Produces the sequence starting with

        311311222113111231133211121312211231131112311211133112111312
        211213211312111322211231131122111213122112311311222112111331
        121113112221121113122113121113222112132113213221232112111312
        111213322112311311222113111221221113122112132113121113222112
        311311222113111231133221121113311211131122211211131221131112
        311332211211131221131211132221232112111312111213322112132113
        ...

        so the idea of using another representation based on repeated
        elements, say `(c, count)`, looks like it will not work.

        """
        return(self.sequence_len(40))

    def solve_part_two(self):
        """Solution for part two."""
        return(self.sequence_len(50))

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


if __name__ == '__main__':
    s = Solver(from_str='1113222113')
    (one, two) = s.solve()
    print("Length of the result after 40 iterations: %d" % one)
    print("Length of the result after 50 iterations: %d" % two)

    assert(one == 252594)
    assert(two == 3579328)
