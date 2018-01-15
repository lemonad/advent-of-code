"""
December 23, Advent of Code 2015 (Jonas Nockert / @lemonad)

Runs the given code in a virtual machine using Python bytecode.

"""
import opcode
import types

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PATTERN = "^(\w+)\s*([^,\s]+)*(,\s*[^,\s]+)*"

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    def runVirtualMachine(self, reg_a=0, reg_b=0):
        ops = []
        for m in self.lines_search(self.PATTERN):
            op = m.group(1)
            args = []
            arg1 = m.group(2)
            if arg1:
                args.append(arg1)

            rest = m.group(3)
            if rest:
                for r in rest.split(','):
                    if not r:
                        continue
                    args.append(r.strip(' ,'))
            ops.append((op, args))

        b = bytearray()
        line_offsets = []
        jump_table = []
        line_no = 0
        consts = (None, 0, 1, 2, 3, reg_a, reg_b)
        varnames = ('a', 'b')

        # Initialize registers a and b.
        ixa = varnames.index('a')
        ixb = varnames.index('b')
        cixa = consts.index(reg_a)
        cixb = consts.index(reg_b)
        b.extend([opcode.opmap['LOAD_CONST'], cixa])
        b.extend([opcode.opmap['STORE_FAST'], ixa])
        b.extend([opcode.opmap['LOAD_CONST'], cixb])
        b.extend([opcode.opmap['STORE_FAST'], ixb])

        # Create byte code for the given program and fills in the
        # jump table for later filling in.
        for op, args in ops:
            line_offsets.append(len(b))
            if op == 'hlf':
                # reg >>= 1.
                vix = varnames.index(args[0])
                cix = consts.index(1)
                b.extend([opcode.opmap['LOAD_FAST'], vix])
                b.extend([opcode.opmap['LOAD_CONST'], cix])
                b.extend([opcode.opmap['INPLACE_RSHIFT'], 0])
                b.extend([opcode.opmap['STORE_FAST'], vix])
            elif op == 'tpl':
                # reg *= 3.
                vix = varnames.index(args[0])
                cix = consts.index(3)
                b.extend([opcode.opmap['LOAD_FAST'], vix])
                b.extend([opcode.opmap['LOAD_CONST'], cix])
                b.extend([opcode.opmap['INPLACE_MULTIPLY'], 0])
                b.extend([opcode.opmap['STORE_FAST'], vix])
            elif op == 'inc':
                # reg += 1.
                vix = varnames.index(args[0])
                cix = consts.index(1)
                b.extend([opcode.opmap['LOAD_FAST'], vix])
                b.extend([opcode.opmap['LOAD_CONST'], cix])
                b.extend([opcode.opmap['INPLACE_ADD'], 0])
                b.extend([opcode.opmap['STORE_FAST'], vix])
            elif op == 'jmp':
                lno = line_no + int(args[0])
                jump_table.append((len(b), lno))
                b.extend([opcode.opmap['EXTENDED_ARG'], 0])
                b.extend([opcode.opmap['JUMP_ABSOLUTE'], 0])
            elif op == 'jie':
                # Jump if TOS (top of stack) is even.
                vix = varnames.index(args[0])
                cix = consts.index(2)
                cix0 = consts.index(0)
                b.extend([opcode.opmap['LOAD_FAST'], vix])
                b.extend([opcode.opmap['LOAD_CONST'], cix])
                b.extend([opcode.opmap['BINARY_MODULO'], 0])
                b.extend([opcode.opmap['LOAD_CONST'], cix0])
                b.extend([opcode.opmap['COMPARE_OP'], 2])
                lno = line_no + int(args[1])
                jump_table.append((len(b), lno))
                b.extend([opcode.opmap['EXTENDED_ARG'], 0])
                b.extend([opcode.opmap['POP_JUMP_IF_TRUE'], 0])
            elif op == 'jio':
                # Jump if TOS (top of stack) is 1.
                vix = varnames.index(args[0])
                cix = consts.index(1)
                b.extend([opcode.opmap['LOAD_FAST'], vix])
                b.extend([opcode.opmap['LOAD_CONST'], cix])
                b.extend([opcode.opmap['COMPARE_OP'], 2])
                lno = line_no + int(args[1])
                jump_table.append((len(b), lno))
                b.extend([opcode.opmap['EXTENDED_ARG'], 0])
                b.extend([opcode.opmap['POP_JUMP_IF_TRUE'], 0])
            line_no += 1

        # Out of bound jumps will be pointed here. Returns value of
        # register b.
        the_end = len(b)
        b.extend([opcode.opmap['LOAD_FAST'], ixb])
        b.extend([opcode.opmap['RETURN_VALUE'], 0])

        # Fill in addresses for all jumps (we didn't have all
        # addresses for forward jumps until now).
        for offset, line_no in jump_table:
            if line_no < 0 or line_no >= len(line_offsets):
                jump_addr = the_end
            else:
                jump_addr = line_offsets[line_no]
            # Most significant byte goes into extended arg instruction.
            b[offset + 1] = jump_addr >> 8
            # Least significant byte goes into jump instruction.
            b[offset + 3] = jump_addr & 0xff

        # Create program out of bytecode.
        # TODO Fill in co_lnotab so exceptions report proper line numbers.
        code = types.CodeType(
                0,  # co_argcount (no function arguments used here)
                0,  # co_kwonlyargcount
                len(varnames),  # co_nlocals
                2,  # co_stacksize
                67,  # co_flags
                bytes(b),  # co_code
                consts,  # co_consts
                (),  # co_names (no globals used here)
                varnames,  # co_varnames
                'vm',  # co_filename
                'runvm',  # co_name
                1,  # co_firstlineno
                bytes(),  # co_lnotab
                (),  # co_freevars
                (),  # co_cellvars
            )

        # Create a function out of the program.
        runvm = types.FunctionType(code, {})
        return runvm()

    def solve(self):
        return (self.runVirtualMachine(),
                self.runVirtualMachine(reg_a=1))


if __name__ == '__main__':
    # assert(Solver.subproblem('') == 0)

    # s = Solver(from_file='input/dec23-sample.in')
    s = Solver(from_file='input/dec23.in')
    (one, two) = s.solve()
    print("Value in register b after completion? %d" % one)
    print("Value in register b when a starts as 1? %d" % two)

    assert(one == 184)
    assert(two == 231)
