"""
December 11, Advent of Code 2016 (Jonas Nockert / @lemonad)

"""
from enum import Enum
from itertools import chain, combinations
import math
import os
from queue import PriorityQueue
import re
import string

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    def solve():
        pass

    def explore(self, floors, elevator_start=1):
        states = PriorityQueue()
        initial_state = (elevator_start, floors)
        initial_hash = self.hash_state(initial_state)
        states.put((0, initial_state))
        check_state = self.get_check_state(initial_state)
        check_hash = self.hash_state(check_state)
        check_steps = set(check_hash)
        steps = {initial_hash: 0}

        while not states.empty():
            h, state = states.get()
            state_hash = self.hash_state(state)
            num_steps = steps[state_hash]
            if self.is_done(state):
                return num_steps

            for new_state in self.possible_moves(state):
                new_cost = num_steps + 1
                check_state = self.get_check_state(new_state)
                check_hash = self.hash_state(check_state)
                if check_hash not in check_steps:
                    new_hash = self.hash_state(new_state)
                    steps[new_hash] = new_cost
                    check_steps.add(check_hash)
                    priority = new_cost + self.heuristic(new_state)
                    states.put((priority, new_state))
        return None

    def hash_state(self, state):
        elevator, floors = state
        hash_str = "%d" % elevator
        for floor in floors:
            hash_str += "%08x" % floor
        return hash_str

    def get_check_state(self, state):
        elevator, floors = state

        counter = 0
        d = {}
        new_floors = []
        for floor in floors:
            new_floor = 0
            for i in range(16):
                if floor & (1 << i):
                    if i not in d:
                        d[i] = counter
                        counter += 1
                    new_floor |= (1 << d[i])
                if floor & (1 << (i + 16)):
                    if i not in d:
                        d[i] = counter
                        counter += 1
                    new_floor |= (1 << (d[i] + 16))
            new_floors.append(new_floor)
        return (elevator, new_floors)

    def heuristic(self, state):
        """Not really an admissible heuristic but works for these problems."""
        elevator, floors = state
        h = 0

        min_floor = None
        for i, floor in enumerate(floors):
            if floor > 0 and not min_floor:
                min_floor = i + 1
            b = bin(floor)[2:]
            h += (4 - i - 1) * b.count('1')
        if elevator > min_floor:
            h += elevator - min_floor

        b = bin(floors[3])[2:]
        h -= b.count('1')
        h = max(h, 0)
        return h

    def possible_moves(self, state):
        """All possible moves from a state."""
        elevator, floors = state

        floor = floors[elevator - 1]
        gens = floor & 65535
        mcs = floor & ~65535
        pairs = floor & (mcs >> 16) | floor & (gens << 16)

        genslist = []
        mcslist = []
        pairslist = []
        for i in range(16):
            genval = 1 << i
            mcsval = genval << 16

            if (gens & genval) and not (mcs & mcsval):
                genslist.append(genval)
            if (mcs & mcsval) and not (gens & genval):
                mcslist.append(mcsval)
            if (gens & genval) and (mcs & mcsval) and len(pairslist) <= 2:
                pairslist.append(genval | mcsval)

        if len(pairslist) > 0:
            # Move one generator.
            move_1 = genslist + [pairslist[0] & 65535]
            # Move two generators.
            move_2 = []
            for m in combinations(move_1, 2):
                move_2.append(m[0] | m[1])
            # Move one microchip.
            move_3 = mcslist + [pairslist[0] & ~65535]
            # Move two microchips.
            move_4 = []
            for m in combinations(move_3, 2):
                move_4.append(m[0] | m[1])
            # Move pair (only makes sense to move Pp and Tt, not Pt or Tp).
            move_5 = pairslist[:1]
            if len(pairslist) > 1:
                # Move two generators.
                move_5.append((pairslist[0] & 65535) | (pairslist[1] & 65535))
                # Move two microchips
                move_5.append((pairslist[0] & ~65535) | (pairslist[1] & ~65535))
        else:
            move_1 = genslist
            move_2 = []
            for m in combinations(move_1, 2):
                move_2.append(m[0] | m[1])
            move_3 = mcslist
            move_4 = []
            for m in combinations(move_3, 2):
                move_4.append(m[0] | m[1])
            move_5 = []

        new_states = []
        for move in chain(move_1, move_2, move_3, move_4, move_5):
            # Can move down?
            if elevator > 1:
                src_floor = floors[elevator - 1]
                dest_floor = floors[elevator - 2]
                src_floor &= ~move
                dest_floor |= move
                new_floors = (floors[:elevator - 2] +
                        [dest_floor, src_floor] +
                        floors[elevator:])
                new_state = (elevator - 1, new_floors)
                if self.is_valid(new_state):
                    new_states.append(new_state)

            # Can move up?
            if elevator < 4:
                src_floor = floors[elevator - 1]
                dest_floor = floors[elevator]
                src_floor &= ~move
                dest_floor |= move
                new_floors = (floors[:(elevator - 1)] +
                        [src_floor, dest_floor] +
                        floors[(elevator + 1):])
                new_state = (elevator + 1, new_floors)
                if self.is_valid(new_state):
                    new_states.append(new_state)
        return new_states

    def is_valid(self, state):
        """True if no microchips are fried by the current state"""
        elevator, floors = state
        if elevator < 1 or elevator > 4:
            print("Elevator invalid: {:d}".format(elevator))
            print(state)
            return False
        if floors[elevator - 1] == 0:
            print("Elevator on empty floor: {:d}".format(elevator))
            print(state)
            return False

        for floor in floors:
            gens = floor & 65535
            mcs = floor >> 16
            if gens > 0 and (mcs & ~gens):
                return False
        return True

    def is_done(self, state):
        """True if all items are on floor 4"""
        elevator, floors = state
        return elevator == 4 and floors[0] == 0 and floors[1] == 0 and floors[2] == 0

if __name__ == "__main__":
    # 4
    # 3                     XG XM RG RM
    # 2            PM    SM
    # 1 E TG TM PG    SG
    #      0 16  1 17  2 18  3 19  4 20
    part1_data = [
            1 << 0 | 1 << 1 | 1 << 2 | 1 << 16,
            1 << 17 | 1 << 18,
            1 << 3 | 1 << 4 | 1 << 19 | 1 << 20,
            0]

    # 4
    # 3                     XG XM RG RM
    # 2            PM    SM
    # 1 E TG TM PG    SG                EG EM DG DM
    #      0 16  1 17  2 18  3 19  4 20  5 21  6 22
    part2_data = [
            1 << 0 | 1 << 1 | 1 << 2 | 1 << 5 | 1 << 6 | 1 << 16 | 1 << 21 | 1 << 22,
            1 << 17 | 1 << 18,
            1 << 3 | 1 << 4 | 1 << 19 | 1 << 20,
            0]

    s = Solver(from_str='...')
    ret = s.explore(part1_data)
    print("Minimum number of steps (part 1):", ret)

    s = Solver(from_str='...')
    ret = s.explore(part2_data)
    print("Minimum number of steps (part 2):", ret)
