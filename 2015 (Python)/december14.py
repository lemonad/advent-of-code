"""
December 14, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import math
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PATTERN = ("^(\w+) can fly (\d+) km/s for (\d+) seconds, "
               "but then must rest for (\d+) seconds.")

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def distance_travelled(time, name, speed, fly_time, rest_time):
        """Calculate distance travelled given number of seconds."""
        n = math.floor(time / (fly_time + rest_time))
        return (n * fly_time * speed +
                min(fly_time, time - n * (fly_time + rest_time)) * speed)

    def solve_part_one(self, time):
        """Solution for part one."""
        max_dist = 0
        for m in self.lines_search(self.PATTERN):
            dist = self.distance_travelled(time,
                                           m.group(1),
                                           int(m.group(2)),
                                           int(m.group(3)),
                                           int(m.group(4)))
            if dist > max_dist:
                max_dist = dist
        return max_dist

    def solve_part_two(self, time):
        """Solution for part two."""
        reindeers = {}
        for m in self.lines_search(self.PATTERN):
            reindeers[m.group(1)] = {
                'speed': int(m.group(2)),
                'fly_time': int(m.group(3)),
                'rest_time': int(m.group(4)),
                'points': 0
            }

        # Instead of simulating each timestep, we just calculate
        # the total distance travelled for each reindeer every
        # timestep.
        for t in range(1, time + 1):
            max_dist = 0
            max_reindeers = None
            for name, spec in reindeers.items():
                dist = self.distance_travelled(t,
                                               name,
                                               spec['speed'],
                                               spec['fly_time'],
                                               spec['rest_time'])
                # Note that in the case of a tie, all leading
                # reindeer are given points.
                if dist == max_dist:
                    max_reindeers.append(name)
                elif dist > max_dist:
                    max_dist = dist
                    max_reindeers = [name]
            for r in max_reindeers:
                reindeers[r]['points'] += 1

        points = []
        for spec in reindeers.values():
            points.append(spec['points'])
        return max(points)

    def solve(self, time):
        return (self.solve_part_one(time), self.solve_part_two(time))


if __name__ == '__main__':
    s = Solver(from_file='input/dec14.in')
    (one, two) = s.solve(2503)
    print("What distance has the winning reindeer traveled? %d" % one)
    print("How many points does the winning reindeer have? %d" % two)

    assert(one == 2655)
    assert(two == 1059)
