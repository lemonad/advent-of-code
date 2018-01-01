import json
import unittest

from december12 import Solver


class TestDec12(unittest.TestCase):

    def test_examples_for_part_one(self):
        self.assertEqual(Solver.sum_json(json.loads('[1,2,3]')), 6)
        self.assertEqual(Solver.sum_json(json.loads('{"a":2,"b":4}')), 6)
        self.assertEqual(Solver.sum_json(json.loads('[[[3]]]')), 3)
        self.assertEqual(Solver.sum_json(json.loads(
            '{"a":{"b":4},"c":-1}')), 3)
        self.assertEqual(Solver.sum_json(json.loads('{"a":[-1,1]}')), 0)
        self.assertEqual(Solver.sum_json(json.loads('[-1,{"a":1}]')), 0)
        self.assertEqual(Solver.sum_json(json.loads('[]')), 0)
        self.assertEqual(Solver.sum_json(json.loads('{}')), 0)

    def test_examples_for_part_two(self):
        self.assertEqual(Solver.sum_json(json.loads(
            '[1,2,3]'), exclude_red=True), 6)
        self.assertEqual(Solver.sum_json(json.loads(
            '[1,{"c":"red","b":2},3]'), exclude_red=True), 4)
        self.assertEqual(Solver.sum_json(json.loads(
            '{"d":"red","e":[1,2,3,4],"f":5}'), exclude_red=True), 0)
        self.assertEqual(Solver.sum_json(json.loads(
            '[1,"red",5]'), exclude_red=True), 6)

    def test_solution(self):
        s = Solver(from_file='input/dec12.in')
        (one, two) = s.solve()
        one_alt = s.solve_part_one_alternative()

        self.assertEqual(one, 191164)
        self.assertEqual(one_alt, 191164)
        self.assertEqual(two, 87842)


if __name__ == '__main__':
    unittest.main()
