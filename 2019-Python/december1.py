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
    def add_fuel_column(df):
        """Adds a column with the fuel cost for the previous column"""
        s_col = df.iloc[:, -1]
        n_cols = len(df.columns)
        col_label = "iter-{:d}".format(n_cols)
        df.insert(n_cols, col_label, ((s_col / 3).apply(np.floor) - 2).clip(0))

    def solve_part_one(self):
        df = pd.DataFrame(self.lines(conversion=int))
        self.add_fuel_column(df)
        return df.iloc[:, 1:].sum().sum().astype("int")

    def solve_part_two(self):
        df = pd.DataFrame(self.lines(conversion=int))
        while df.iloc[:, -1].sum() > 0:
            self.add_fuel_column(df)
        return df.iloc[:, 1:].sum().sum().astype("int")


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
