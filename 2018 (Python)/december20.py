"""
December 20, Advent of Code 2018 (Jonas Nockert / @lemonad)

"""
from collections import deque
from enum import Enum, unique
import heapq
import math
import os
import re
import string

import numpy as np
import pandas as pd
import sympy as sp

from common.puzzlesolver import PuzzleSolver
from common.gridgraph import GridGraph


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Graph():
    def __init__(self):
        self.next_index = 1
        self.g = {0: {
            'adj': [], 'pos': (0, 0), 'dist': None,
            'N': None, 'S': None, 'W': None, 'E': None}}
        self.pos = {(0, 0): 0}

    def print(self):
        print(self.g)

    def add(self, node, direction):
        dirs = self.g[node]
        if dirs[direction] is not None:
            return dirs[direction]

        pos_x, pos_y = self.g[node]['pos']
        if direction == "N":
            opposite_direction = "S"
            pos_y += 1
        elif direction == "E":
            opposite_direction = "W"
            pos_x += 1
        elif direction == "S":
            opposite_direction = "N"
            pos_y -= 1
        else:  # W
            opposite_direction = "E"
            pos_x -= 1

        if (pos_x, pos_y) in self.pos:
            child_node = self.pos[(pos_x, pos_y)]
            self.g[node][direction] = child_node
            self.g[child_node][opposite_direction] = node
            self.g[node]['adj'].append(child_node)
            self.g[child_node]['adj'].append(node)
            return child_node

        child_node = self.next_index
        self.next_index += 1
        self.g[child_node] = {
                'adj': [], 'pos': (pos_x, pos_y), 'dist': None,
                'N': None, 'S': None, 'W': None, 'E': None}
        self.g[node][direction] = child_node
        self.g[child_node][opposite_direction] = node
        self.g[node]['adj'].append(child_node)
        self.g[child_node]['adj'].append(node)
        self.pos[(pos_x, pos_y)] = child_node
        return child_node

    def all_shortest_paths(self):
        for i in range(self.next_index - 1, 0, -1):
            pathlen = self.shortest_path(0, i)
            yield pathlen

    def dims(self):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for k in self.g.keys():
            min_x = min(min_x, self.g[k]['pos'][0])
            max_x = max(max_x, self.g[k]['pos'][0])
            min_y = min(min_y, self.g[k]['pos'][1])
            max_y = max(max_y, self.g[k]['pos'][1])
        return (min_x, max_x, min_y, max_y)

    def shortest_path(self, start, goal):
        if self.g[goal]['dist']:
            return self.g[goal]['dist']

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if (self.g[current]['dist'] and
                    cost_so_far[current] != self.g[current]['dist']):
                raise Exception("What!")
            self.g[current]['dist'] = cost_so_far[current]

            if current == goal:
                break

            for next in self.g[current]['adj']:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + 1
                    frontier.put(next, priority)

        return cost_so_far[goal]

# @unique
# class Symbol(Enum):
#     DIRECTIONS = 256
# 
#     NORTH = 1
#     EAST = 2
#     SOUTH = 3
#     WEST = 4
# 
#     END = 32
#     LPAREN = 33
#     RPAREN = 34
#     DIV = 35
#     START = 36
# 
#     # Not in grammar, just to simplify parsing.
#     QUIT = 128
# 
# class SyntaxTree():
#     def __init__(self, symbol, value = None):
#         self.symbol = symbol
#         self.subtrees = []
# 
#     def add_subtree(self, subtree):
#         self.subtrees.append(subtree)
# 
# class Parser(object):
#     tokens = None
#     sym = None
#     lexer = None
# 
#     def __init__(self, tokens):
#         self.tokens = iter(tokens)
# 
#     def nextsym(self):
#         try:
#             self.sym = next(self.tokens)
#         except StopIteration:
#             self.sym = None
# 
#     def accept(self, s):
#         if self.sym.symbol == s:
#             self.nextsym()
#             return True
#         return False
# 
#     def expect(self, s):
#         if self.accept(s):
#             return True
#         raise Error("Syntaxfel på rad %d" % self.sym.line)
# 
#     def directions(self):
#         directions_node = SyntaxTree(Symbol.DIRECTIONS)
#         while True:
#             node = self.direction()
#             if node == None:
#                 break
#             directions_node.add_subtree(node)
#         return directions_node
# 
#     def direction(self):
#         if self.accept(Symbol.NORTH):
#             return SyntaxTree(Symbol.NORTH)
#         elif self.accept(Symbol.EAST):
#             return SyntaxTree(Symbol.EAST)
#         elif self.accept(Symbol.SOUTH):
#             return SyntaxTree(Symbol.SOUTH)
#         elif self.accept(Symbol.WEST):
#             return SyntaxTree(Symbol.WEST)
#         else:
#             return None
# 
#         elif self.accept(Symbol.LPAREN):
#             dir_node = SyntaxTree(Symbol.DIRECTIONS)
#             dir_tree = self.directions()
#             self.expect(Symbol.RPAREN)
#             # Avoid nesting by adding subtrees instead of COMMANDS node.
#             for tree in dir_tree.subtrees:
#                 dir_node.add_subtree(tree)
#             return dir_node
#         elif self.accept(Symbol.DIV):
#             return SyntaxTree(Symbol.DIV)
# 
#     def parse(self):
#         self.nextsym()
#         self.expect(Symbol.START)
#         tree = self.directions()
#         self.expect(Symbol.END)
#         self.expect(Symbol.QUIT)
#         return tree
# 
# class Lexer():
#     source_code = None
# 
#     def __init__(self, logo_code):
#         self.source_code = logo_code
# 
#     def lex(self):
#         keywords = {
#             'FORW': Symbol.FORW,
#             'BACK': Symbol.BACK,
#             'LEFT': Symbol.LEFT,
#             'RIGHT': Symbol.RIGHT,
#             'DOWN': Symbol.DOWN,
#             'UP': Symbol.UP,
#             'COLOR': Symbol.COLOR,
#             'REP': Symbol.REP
#         }



