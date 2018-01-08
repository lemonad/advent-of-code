"""
December 20, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from functools import reduce
from itertools import chain, combinations
import operator

from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def factors(n):
        """Given an integer n, return prime factors and their powers.

        `factors(12)` returns `[2, 2, 3]` (note that 1 has no prime factors.)
        """
        primes = []

        # Powers of two.
        while n % 2 == 0:
            primes.append(2)
            n /= 2

        # n is now odd.
        i = 3
        # Every composite number has at least one prime factor less
        # than or equal to square root of itself, i.e. if n = a * b,
        # then a and b can't both be > sqrt(n).
        while i * i <= n:
            while n % i == 0:
                primes.append(i)
                n /= i
            # Only test odd numbers.
            i += 2

        # Do we have a remaining prime factor > sqrt(n)?
        if n != 1:
            primes.append(int(n))

        return primes

    @staticmethod
    def get_count(n, factor=10, limit=None):
        # note we return an iterator rather than a list
        primes = Solver.factors(n)
        powerset = set(chain.from_iterable(combinations(primes, h)
                                           for h in range(len(primes) + 1)))
        prods = [reduce(operator.mul, p, 1) for p in powerset]
        if not limit:
            ssum = sum(prods)
        else:
            ssum = sum([p for p in prods if p * limit >= n])
        return ssum * factor

    def solve_part_one(self):
        """Solution for part one.

        We could have used the same solution as in part two here but
        this is a little bit more interesting, using the formula
        for \sigma_1(n) = prod(sum(p_i^j)):
            https://en.wikipedia.org/wiki/Divisor_function#Properties
        """
        start = self.as_int() // 100
        for n in range(start, self.as_int()):
            prime_factors = self.factors(n)
            prime_set = set(prime_factors)
            count = 1
            for p in prime_set:
                a = prime_factors.count(p)
                count *= sum([p ** i for i in range(0, a + 1)])
            count *= 10
            if count >= self.as_int():
                return n
        return None

    def solve_part_two(self, start):
        """Solution for part two."""
        for n in range(start, self.as_int()):
            # The product of each set in the powerset of prime factors is
            # an elf. So we'll check that the elf * 50 >= puzzle_input,
            # otherwise the elf has stopped at an earlier house.
            count = self.get_count(n, 11, 50)
            if count >= self.as_int():
                return n
        return None

    def solve(self):
        one = self.solve_part_one()
        two = self.solve_part_two(one)
        return (one, two)


if __name__ == '__main__':
    s = Solver(from_str='29000000')
    (one, two) = s.solve()
    print("Lowest house number: %d" % one)
    print("New lowest house number: %d" % two)

    assert(one == 665280)
    assert(two == 705600)
