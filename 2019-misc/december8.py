"""
December 8, Advent of Code 2019 (Jonas Nockert / @lemonad)

"""
import platform

if platform.system() == "Darwin":
    import matplotlib

    matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
import numpy as np

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    def to_layers(self, width, height):
        m = np.array(list(self.puzzle_input), dtype="float")
        return m.reshape((-1, height, width))

    def solve_part_one(self, width, height):
        """Solution for part one."""
        m = self.to_layers(width, height)
        zero_counts = np.sum(np.where(m == 0, 1, 0), axis=(1, 2))
        layer = m[np.argmin(zero_counts)]
        return np.sum(np.where(layer == 1, 1, 0)) * np.sum(np.where(layer == 2, 1, 0))

    def solve_part_two(self, width, height):
        """Solution for part two."""
        m = self.to_layers(width, height)
        n_layers = m.shape[0]
        # Set transparent pixels to NaN.
        m[m == 2] = np.nan
        img = m[0]
        for i in range(1, n_layers):
            # Replace NaNs with pixels of next layer.
            img[np.isnan(img)] = m[i][np.isnan(img)]
        return img


if __name__ == "__main__":
    example_input = """
    123456789012
    """
    s = Solver(from_str=example_input)
    one = s.solve_part_one(3, 2)
    assert one == 1

    s = Solver(from_file="input/december8.input")
    one = s.solve_part_one(25, 6)
    print(one)
    assert one == 2210

    example_input = """
    0222112222120000
    """
    s = Solver(from_str=example_input)
    two = s.solve_part_two(2, 2)
    assert list(two.reshape((4))) == [0, 1, 1, 0]

    s = Solver(from_file="input/december8.input")
    two = s.solve_part_two(25, 6)
    plt.imshow(two)
    plt.show()
