"""
December 15, Advent of Code 2018 (Jonas Nockert / @lemonad)

"""
import collections
from collections import deque
from enum import Enum
import heapq
import math
import os
import re
import string

import numpy as np
import pandas as pd

from common.puzzlesolver import PuzzleSolver

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    def print_grid(self, G, monsters):
        max_x = 0
        max_y = 0
        for g in G.values():
            max_x = max(g['x'], max_x)
            max_y = max(g['y'], max_y)

        # print(max_x, max_y)

        grid = self.H.copy()
        for m in monsters:
            x = G[monsters[m]['loc']]['x']
            y = G[monsters[m]['loc']]['y']
            if monsters[m]['type'] == 'Goblin':
                grid[y, x] = b'G'
            else:
                grid[y, x] = b'E'
        formatter = lambda x: '%s' % x
        print(np.array2string(np.char.decode(grid), separator='',
            formatter={'str_kind': formatter}))

        # grid = self.H.copy()
        # for g in G:
        #     x = G[g]['x']
        #     y = G[g]['y']
        #     m = G[g]['contains']
        #     if not m:
        #         grid[y, x] = b'.'
        #     elif monsters[m]['type'] == 'Goblin':
        #         grid[y, x] = b'G'
        #     elif monsters[m]['type'] == 'Elf':
        #         grid[y, x] = b'E'
        #     else:
        #         raise Exception()
        # formatter = lambda x: '%s' % x
        # print(np.array2string(np.char.decode(grid), separator='',
        #     formatter={'str_kind': formatter}))

    @staticmethod
    def heuristic(a, b, G):
        x1 = G[a]['x']
        y1 = G[a]['y']
        x2 = G[b]['x']
        y2 = G[b]['y']
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def a_star_search(start, goal, graph):
        # print("Start", start, graph[start], "goal", goal, graph[goal])
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()
            # print("Current=", current, " / ", start)

            if current == goal:
                break

            # print(current, graph[current]['adj'])
            for next in graph[current]['adj']:
                # Check for monsters.
                if (graph[next]['contains'] and
                        next != goal):
                    # print("Skipped", next)
                    continue
                #else:
                    # print("Not skipped", next, graph[next])
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + Solver.heuristic(goal, next, graph)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far

    @staticmethod
    def targets(u, monsters):
        t = monsters[u]['type']
        targets = []
        if t == 'Goblin':
            for k in monsters.keys():
                if monsters[k]['type'] == 'Elf':
                    targets.append(k)
        else:
            for k in monsters.keys():
                if monsters[k]['type'] == 'Goblin':
                    targets.append(k)
        return targets

    @staticmethod
    def targets_by_hp(targets, G, monsters):
        t = sorted(targets, key=lambda k: (
            monsters[k]['HP'],
            G[monsters[k]['loc']]['y'],
            G[monsters[k]['loc']]['x']))
        return t

    @staticmethod
    def targets_in_range(u, targets, G, monsters):
        in_range = []
        loc = monsters[u]['loc']
        adj = G[loc]['adj']
        for t in targets:
            if monsters[t]['loc'] in adj:
                in_range.append(t)
        return in_range

    @staticmethod
    def find_adjacent_open_squares(targets, G, monsters):
        open_locs = []
        for t in targets:
            loc = monsters[t]['loc']
            adj = G[loc]['adj']
            for a in adj:
                if not G[a]['contains']:
                    open_locs.append(a)
        return open_locs

    # def lowest_hp(x, y, G, HP):
    #     t = G[b[0], b[1]].decode('UTF-8')
    #     c = np.array([[y, x - 1], [y, x + 1], [y - 1, x], [y + 1, x]])
    #     if t == 'G':
    #         print(G[c])
    #     else:
    #         print(G[c])

    def solve_part_one(self):
        """Solution for part one."""
        all_nodes = []
        node_ids = {}
        node_coords = {}
        monsters = {}
        G = {}
        self.H = self.as_char_numpy_array()
        i = 1
        for y, row in enumerate(self.H):
            for x, h in enumerate(row):
                if h != b'#':
                    all_nodes.append((x, y))
                    node_ids[(x, y)] = i
                    node_coords[i] = (x, y)
                    if h == b'G':
                        monsters[i] = {'loc': i, 'type': 'Goblin', 'HP': 200, 'Attack': 3}
                        self.H[y, x] = b'.'
                    elif h == b'E':
                        monsters[i] = {'loc': i, 'type': 'Elf', 'HP': 200, 'Attack': 3}
                        self.H[y, x] = b'.'
                    i += 1

        for x, y in all_nodes:
            i = node_ids[(x, y)]
            if i in monsters:
                mi = i
            else:
                mi = None
            G[i] = {'contains': mi, 'adj': [], 'x': x, 'y': y}
            if (x, y - 1) in all_nodes:
                G[i]['adj'].append(node_ids[(x, y - 1)])
            if (x, y + 1) in all_nodes:
                G[i]['adj'].append(node_ids[(x, y + 1)])
            if (x - 1, y) in all_nodes:
                G[i]['adj'].append(node_ids[(x - 1, y)])
            if (x + 1, y) in all_nodes:
                G[i]['adj'].append(node_ids[(x + 1, y)])

        rounds = 1
        while rounds < 500:
            units = sorted(monsters, key=lambda k: (G[monsters[k]['loc']]['y'], G[monsters[k]['loc']]['x']))
            for u in units:
                if u not in monsters:
                    # Killed
                    continue

                loc = monsters[u]['loc']
                targets = self.targets(u, monsters)
                if not targets:
                    # Combat ends
                    total_hp = 0
                    for m in monsters:
                        total_hp += monsters[m]['HP']
                    return (rounds, total_hp, (rounds - 1) * total_hp)

                targets_in_range = self.targets_in_range(u, targets, G, monsters)
                if targets_in_range:
                    print("Targets in range so dont move")
                    pass
                else:
                    # Move
                    print("Moving monster", u, "from", loc, (G[loc]['x'], G[loc]['y']))
                    # Find target adjacent squares
                    open_squares = self.find_adjacent_open_squares(targets, G, monsters)
                    # open_square_dists = self.distances(x, y, open_squares, G, HP, A)
                    paths = {}
                    for oloc in open_squares:
                        came_from, cost_so_far = self.a_star_search(oloc, loc, G)
                        if loc not in cost_so_far:
                            print("Skip  ", oloc, (G[oloc]['x'], G[oloc]['y']))
                            print("Adj", G[loc]['adj'])
                            # print("skipping", oloc)
                            continue
                        paths[oloc] = {'cost': cost_so_far[loc], 'dest': oloc, 'path': came_from, 'costs': cost_so_far}
                        # print(loc, (G[loc]['x'], G[loc]['y']), oloc, (G[oloc]['x'], G[oloc]['y']))
                        # print(oloc, cost_so_far[loc])
                    if not paths:
                        print("No path")
                        continue
                        # for a in G[loc]['adj']:
                        #     print(G[a])
                        # return None

                    sorted_paths = sorted(paths, key=lambda k: (paths[k]['cost'],
                        G[paths[k]['path'][loc]]['y'], G[paths[k]['path'][loc]]['y']))
                    if sorted_paths:
                        path_id = sorted_paths[0]
                        next_loc = paths[path_id]['path'][loc]
                        print("      ", next_loc, (G[next_loc]['x'], G[next_loc]['y']))
                        G[next_loc]['contains'] = G[loc]['contains']
                        G[loc]['contains'] = None
                        monsters[u]['loc'] = next_loc
                        # print(monsters)

                # Attack?
                targets_in_range = self.targets_in_range(u, targets, G, monsters)
                if targets_in_range:
                    print("Targets in range:", targets_in_range)
                    print(monsters)
                    by_hp = self.targets_by_hp(targets_in_range, G, monsters)
                    print(by_hp[0])
                    opponent = by_hp[0]
                    monsters[opponent]['HP'] -= monsters[u]['Attack']
                    print(monsters)
                    if monsters[opponent]['HP'] <= 0:
                        G[monsters[opponent]['loc']]['contains'] = None
                        del monsters[opponent]
            self.print_grid(G, monsters)
            rounds += 1
        return None

        self.print_grid(G, monsters)
        print(monsters)
        total_hp = 0
        for m in monsters:
            total_hp += monsters[m]['HP']
        return (rounds, total_hp, rounds * total_hp)
        return None



        # HP = np.zeros(np.shape(G))
        # A = np.zeros(np.shape(G))
        # stats = {}

        # both = np.argwhere(np.logical_or(G==b'G', G==b'E'))
        # for b in both:
        #     t = G[b[0], b[1]].decode('UTF-8')
        #     HP[b[0], b[1]] = 200
        #     A[b[0], b[1]] = 3
        #     if t == 'G':
        #         stats[(b[0], b[1])] = {'type': 'Goblin', 'HP': 200, 'Attack': 3}
        #     else:
        #         stats[(b[0], b[1])] = {'type': 'Elf', 'HP': 200, 'Attack': 3}

        # while True:
        #     both = np.argwhere(np.logical_or(G==b'G', G==b'E'))
        #     goblins = np.argwhere(G==b'G')
        #     elfs = np.argwhere(G==b'E')
        #     for b in both:
        #         x = b[1]
        #         y = b[0]
        #         targets = self.targets_by_hp(x, y, G, HP, A)
        #         if targets == 0:
        #             # Combat ends
        #             return G[y, x]

        #         target_dists = self.distances(x, y, targets, G, HP, A)
        #         targets_in_range = targets[target_dists == 1]
        #         if targets_in_range.size > 0:
        #             # Attack
        #             pass
        #         else:
        #             # Move
        #             # Find target adjacent squares
        #             open_squares = self.find_adjacent_open_squares(x, y, targets, G, HP, A)
        #             open_square_dists = self.distances(x, y, open_squares, G, HP, A)
        #             print(open_square_dists)

        #         t = G[y, x].decode('UTF-8')
        #         w = G[y, x - 1].decode('UTF-8')
        #         e = G[y, x + 1].decode('UTF-8')
        #         n = G[y - 1, x].decode('UTF-8')
        #         s = G[y + 1, x].decode('UTF-8')
        #         # print(x, y, self.targets_by_hp(x, y, G, HP, A))
        #         return None
        #         if t == 'G':
        #             # Check if target is in range. Attack.
        #             if n == 'E' or e == 'E' or s == 'E' or w == 'E':
        #                 print('Found Elf')
        #         else:
        #             if n == 'G' or e == 'G' or s == 'G' or w == 'G':
        #                 print('Found Goblin')

        #         print(t, n, e, s, w)


        #     # for g in G:
        #     #     print(g)
        #     return None
        # return None

    def solve_part_two(self):
        """Solution for part two."""
        return None

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


