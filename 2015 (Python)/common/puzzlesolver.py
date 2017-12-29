"""
Abstract base class for advent of code puzzle solvers.

"""
from abc import ABC, abstractmethod
import re


class PuzzleSolver(ABC):
    def __init__(self, from_file=None, from_str=None):
        if not (from_file or from_str):
            raise ValueError('PuzzleSolver needs to be initialized from '
                             'either file or string.')
        elif from_file and from_str:
            raise ValueError('PuzzleSolver ambiguous initialization.')
        elif from_str:
            self.raw_puzzle_input = from_str
        else:
            with open(from_file) as f:
                self.raw_puzzle_input = f.read()

    @abstractmethod
    def solve(self):
        pass

    @property
    def puzzle_input(self):
        return self.raw_puzzle_input

    def chars(self):
        for c in self.raw_puzzle_input:
            yield c

    def lines(self):
        for line in self.raw_puzzle_input.split():
            yield line

    def lines_match(self, pattern):
        for line in self.raw_puzzle_input.split():
            m = re.search(pattern, line)
            yield m

    def lines_split(self, split_str):
        for line in self.raw_puzzle_input.split():
            yield line.split(split_str)
