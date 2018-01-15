"""
December 23, Advent of Code 2015 (Jonas Nockert / @lemonad)

Runs the given code in a virtual machine using Python bytecode.

NOTE: Currently can't be run with pypy as it only supports 3.5 and
bytecode structure was changed significantly with Python 3.6. Now
all instructions are two bytes and EXTENDED_ARG instructions need
to be used to provide arguments > 255.

"""
import opcode
import types

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def create_program_bytecode(self):
        """Creates a program emulating the given assembler code.

        Returns tuple of bytecode, constants, variable names.

        The program will take two arguments (registers a and b) and
        returns a tuple of a and b.
        """
        consts = (None, 0, 1, 2, 3)
        varnames = ('a', 'b')
        b = bytearray()
        line_no = 0
        line_offsets = []
        jump_table = []

        # Create byte code for the given program and fills in the
        # jump table for later filling in.
        for op, args in self.as_instructions():
            # Store address to start of instruction for jumps.
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

        # Out of bound jumps will be pointed here. Returns a tuple
        # of registers a and b.
        the_end = len(b)
        ixa = varnames.index('a')
        ixb = varnames.index('b')
        b.extend([opcode.opmap['LOAD_FAST'], ixa])
        b.extend([opcode.opmap['LOAD_FAST'], ixb])
        b.extend([opcode.opmap['BUILD_TUPLE'], 2])
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

        return b, consts, varnames

    def create_function(self):
        """Create function out of bytecode."""
        bytecode, consts, varnames = self.create_program_bytecode()
        # TODO Fill in co_lnotab so exceptions report proper line numbers.
        # https://svn.python.org/projects/python/branches/pep-0384/Objects/lnotab_notes.txt
        code = types.CodeType(
                2,  # co_argcount (registers a and b)
                0,  # co_kwonlyargcount
                len(varnames),  # co_nlocals
                100,  # co_stacksize
                67,  # co_flags
                bytes(bytecode),  # co_code
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
        return types.FunctionType(code, {})

    def solve(self):
        runvm = self.create_function()
        _, res1 = runvm(0, 0)
        _, res2 = runvm(1, 0)
        return (res1, res2)


if __name__ == '__main__':
    import time
    start_time = time.time()
    s = Solver(from_file='input/dec23.in')
    (one, two) = s.solve()
    print("--- %.5f seconds ---" % (time.time() - start_time))
    print("Value in register b after completion? %d" % one)
    print("Value in register b when a starts as 1? %d" % two)

    assert(one == 184)
    assert(two == 231)
