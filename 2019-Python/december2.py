"""
December 2, Advent of Code 2019 (Jonas Nockert / @lemonad)

"""
import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def subproblem(s, noun=None, verb=None):
        if noun and verb:
            s[1] = noun
            s[2] = verb
        offset = 0
        while s[offset] != 99:
            if s[offset] == 1:
                s[s[offset + 3]] = s[s[offset+1]] + s[s[offset+2]]
            elif s[offset] == 2:
                s[s[offset + 3]] = s[s[offset+1]] * s[s[offset+2]]
            else:
                print("unknown")
            offset += 4
        return s[0]

    def solve_part_one(self, noun=None, verb=None):
        """Solution for part one."""
        s = pd.Series(self.as_list(split_str=","), dtype="int")
        return Solver.subproblem(s, noun=noun, verb=verb)

    def solve_part_two(self):
        """Solution for part one."""
        for noun in range(100):
            for verb in range(100):
                s = pd.Series(self.as_list(split_str=","), dtype="int")
                s[1] = noun
                s[2] = verb
                out = Solver.subproblem(s)
                if out == 19690720:
                    return (noun, verb)

        print("Combination not found")
        return (0,0)


if __name__ == "__main__":
    example_input = """
    1,9,10,3,2,3,11,0,99,30,40,50
    """
    s = Solver(from_str=example_input)
    one = s.solve_part_one()
    assert one == 3500

    s = Solver(from_file="input/december2.input")
    one = s.solve_part_one(noun=12, verb=2)
    print(one)
    assert one == 2890696

    s = Solver(from_file="input/december2.input")
    noun, verb = s.solve_part_two()
    two = int("{:d}{:d}".format(noun, verb))
    print(two)
    assert two == 8226