class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def parse_inner_directions(dir_list, start_pos, end_pos):
        out_len = 0
        pos = start_pos
        outlens = []
        outlen = 0
        while pos <= end_pos:
            if dir_list[pos] in ["N", "E", "S", "W"]:
                outlen += 1
            elif dir_list[pos] == "|":
                outlens.append(outlen)
                outlen = 0
            elif dir_list[pos] == "(":
                inner_start_pos = pos + 1
                pos += 1
                level = 1
                while level > 0:
                    if dir_list[pos] == "(":
                        level += 1
                    if dir_list[pos] == ")":
                        level -= 1
                    pos += 1
                pos -= 1  # end on ')'.
                inner_end_pos = pos
                outlen += Solver.parse_inner_directions(
                        dir_list, inner_start_pos, inner_end_pos)
            pos += 1
        outlens.append(outlen)
        if 0 in outlens:
            return 0
        return max(outlens)

    @staticmethod
    def parse_directions(dir_list):
        "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
        out_len = 0
        pos = 1
        outlen = Solver.parse_inner_directions(dir_list, 1, len(dir_list) - 1)
        return outlen

    @staticmethod
    def parse_inner_directions_g(dir_list, start_pos, end_pos, G, parent_node):
        out_len = 0
        pos = start_pos
        current_nodes = set([parent_node])
        outnodes = set()

        while pos <= end_pos:
            if dir_list[pos] in ["N", "E", "S", "W"]:
                print(dir_list[pos], current_nodes)
                current_nodes = set([G.add(c, dir_list[pos]) for c in current_nodes])
            elif dir_list[pos] == "|":
                outnodes.update(current_nodes)
                current_nodes = set([parent_node])
            elif dir_list[pos] == "(":
                pos += 1
                inner_start_pos = pos
                level = 1
                while level > 0:
                    if dir_list[pos] == "(":
                        level += 1
                    if dir_list[pos] == ")":
                        level -= 1
                    pos += 1
                pos -= 1  # end on ')'.
                inner_end_pos = pos
                comb = set()
                print(current_nodes)
                for c in current_nodes:
                    new_nodes = Solver.parse_inner_directions_g(
                            dir_list, inner_start_pos, inner_end_pos, G, c)
                    comb.update(new_nodes)
                current_nodes = comb
            pos += 1
        outnodes.update(current_nodes)
        return outnodes

    @staticmethod
    def parse_directions_g(dir_list, G):
        out_len = 0
        pos = 1
        outlen = Solver.parse_inner_directions_g(dir_list, 1, len(dir_list) - 1, G, 0)
        print("all paths")
        cnt = 0
        for pathlen in G.all_shortest_paths():
            if pathlen >= 1000:
                cnt += 1
        # All shortest paths for G
        return cnt

        # while pos < len(dir_list):
        #     if dir_list[pos] in ["N", "E", "S", "W"]:
        #         outlen += 1
        #     elif dir_list[pos] == "(":
        #         start_pos = pos + 1
        #         pos += 1
        #         level = 1
        #         while level > 0:
        #             if dir_list[pos] == "(":
        #                 level += 1
        #             if dir_list == ")":
        #                 level -= 1
        #         end_pos = pos
        #         out_len += parse_inner_directions(dir_list, start_pos, end_pos)
        #     pos += 1
        # return out_len

    def solve_part_one(self):
        """Solution for part one."""
        return self.parse_directions(list(self.puzzle_input))

    def solve_part_two(self):
        """Solution for part two."""
        G = Graph()
        n_paths = self.parse_directions_g(list(self.puzzle_input), G)

        min_x, max_x, min_y, max_y = G.dims()
        w = max_x - min_x + 1
        h = max_y - min_y + 1
        plan = np.zeros((2 * h + 1, 2 * w + 1), dtype="c")
        plan.fill(b'#')
        for k in G.g.keys():
            x, y = G.g[k]['pos']
            x = 2 * x - 2 * min_x + 1
            y = 2 * y - 2 * min_y + 1
            plan[y, x] = b'.'
            if G.g[k]['N']:
                plan[y + 1, x] = b'-'
            if G.g[k]['S']:
                plan[y - 1, x] = b'-'
            if G.g[k]['E']:
                plan[y, x + 1] = b'|'
            if G.g[k]['W']:
                plan[y, x - 1] = b'|'
        x = -2 * min_x + 1
        y = -2 * min_y + 1
        plan[y, x] = b'X'

        formatter = lambda x: '%s' % x
        print(np.array2string(np.char.decode(np.flip(plan, 0)),
            separator='', prefix='', suffix='',
            max_line_width=np.nan, formatter={'str_kind': formatter}))

        return n_paths

    def solve(self):
        return (self.solve_part_one(), self.solve_part_two())


