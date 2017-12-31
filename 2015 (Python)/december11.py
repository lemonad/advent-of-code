"""
December 11, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
import string

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    PASSWORD_LENGTH = 8
    ALPHABET_LENGTH = 26

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def valid_password(password):
        """True if password is valid."""
        def no_ilo(password):
            """May not contain letters i, o, or l."""
            ilo = 'i' in password or 'l' in password or 'o' in password
            return not ilo

        def three_chars_in_order(password):
            """At least three characters in order, e.g. abc, ..., xyz."""
            found = False
            for i in range(len(password) - 2):
                x1 = ord(password[i])
                x2 = ord(password[i + 1])
                x3 = ord(password[i + 2])
                if x3 == x2 + 1 and x2 == x1 + 1:
                    found = True
                    break
            return found

        def two_different_pairs_of_letters(password):
            """Contains at least two different, non-overlapping pairs of
            letters, like aa, bb, or zz.
            """
            counter = 0
            for p in string.ascii_lowercase:
                if p * 2 in password:
                    counter += 1
                if counter >= 2:
                    return True
            return False

        return (no_ilo(password) and
                three_chars_in_order(password) and
                two_different_pairs_of_letters(password))

    @staticmethod
    def next_password(password):
        """Generates next consequtive password based on previous password."""
        # 8-character password -> integer
        val = 0
        for c in password:
            val = val * Solver.ALPHABET_LENGTH + (ord(c) - ord('a'))

        # Loop until a valid password is found.
        while True:
            val += 1  # Equivalent of 'abc' -> 'abd', 'abz' -> 'aca', ...
            val_tmp = val
            password = ''
            for i in reversed(range(Solver.PASSWORD_LENGTH)):
                c = int(val_tmp % Solver.ALPHABET_LENGTH)
                password = chr(c + ord('a')) + password
                val_tmp = int(val_tmp / Solver.ALPHABET_LENGTH)
            if Solver.valid_password(password):
                break

        return password

    def solve_part_one(self):
        """Solution for part one."""
        return self.next_password(self.puzzle_input)

    def solve_part_two(self, password):
        """Solution for part two."""
        return self.next_password(password)

    def solve(self):
        one = self.solve_part_one()
        two = self.solve_part_two(one)
        return (one, two)


if __name__ == '__main__':
    s = Solver(from_str='hxbxwxba')
    (one, two) = s.solve()
    print("Santa's new password: %s" % one)
    print("Santa's next password: %s" % two)

    assert(one == 'hxbxxyzz')
    assert(two == 'hxcaabcc')
