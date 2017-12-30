"""
December 7, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PATTERN1 = '^()()(\w+) -> (\w+)'
    PATTERN2 = '^()(NOT) (\w+) -> (\w+)'
    PATTERN3 = '^(\w+) (AND|OR|LSHIFT|RSHIFT) (\w+) -> (\w+)'

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

        # Parse instructions into list of instructions tuples.
        self.instructions = [m.groups()
                             for m in self.lines_search(self.PATTERN1) if m]
        self.instructions += [m.groups()
                              for m in self.lines_search(self.PATTERN2) if m]
        self.instructions += [m.groups()
                              for m in self.lines_search(self.PATTERN3) if m]
        self.reset_wires()

    def reset_wires(self):
        """Sets all wires to not connected."""
        self.wires = {}

    def value_from_wire(self, wire):
        """Return value of wire or None."""
        if wire.isdigit():
            return int(wire)
        elif wire in self.wires:
            return self.wires[wire]
        else:
            return None

    def step(self):
        """Run through the instructions once."""
        for instr in self.instructions:
            op = instr[1]
            v_src1 = self.value_from_wire(instr[0])
            v_src2 = self.value_from_wire(instr[2])

            if op == '':
                if v_src2 is not None:
                    self.wires[instr[3]] = v_src2
            elif op == 'NOT':
                if v_src2 is not None:
                    self.wires[instr[3]] = ~v_src2 & 65535
            elif op == 'AND':
                if v_src1 is not None and v_src2 is not None:
                    self.wires[instr[3]] = v_src1 & v_src2
            elif op == 'OR':
                if v_src1 is not None and v_src2 is not None:
                    self.wires[instr[3]] = v_src1 | v_src2
            elif op == 'LSHIFT':
                if v_src1 is not None:
                    self.wires[instr[3]] = v_src1 << v_src2
            elif op == 'RSHIFT':
                if v_src1 is not None:
                    self.wires[instr[3]] = v_src1 >> v_src2
            else:
                raise ValueError('No such instruction: %s' % instr)

    def solve_part_one(self):
        """Solution for part one."""
        # For my input, once wire 'a' is assigned a value, we're done.
        while 'a' not in self.wires:
            self.step()
        return self.wires['a']

    def solve_part_two(self, value_of_a):
        """Solution for part two."""
        self.reset_wires()

        # Replace override of b with value we got from part one
        # (not sure if other people's puzzle inputs are completely
        # different.)
        ix = self.instructions.index(('', '', '19138', 'b'))
        self.instructions[ix] = ('', '', str(value_of_a), 'b')

        # For my input, once wire 'a' is assigned a value, we're done.
        while 'a' not in self.wires:
            self.step()
        return self.wires['a']

    def solve(self):
        value_of_a1 = self.solve_part_one()
        value_of_a2 = self.solve_part_two(value_of_a1)
        return (value_of_a1, value_of_a2)


if __name__ == '__main__':
    s = Solver(from_file='input/dec07.in')
    (one, two) = s.solve()
    print("Signal ultimately provided to wire a: %d" % one)
    print("Signal ultimately provided to wire a (with '%d -> b'): %d" %
          (one, two))

    assert(one == 16076)
    assert(two == 2797)