def main(input_data):
    example_input = """
    ^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
    """
    s = Solver(from_str=example_input)
    one = s.solve_part_one()
    assert one == 18

    s = Solver(from_file="input/december20.input")
    one = s.solve_part_one()
    print(one)
    assert one == 3502

    # ex = "^WNE$"
    # ex = "^ENWWW(NEEE|SSE(EE|N))$"
    # ex = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    ex = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
    # ex = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"
    # ex = "^N(E|W)N(E|W)$"
    s = Solver(from_str=ex)
    s = Solver(from_file="input/december20.input")
    s = Solver(from_file="day20.txt")
    two = s.solve_part_two()
    print(two)
    assert two == 0
    return

    #8984 too high
    s = Solver(from_file="input/december20.input")
    (one, two) = s.solve()
    print(one)
    print(two)
    # print("{:s}".format(one))
    # print("{:s}".format(two))


if __name__ == "__main__":
    input_data = """
^SENEESWSWSSWSWSWNWSWWSESEESESSWSWSWWSSWSWSWWSSWNNWSSWWWSSSEESSENEEEENENEENNWNN(NENNESSSS(WNSE|)ESWSSEESWWSSENEENNEESESSSEEEEEESSSSSWSWNWNNNEE(SWSEWNEN|)NWWWWSSSSWWWWSWWWSWWWSWWSWSEENEESSSEENWNEENWN(EESESSSWW(NENSWS|)SWWWWSSWWNWWNNN(ESSENE(SS|N(E(N|S)|W))|WWNWNWSWWNNNWNNWSSWWSWWWSWSEENESSEENWNENESSSSEN(NNN|ESSSWSEESSWWWSWNNE(EE|NNWN(EE|NWSSWSE(E|SSWNWNWSSWSWSEEESEEEEESSENENWNN(EEENWNEESESSSWSSSSSENESSWWWWWWWNWWWS(WWNENEEEEN(WWNN(ESNW|)WWWWSSS(ENEN(ESNW|)W|SSWNNWNNWNWNNE(NWWNENNWSWSSSSSWNNWNENWWNWWNENEES(E(SWEN|)NE(EENWNENWNWWNENESESESE(SEEE(NWWEES|)S(ENSW|)WS(WWSS(ENSW|)W(SEWN|)NNN(N|EE)|E)|NNWNNEE(SWEN|)ENEE(SWEN|)EENWNNENWWNNESENNWWNWWNNWNNEENEEENWNEESSENNNENNWSWWWNWSWSSE(NEEEWWWS|)SWWWWS(EE|WNNENWNWWWSSWSESSWSWWSWNWSWWSWWWSEEESWWSESWWNWWSWWWWSSWWWNNWSSSEESWSESWSWWW(NNESENNWNNNNW(NNENNNNW(SSS|NENNW(NENEESENNESENNESSSESSESSENESENNENNWSWNNNWNWW(SES(ESS(WN|SE)|W)|NNWNEENESSS(WNSE|)ESESSENNEENNWNENWNEENWWWSSSWW(NENNNNWSWWWSWSS(ENENEESW(ENWWSWENEESW|)|WWWNENWNNWSWWW(SEEESWWWSEEESEEESS(E|WWN(E|WSS(SWNNNNWWSESSSW(S|NN)|EE)))|NNNESE(SWEN|)NENNNEENNNWWSWWSW(SSENE(NEEN|SSWW)|NNNNENENWNEESESSW(N|WS(SWNSEN|)EEENEEENWWNENWNNENWNWWWWWNNENENNNNEESWSEESWWSESS(WNWSWENESE|)EENN(WSNE|)ESEENNESEEENWWNWWNWWW(SEES(WW|S)|NEEENWWNWNNNWWWNNEEENWNWNENWWNENEEEESSWSW(NN(W|E)|SESESENENEENEENNWNENEENWWWSWSSWWNENNENWNWNWWWNWNEENNWNEENWNNNWWWSESWWNNWSWNNWSSSWW(SESSW(N|SSEEESSSWSESSE(SWSSWWNW(NNEE(S(W|S)|NWWNENNW(NEESNWWS|)S)|SSSEESE(SSWWW(NE(NWES|)E|SSESSSSW(SSES(ENN(NNNESEENE(S(E|SS)|NNWWS(E|S|WNW(N(E|W)|S)))|W)|SW(N|SSSSEESWS(W(SSS|N)|EEENN(WSNE|)ESSS(W|SS))))|NNN))|NE(SE|NWWW)))|EEEEENEN(ESSWSSSEE(SWWSWN|EE)|NWWS(WS(E|WNNWSW(SEWN|)NNNESE(ESNW|)NNNWNWNEEE(S(SEWN|)W|N(ENNSSW|)WWWW(NEWS|)SSW(NN|S(EESEWNWW|)W)))|E))))|NENNN(WSSNNE|)EEEES(W|ENESEEEESSEEEENESENENN(WWWWS(EEE|WNW(SSEEWWNN|)WWWW)|ESEEN(EEEEESEESWSSWNNWSWWNW(NEE(S|E)|WWSEESSSENNESE(SSSWWWN(EENSWW|)WWSWWNNNWWN(WSWWWN(W(WNNSSE|)SSSEESWSESEESSW(NW(WNWW(W|NN(ESNW|)N)|S)|SEENNNESESWSESSESEEEESWWSEEESSWWN(WSWNNNWSSSSEEESWWWWSSEEESWSWWSSWWSEEENEESWSSSWNNWWSWNWWNNWNENNNWSSWSSW(SES(E(SEESEEE(N|SESENEEENNWN(WSSEWNNE|)EEEENNWWNEENNNESESWSEEENESEESEEESWSSESSWSWNWSWWWSWWWNNENWWN(WWSSSSEE(SSWNWSSSWWNWSWWNNWNWSWNWWNWSSWSWWNNE(ENN(WSWWSSW(SS(W|E(N|SS(WNSE|)SSEENNNW(NEESENNENESEESWWWSEESWSWWN(E|WSSESSSEENWNNEES(SSEENEEESSWW(NEWS|)WSSWNWSWSSEESWSWWS(EEENESSWSEENNNENEEESSSEESWSWNWNWSW(NNEENW|SWWSWW(NEWS|)SEESWWSESSWNWSSW(NN|SESENNEEEE(NWNW(S|NEESE(S|NNESEENEEESW(SEE(SWSEWNEN|)NNNNWNNNNESSSESSS(ENNENENWW(NENNNNENNEEENEENNWWWNEENWNNWWNENNEESENEEESESEESEENEESWSSEEN(W|ENEESESENNEEESENNNNESEESWWSSEEESSWNWWSWSEE(N|ESSESSEENNENNNENNENEEEEENWNNESEESSW(N|SSWWN(WSWSEESESENN(ENESESWWSEEENESSESSWWSSWSWNNENNN(ESEWNW|)WWWWWSSEESE(SSSWWSSEEN(ESSSSEEEEESWSWSEENEENWNNWWWWNENNNW(NENNEEEENNNENENESEEENWNNNWWSES(WWWNENNNWNENWWWSWSWWNWWNEENWNWWS(E|S(SSSS(EEEEEEE(SSWNWSW(NWSWNW|SSEE(SWSSEN|EN(E|WW)))|ENWN(WSWWWWNWS(NESEEEWWWNWS|)|N))|W)|WNNNWNENNEEENNEENNESESWSSSWNW(NEWS|)SSESS(SS(ENNESEENEENEESWSW(SEEEN(NNNEEESSWW(NEWS|)SSEEEESWSSWNNWSWSESSWW(N(E|NWNWSWNNEEE(E|S))|SESSESWSWNWSSWSSWSWWSWNWSSESENESENN(W|ESENN(ENN(WSNE|)EEN(NESSSWSSW(NN|SW(N|SEENENNENEENESSSSWNNWSSSSEESSEEENENNE(NNWNENNWWS(WNW(SSESWSS(WW|ENE(E|NN|SSWWSE))|NNESENENWNWNWWNEEENWWWNNWSW(WWSEEESSWSSW(SEEE(NWNEESE(WNWWSEWNEESE|)|SWWSWN)|WNENN(WWSEWNEE|)E)|NNENESENESSS(WNSE|)EESSS(W|E(S(SSSWENNN|)W|NNNNNNWNENWNENWNENWNENWNNE(NNNNWWSWNNNWWNEEEENE(NNWSWSWNNNNES(EENNW(NWSWWNNE(ENEE(NWWWSWNNNEEES(ENNWWWWWNENENENNNNWSWWSSS(ENENWESWSW|)WNNNNNNN(WSWNWSWNWWWSEESEESESSE(NNNWESSS|)SWSESWWNWNENWN(WN(WSSWNWWSWWNWSSEEESEEEE(N(WWWNSEEE|)N|SWSESSSSSSSSEESSSSSSSEENNE(EENNNNWWWNENWW(SSSSS(EEENNWSWN(SENESSNNWSWN|)|SS)|NENWNENEE(NWWNN(WSSWS(E|W(NNN(ESNW|)N|SESWSESW(ENWNENSWSESW|)))|E(NEWS|)S)|SSS(WNNSSE|)SS))|SSSEESSWSWSEENESSWSSEE(SSSSWNNWSWNWWW(SEESSESW(SEEENN(W(NWES|)S|ESSSSSEN(SWNNNNSSSSEN|))|WNNWSSWW(EENNESNWSSWW|))|NEENNE(SSEEWWNN|)NWWWWSES(ENSW|)WSWWNNNNWSWWNENWNENESES(W|ENEESWS(WSSSNNNE|)EENNEN(E|WNWSWWWNNE(SEWN|)NWNNNWSWNWNWNEEE(ES(E(N|SSS)|WW)|NWWNWWWWWSESESSWWSESWSWNNNNN(ESEWNW|)WSWNWSWWWWNEENWWWSSSEEEESENESE(N|SWWWSESEE(NWES|)SESSES(WWNNWSWSESWS(WNNNWNNE(SENEWSWN|)NWWWNNESENNWWWWNWSSSSSWSWNWSSSWWWWSEESSSENNNESEENENWN(WSSNNE|)EESSEESEE(SS(ENSW|)WNWSSWNWWN(EN(ESNW|)W|WWWSEESEESWWSSESWWWSSWNNWNWSSESWSSSE(ENN(WSNE|)EEES(ENNWN(WSNE|)EENNE(N(NEWS|)WW|SSE(S|N))|WW)|SSWNW(SSSE(SW(WNSE|)SS|N)|NNW(SWWEEN|)NNNE(NNNEENN(ESENESSSWWNE(WSEENNSSWWNE|)|WSWWWSWNWWWWNWWSWWWWNEENWNENNNWNWNEENNWWNNNEEESWS(WNSE|)ESSSS(W|SESEENESSESSW(SEEEENNNE(NWWNWW(SESESSWN(SENNWNSESSWN|)|NNWSWW(WNEENENNNEESWSSENENENWNWWNNNWWWNEENENWWNWNEESEENESEEEESESWWWSESWSSEEEENWW(NNESEEESSSE(NNNEE(SWEN|)NWNENWNEENWNWWNNNENESESESS(WNWNWS|ENNESSSWSSW(NN|WSEEEENWNEENWNNNNWNEEESSSW(NN|SESSENNNNNESEENENE(NWWSW(WNNE(S|NNNWSWNWNENEN(WWWWSE(SSWNWNNWSWNWSWSSWSESENNEE(NWWEES|)SSSEEENE(NWWW(SEWN|)N|E(SWS(ESNW|)WWWWWS(ESWENW|)WNWN(EENNSSWW|)WWS(WS(WSESSSWNNWNNNENNWNWSWWSWSWNWWWSESSSWWNENWWNNNNWWSWSWWWNWWWWWSESWWWNWWWNWSWSWWNNE(NE(S|NWNNN(WWWSWNWSWW(SSWSEEEENWWNEEEEE(NWES|)SSWW(NEWS|)SWSWNWWSSWSSESESSEENNNNWW(SESSNNWN|)(W|N(N|EEESE(SWSSEEESEESESENNEENNWSWNWNWSW(SEESNWWN|)NWN(EENESEE(NWES|)S(ENESSSSEESEEEENNWSWWNWNNW(NEESSE(EEENNWN(EESESSW(N|SWSSENENEENN(W(S|NENW(NENSWS|)W)|ESSEES(ENENNEN(WNSE|)EESSENNN(W|E(N(E|W)|SSSSSE(N|SS(SENNEE(SWSSS(WNWS|ENN)|E)|WNWWNENWWN(WSS(ESWENW|)W|N)))))|WWWWSWSESWSE(E(E|N)|SWWNWNENWWSSWWSWWWWSEESEESWWSWNNWSSSSESWSWWNNNNE(NNNNWSWWSSSSE(NNENWESWSS|)SWSWNWSWSWNWSWW(SEESENESENNESEE(SENEEESSWSSENENNNN(NNESEE(S(EE|WSESWW(SEEESESWWNWWSWSWWSSSESWWWWSEESSESW(SEE(S|EENWWNEENENEESSSEEENENESESSS(ENNNNWNN(EES(W|E(SWSEENNEE(SWSSWENNEN|)N|N))|W(N|WS(WSWSWNNN(E(S|E)|WWWWW(S(WWSEEWWNEE|)E|NNWNEESSENNN(W|ES(ENSW|)SS|N)))|E)))|WWW(S|WWWW(N(NW(NENSWS|)S|EEEEEENW(ESWWWWEEEENW|))|S))))|WNWN(WSWWNWSWWWNWNW(NEEES(SENNESEE(NE(S|NENENWWSWSW(W|NNENWN(NNEE(NWES|)ESSS(WNWNEWSESE|)ENNE(N(NEWS|)W|SSSSSW)|W)|S))|S)|W)|SWNWWWSSEE(NWES|)EESWSSEE(SWWSWWSSENESEENN(WSNE|)ES(ENSW|)SSSWS(EENEEWWSWW|)WNN(E|WWSWWSWSWSSEEN(W|ESSS(WNWWW(NWWWNNEN(WWWSESWS(E|W(SE|NWW))|EE(SSW(W|N)|ENNE(E(NNWWWWNEENWWNWWWN(EEEESEEEES(WSWNSENE|)ENNWN(WWNWSSEE(WWNNESNWSSEE|)|E)|WW(SW(S(W|SES(WSNE|)ENN(EESS(WNSE|)E(SSEE(SWWEEN|)N(EE|W)|NN)|W|N))|N)|NN))|E)|S)))|SEES(SSSSS(WWW(S|N(EENSWW|)WSWN(NEWS|)WSW(SEWN|)N)|E)|WW))|ENNE(SSSWSS|NWNN(WSWENE|)E(SESNWN|)N))))|N(N(ESNW|)N|W)))|E))|NN))|NNW(N(WSWWEENE|)ENENNE(NWWS(S|WW)|ESEE(NWES|)S(WWWNSEEE|)ESE(SWW(SEESWSWN(SENENWESWSWN|)|N)|ENNW(W|S)))|S))|W)|N(W|N))|WWW(S|NWNEESEEENWNW(NENNWNENWNWNENWWWSSSE(ESSS(SSWNNWWSWW(SWNWSSSENE(SSWS(E|WSW(SSE(EE|N)|W(NEN(NNWWWEEESS|)E|WW)))|EEN(ENSW|)W)|NNE(NWNWNEESE(SEESWW|NNWNWWNNWSWNWNENEEEN(ESE(NNWNENENWWS(NEESWSNENWWS|)|ESSWWS(E(S|EE(NN|EEEEESWWSES(SEENWNENESEN(ESSWWSESWSSSWWW(NENE(NWWSNEES|)S|SESEEN(EENNN(WSSNNE|)NNENE(S|EN(NNEEESWWSEEENEES(ENSW|)WSWWWW|WW))|W))|NWWNWW)|W)))|WNN(EE|WW)))|WWWW(WWS(E(E|SWSSE(ESES(WWNWESEE|)E(EE|N)|N))|WNWNNNWWW(SSSENE(NWES|)S|WW))|N)))|S))|E)|NN)|S)))|SSS))|S)))|WSS(E|WNNN(WSNE|)E))|S)|SS)|W)|WSS(W|E))|NN(N|W))))|N(E|WW))|ESES(W|ENEN(ESSWSEEENNESSS(EENWNNESEENN(ESSESWWWSEEESENENNNESENN(WWWS(WNSE|)SS|ESSENESSSW(NWWWEEES|)S(SS|EENNNESEEENNN(EESWSS(EEN(W|NEEN(ESE(NEWS|)SWWSW(SEE(S(WSNE|)E|N)|N)|WW))|SWWSWNWS(NESENEWSWNWS|))|WSW(SEWN|)WN(E|W(WW|S)))))|W(S|WWWWWSS(NNEEEEWWWWSS|)))|WWWW(SEEES|WWNE))|WW))))|S)|E)|E)|E))|E)|EESWS(ESEE(NNN(WSSNNE|)EESSW(SEENEWSWWN|)N|S)|W)))|S)|SSEEE(ESWWSESSWNWNWWWWW(SEESWS(W(N|SWS(E|WNN(WSSWSNENNE|)E))|EEEE(NWWNEWSEES|)EEE(SWEN|)NNN)|NEEE(N|EE))|NWN(WSNE|)E)))))|SWWWWN(EENNSSWW|)WWSESWSSENESE(NN(W|EEESWW)|SSWNWSWNWWW(NEEN(NNNWNNNNNN(EE|WWSESSW(NW|SESW))|W)|WSEESEN(SWNWWNSEESEN|))))|W)|S))|SSE(SWEN|)NE(NWES|)S)|WWNE(NWWSSW(S|NNN)|E))))|SS))))|NNW(NNWW(SESWENWN|)W(W|NE(EE|NNW(NEWS|)S))|S))|E)|SESSSSSSS(WWNENNN(SSSWSEWNENNN|)|EENWNEEES(ENNNE(SSEEEWWWNN|)NWWWWSEESWWWNNNENNNE(NNWSWNNEENNN(NW(NNN(W|E)|SSSW(WSSW(NWES|)SESSE(S|N)|NN))|ESEESWSW(S(EENSWW|)S|N))|SSS)|W)|S)))))))|N(NNNE(S|N)|W))))|E)|E)|ESES(SWNSEN|)EENEE(NWWW(W|S)|SWSSE(SSSW(SS(ENSW|)W(N|W)|NN)|N)))|WW)|S(S|W))|S)|S)|S)|SSWS(WNSE|)E)|S)))))|E)|SSSWSESWSESSWSSE(SSWNWNWSWNNWNEEE(SWEN|)N(WNWSWWWSSE(N|SWWNNWSWWWSWWNWWNNENWNEEEEESSS(ENEENWNW(NNESENEE(SES(SWWN(W|E|N)|EEE(NWWEES|)S)|NWWNN(NN|WSSWWSSWNNN(WSWSS(ENSW|)WWW(NENN(WSW(NWNWW(SEWN|)NNNNE(SSS|EEEENWNNESE(NENWWEESWS|)S)|S)|E(ENEWSW|)SS)|SSSWW(NEWS|)WWWWSWWNNNN(EE(SWS(S|E)|E)|WNNNWWSESWSWNWWNNNWWNNENWWSSSSSWWWNNENWNNNN(WSSSWWWNWNEENNN(NWSSWNNWN(W(NWWWN(EENNESE(S(W|S)|E)|WSWNN(N|WSSWNWSSEEE(SSWSSS(ENNESNWSSW|)WNWWWWNNNWSWWNWWW(NEEENNWNEESENEE(NWWWNWSWWNN(ESNW|)NWSWSESW(WNNWNSESSE|)SSENESS(W|E)|SESWW(N|WWS(S|EEEESSES(WWNNSSEE|)ENN(E|W))))|SWSEENESESEE(NWES|)SWWSWWSWNWSWNNEN(ESEENW|WN(N|WSWW(NEWS|)SWSSSEENE(SSWWSEEENNEESWSSSSEENESSSSS(WSWNWW(NNEN(WNWNN(ESNW|)WSSWNW(NEWS|)S(WN|SE)|EESSW(W|N))|WSES(WSWWWSESENEE(SSW(N|SWW(N(E|WNWWN(NESNWS|)W(W|SSEESE))|SEESWWSESSW(N|S(W|EEEESSSENNEENENNEENESSENNENE(NNW(NEWS|)SW(N|WS(WNWSW(N|WWWSSWNNNW(NEESNWWS|)SSWSSE(EEE(SWEN|)ENWNEEE(WWWSESNWNEEE|)|N))|E))|SESWWSEEESWS(EENENEEE(SWWEEN|)NNWWNWSS(W(S|WNN(E(NEEE(NWNSES|)S|S)|W))|EE)|WSWWNN(WWSSS(ENNSSW|)WNN(NNEWSS|)WSSWNWSS(WWW(NNNWSNESSS|)S|EE(SW(SEWN|)W|E))|E(S|E))))))))|N)|E(N|EE)))|ENESENENENWNNEENWNE(NWNWWNW(WWSWSSWS(S|EEEEE(SWWSEESWWSEE(WWNEENSWWSEE|)|ENWWWN(WSNE|)E(NWES|)EE))|NEESENN(EESWENWW|)W)|EES(E|SW(SWWEEN|)N)))|NNWSWS))))|EEEE)|E))|SSSE(S(EE|SSWWW(WSSSSSEESENESEESWSSESWSWNWNNE(S|NWWSSWSWWSSW(SESS(W(W|N)|ENEEESEEESSESWWS(WWNNE(N(WWNW|ES)|S)|EEEENWNEENENENENNEESWSSENEESEENESSENESESSSENNNNWNEENWWWSWNN(EEEEEEEEE(SSWSWNWN(WSSESSESENN(W|ESEENWN(W|EN(WNEWSE|)EEEENESSSSSWNNNWSWW(NEWS|)SSEE(NWES|)SWSSWNNWWSSSWSSESWWSSWNNWNEENNNWWWWN(WSSESE(EN(ESNW|)W|SWSSSSEE(SSEEEEESESESWWWSSSSSEENWNNEN(EENENESSENENEENENNNWWWNWSWSWNNWNWSSWS(WWNENWW(NEENNEENN(ESSES(WWWSSNNEEE|)EENENWW(S|WNNN(WSNE|)NESSES(W|EESEEEENENENNE(NWWSWWNENNE(EESWWEENWW|)NWWSWWWWSW(NNN(N|EEEE(SWWWEEEN|)N)|SESWSEES(W|EEE(SWWEEN|)N(WNNWW(NEEE|SES)|E(S|E))))|SSSSSSWNW(NENSWS|)SWWSWWW(W(NENEE(SWEN|)EE|WW(W|S))|SEEEENESESSSWWSW(NNNEESW(ENWWSSNNEESW|)|SSSESSSSWSSEEEE(SSWWN(WWSESWWSEESWS(WWN(NWSSWNNWNWSSWWNNE(NNNNWNENWW(SSSSWWWSWNNEN(EESWENWW|)WWSWSESWSWNWWSWSSES(EEENESENEES(W|EE(EEEENSWWWW|)NWNNE(N(ENNSSW|)WWSWS(WW(NEWS|)WWSWN(W|N)|E)|S))|WWWWWNENENE(SSWENN|)NNE(S|ENWNWSWSWWNNWSWWSEESEE(E|SWWS(SSWWNENNNWSSWNWWSESWS(EENSWW|)WNWSWNWWS(WNWSWWNNWNWNNEENEEEESWWWSEEEESES(EENWNWNNW(NENESSSESEEENNWSWNNW(S|NNENESS(EES(ENNEEEEENWNWWNNNENEENWNWSWSWSSWNNNENWNNEENENNENWWNENEN(ESS(W|SESSW(WSSES(E(NNWESS|)S(EESWWSESWSESSW(SSS(WWW(S(S|E)|WW)|ENEN(NNESEESWSES(ENNNNNNN(ESEWNW|)WSSW(SEWN|)NWSWNNEE(WWSSENSWNNEE|)|WW(WS(E(SWSEWNEN|)E|W)|NN))|W))|WN(NW(WSE|NE)|E))|W)|WW(N|W(W|S)))|N))|WNENWN(WSWSSS(ENNSSW|)WWNENWWNWWNEN(WW(SSWN(WSWSSESEENEN(ESESWSSESWWNN(N|WSWNWWNW(N|SSESE(ESWWW(SEESENESENEESSE(NNENE(ENWNNWW(W|SESWSWWWWN(SEEEENSWWWWN|))|S)|SWWSESWSESWWSES(WWNWSWWSEE(SWWWWWWWNENNEEE(EENNWWWNEEENNEEN(E(ENSW|)SSSSWW(NNES|SE)|WWWWWWN(WWSSWWWWW(SEESESSESE(NNWNN(W|ESESSE(NNNN(W(S|N)|EES(ENSW|)W)|EEE))|SWSWNNWSSSESWSS(ENE(S|EEN(WWNSEE|)EES(ENEWSW|)W)|WSESWSSSWS(EENN(ESESWENWNW|)N|WNWNNNENE(SSSWNSENNN|)NWWWNWWWSESWSSSSWS(EENNNESSSE(E|NNNNN(E|W(SWEN|)N))|WNNWSSWNNNENEE(S(S|W)|NNNWSWS(E|WNW(SS(W(SEWN|)N|E)|NNNEN(EESWS(SWNSEN|)EENNENNESENEESWSSENESESS(WNW(WWWN(NES|WS)|S)|ENNNWNWNEE(S|NENWW(SWW|NE)))|NWSWNWWWNWNEESEENWN(E|WWN(WSNE|)E)))))))))|NWN(EESEEENWN(E(E|NNNN)|W(S|WW))|WW))|E(N|EE)))|SWWSEE)|E)|ENE(NNNN|ESE(N|S(WW(SWNSEN|)N|EE)))))|N)|N)))|WW(W|S))|N)|N)|E(N|ES(W|E(SW|NES))))|E))|WW)|W))|S)|WWNWSWNW(WNWESE|)SS)|E)|E))))|N(EEN(N|WW|ESENENESENE(SESSWNWWWSWSW(N|SSENENESEE(NWNWESES|)SWSWW(NEWS|)S(WWNEWSEE|)SEEN(ENSW|)W)|N(WW|N)))|W))|S)|E)|EEENWNEN(ESSSNNNW|)W)|E)|NNWSW(W|NNEENNNWW(SESWENWN|)NN(WSNE|)NESE(SWEN|)NNNNNNW(ESSSSSNNNNNW|))))))))|WW(NN|S(W|E)))|SSWWNE)|ES(SE(EN(WNNSSE|)ESE(NEN(W|EESWSW)|S)|S)|W))|W)|NNW(N|S)))|NEN(NW(S|N(N|E))|ESS(W|ENESE(NNEEWWSS|)S)))))|EE)|NWWWWW)|NNWSSSWW(NENWNENN(E(SENSWN|)N|WSWNWN(WNW(NNESNWSS|)SWWN(E|WWWNWSSW(NNNENN(ESSNNW|)WWWSE(SW(SEWN|)WNNN(WWSESWW(SEEWWN|)NN|E)|E)|S(W|ESWSSSW(SWS(EENEENNW(NEEENEN(ESENESESESW(SSENSWNN|)WNWSWNWSSWW(NEWS|)SE(E|SWWS(W(WSEEWWNE|)N|E))|WWSWNNEE(WWSSENSWNNEE|))|S)|WNWWNE(NW(N|WSW(SEWN|)N)|EE))|N))))|E))|S))))|WNENNEENENNWW(NNNN(W(S|WW)|N)|S(WS(WSSNNE|)E|E))))|NNE(SENSWN|)N))|N))|EEE)|ESSSSW)|EENEN(EESENE(SSWS(WWW(NE(E|N)|WWSSE(SSSWENNN|)N)|SSS(W|ENNNES(SSSSSWNN(SSENNNSSSWNN|)|EN(ES|NW))))|NN(NWSSWWNN(WSSNNE|)NE(SS|N(NEWS|)W)|E))|W))))|EE)))|S)|WW(S|NENWWSSW(ENNEESNWWSSW|))))|E)|N))))|WW)|W)))|W)|W)|S)|WNWNWW(SE|NEE))))|S)|SW(NWES|)S(SS|E))|W)|NN(ESNW|)WW)|W)|E))))|S)|S)|W)))|SWWWSS(WWS(E|WN(WSS(WWWSSWS(WNNWNE(ESNW|)NWN(WWSWSEE(SWWSWW(NENNNNN(ES(S|EEENWNWS(NESESWENWNWS|))|W(N|SSSS))|SEES(WWW|E(SWSEWNEN|)NEE(NWWEES|)S(W|EE)))|N)|E)|EE(NN|E))|E)|N))|EEEN(E|WW)))))|WNNNNWWSWWSS(ENEENSWWSW|)WWNWSS(E|WNNW(W|NEENN(WSWNSENE|)EEES(WS(WNSE|)S|ENNNWNENN(WWWWSSESE(S(WWNSEE|)E|NN(W|E))|EESSSW(SSENEE(N(W|E(EE|S))|S(SSSEWNNN|)W)|NN))))|SS))|W))|SS)))|N(N|W))|EEEEN(ESS(E(N|EES(W|ES(WSNE|)EE(NWNENWWS(NEESWSNENWWS|)|S)))|WW)|W))|S)|NNW(N|S))|ENENEESEEN(EESWSWWSS(ENEE(E|N)|WNNW(SSSWENNN|)(W|N))|WN(WWWWSNEEEE|)E)))|N)|W)|NNWNWNW(SSESEWNWNN|)N(N|WWW|EEEE(SSWNWESENN|)ENN(WSWENE|)EEN(W|EEE(NNWW(SEWN|)NEN(ESNW|)W|SWWSSW(NWSNES|)SESSS(W(NN|SS)|ENN(EE|NNN))))))|E))|EE)|EEE(ESWS(EENNSSWW|)S|N(N|W)))|N))|W))))))))))|SEES(W|E)))|S))|SSSS)|SESESSWSSSEESESSSENNENNEESWSEEENWNEEENWNWNWWWSWNWNNNN(WSSSW(NNWESS|)SESS(WNWSNESE|)E(N|S(S|W)|EEENESE(WNWSWWEENESE|))|ENWNENESSSENNNNENEEESESWSSSWNNNNWSSSW(NN|SSSES(WWWNENWWSS(NNEESWENWWSS|)|ESEES(ESWSSESESWWNWNWSSWWSWWN(WSSWWWSESENEESWSWWSWWSS(WWNENWNENNNNW(NNN(NNNNN(E|N)|EESS(WNSE|)E(N|SWSSSESW(ENWNNNSSSESW|)))|SSS)|EEEN(ESENESEEEENNENWNWNWSWNW(SSS(W(WW|N)|ENESS(ENNSSW|)W)|N(W|EEEN(E(SSESESSESS(WWNEWSEE|)EEEEENNNWWSWW(SEEENSWWWN|)NWNNNW(N(WSNE|)EESSEENNE(SESWS(WW(W|S)|EESESSS(WNNSSE|)EENWNNE(ES(SESWENWN|)W|NW(W|NNN)))|NWW(SS|WN(NWN(ENWNEE(NENWNEENE(NENEENWWWNENNWSWNWNNWWN(NNNESSSENNEEENEN(WWSWWEENEE|)EEESWWSESSSSENNNEE(NNW(SWEN|)NNWWW(W|NE(NNNNWSSS(NNNESSNNWSSS|)|EE))|SWSESESWW(N|SWWWN(EE|W(NNE(S|NNW(SWNWWSESWSEEN(SWWNENSWSEEN|)|N))|SSEES(ENEE(SWEN|)EEN(WW|E(S|NWNNNNWSS(NNESSSNNNWSS|)))|SS)))))|WSSESSWNW(SSESWSEESES(WWNWW(SSE(N|S(WWNWN(WNSE|)E|SENNESS(NNWSSWENNESS|)))|NN)|ENNE(S|NWN(NW(SS(WNSE|)S|NN)|E)|E))|WN(WW(N|WWWWS(SWWSNEEN|)E)|E)))|SSSS(ENNESS|W(NN|W)))|S)|W)|EE)))|S)|N)|W)))|WW))|E)|W)))))))|S)|W)|SEE(S(W|SS)|E)))|EESEE(SWWWNSEEEN|)NWN(NE(NN(ENSW|)W(W|S)|S)|W))|EE)|WSWWWNW(W(W|N)|S)))))))|W(S|W))|WSSS(WW(NENWESWS|)S(SWNNWSSWNWN(WSNE|)E|E)|E))$
    """.strip()
    main(input_data)
