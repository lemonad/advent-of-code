"""
December 1, Advent of Code 2019 (Jonas Nockert / @lemonad)

"""
import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def calculate_fuel(s):
        return ((s / 3).apply(np.floor) - 2).clip(0)

    @staticmethod
    def recursive_fuel(s, fuel=0):
        res_s = Solver.calculate_fuel(s)
        res_fuel = res_s.sum()
        if res_fuel > 0:
            return Solver.recursive_fuel(res_s, res_fuel + fuel)
        else:
            return res_fuel + fuel

    def solve_part_one(self):
        s = pd.Series(self.lines(conversion=int))
        return self.calculate_fuel(s).sum().astype("int")

    def solve_part_two(self):
        s = pd.Series(self.lines(conversion=int))
        return self.recursive_fuel(s).astype("int")


if __name__ == "__main__":
    example_input = """
    12
    14
    1969
    100756
    """
    s = Solver(from_str=example_input)
    one = s.solve_part_one()
    assert one == 2 + 2 + 654 + 33583

    s = Solver(from_file="input/december1.input")
    one = s.solve_part_one()
    print(one)
    assert one == 3372463

    example_input = """
    14
    1969
    100756
    """
    s = Solver(from_str=example_input)
    two = s.solve_part_two()
    assert two == 2 + 966 + 50346

    s = Solver(from_file="input/december1.input")
    two = s.solve_part_two()
    print(two)
    assert two == 5055835
