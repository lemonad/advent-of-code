"""
December 17, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)
        self.containers = []
        for val in self.lines(conversion=int):
            self.containers.append(val)

    def solve(self, liters):
        """Solution for part two."""
        n_containers = len(self.containers)
        counter_liters = 0
        min_counter = 0
        min_containers = n_containers

        # Since number of subsets of containers is 2^20, we just
        # iterate over all subsets (bits set in an integer [0, 2^20)).
        for i in range(pow(2, n_containers)):
            val = 0
            counter = 0
            # Bit n set means the n'th container is used.
            for j in range(n_containers):
                if i & 1:
                    val += self.containers[j]
                    if val > liters:
                        break
                    counter += 1
                i >>= 1
            if val == liters:
                counter_liters += 1
                if counter < min_containers:
                    min_counter = 1
                    min_containers = counter
                elif counter == min_containers:
                    min_counter += 1
        return (counter_liters, min_counter)


if __name__ == '__main__':
    s = Solver(from_file='input/dec17.in')
    (one, two) = s.solve(150)
    print("Combinations of containers that fit exactly 150l: %d" % one)
    print("Min combinations of containers that fit exactly 150l: %d" % two)

    assert(one == 4372)
    assert(two == 4)
