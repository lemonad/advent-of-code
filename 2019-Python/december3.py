"""
December 3, Advent of Code 2019 (Jonas Nockert / @lemonad)

"""
from itertools import combinations

from shapely.geometry import Point, Polygon, LineString
from shapely.ops import split

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def wire_length_to_intersection(wires, intersection_point):
        len_wire = 0
        for i in range(len(wires)):
            res = split(wires[i], intersection_point)
            prev_coord = Point(0, 0)
            for coord in res.geoms[0].coords:
                p = Point(coord[0], coord[1])
                len_wire += abs(p.x - prev_coord.x) + abs(p.y - prev_coord.y)
                prev_coord = p
        return int(len_wire)

    @staticmethod
    def wire_linestring(path_list):
        points = []
        curr_p = Point(0, 0)
        start_p = Point(0, 0)
        for p in path_list:
            direction = p[0]
            length = int(p[1:])
            if direction == "L":
                curr_p = Point(curr_p.x - length, curr_p.y)
            elif direction == "R":
                curr_p = Point(curr_p.x + length, curr_p.y)
            elif direction == "U":
                curr_p = Point(curr_p.x, curr_p.y + length)
            elif direction == "D":
                curr_p = Point(curr_p.x, curr_p.y - length)
            else:
                raise "Unknown direction {:s}".format(direction)
            points.append(curr_p)
        return LineString(points)

    def wires_from_input(self):
        wires = []
        for row in self.lines():
            path_list = row.split(",")
            wire = Solver.wire_linestring(path_list)
            wires.append(wire)
        return wires

    def solve_part_one(self):
        """Solution for part one."""
        wires = self.wires_from_input()

        min_dist = 100000000
        for p in wires[0].intersection(wires[1]):
            dist = int(abs(p.x) + abs(p.y))
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def solve_part_two(self):
        """Solution for part two."""
        wires = self.wires_from_input()
        min_dist_len = 1000000
        for p in wires[0].intersection(wires[1]):
            d = int(Solver.wire_length_to_intersection(wires, p))
            if d < min_dist_len:
                min_dist_len = d
        return min_dist_len


if __name__ == "__main__":
    example_input1 = """
        R8,U5,L5,D3
        U7,R6,D4,L4
    """
    s = Solver(from_str=example_input1)
    assert s.solve_part_one() == 6
    example_input2 = """
        R75,D30,R83,U83,L12,D49,R71,U7,L72
        U62,R66,U55,R34,D71,R55,D58,R83
    """
    s = Solver(from_str=example_input2)
    assert s.solve_part_one() == 159
    example_input3 = """
        R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
        U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
    """
    s = Solver(from_str=example_input3)
    assert s.solve_part_one() == 135

    s = Solver(from_file="input/december3.input")
    one = s.solve_part_one()
    print(one)
    assert one == 1264

    s = Solver(from_str=example_input1)
    assert s.solve_part_two() == 30
    s = Solver(from_str=example_input2)
    assert s.solve_part_two() == 610
    s = Solver(from_str=example_input3)
    assert s.solve_part_two() == 410

    s = Solver(from_file="input/december3.input")
    two = s.solve_part_two()
    print(two)
    assert two == 37390