def main(input_data):
    example_input = """
    #########
    #G..G..G#
    #.......#
    #.......#
    #G..E..G#
    #.......#
    #.......#
    #G..G..G#
    #########
    """
    example_input = """
    #######
    #.G...#
    #...EG#
    #.#.#G#
    #..G#E#
    #.....#
    #######
    """
    example_input = """
    #######
    #G..#E#
    #E#E.E#
    #G.##.#
    #...#E#
    #...E.#
    #######
    """
    s = Solver(from_file="input/december15.input")
    # s = Solver(from_str=example_input)
    one = s.solve_part_one()
    print(one)
    assert(one == 0)

    # s = Solver(from_file="input/december15.input")
    s = Solver(from_str=example_input)
    two = s.solve_part_two()
    print(two)
    assert(two == 0)
    return

    s = Solver(from_file="input/december15.input")
    (one, two) = s.solve()
    print(one)
    print(two)
    # print("{:s}".format(one))
    # print("{:s}".format(two))


if __name__ == "__main__":
    input_data = """
################################
######..#######.################
######...######..#.#############
######...#####.....#############
#####....###G......#############
#####.#G..#..GG..##########..#.#
#######G..G.G.....##..###......#
######....G...........#.....####
#######.G......G........##..####
######..#..G.......E...........#
######..G................E..E..#
####.............E..........#..#
#####.........#####........##..#
########.....#######.......#####
########..G.#########......#####
#######.....#########....#######
#######G....#########..G...##.##
#.#.....GG..#########E##...#..##
#.#....G....#########.##...#...#
#....##......#######..###..##E.#
####G.........#####...####....##
####..G...............######..##
####....#.....##############.###
#..#..###......#################
#..#..###......#################
#.....#####....#################
###########.E.E.################
###########.E...################
###########.E..#################
#############.##################
#############.##################
################################
    """.strip()
    main(input_data)
