import unittest

from december25 import Solver


class TestDec25(unittest.TestCase):

    def test_sum_of_natural_numbers(self):
        self.assertEqual(Solver.sum_of_natural_numbers(1), 1)
        self.assertEqual(Solver.sum_of_natural_numbers(2), 3)
        self.assertEqual(Solver.sum_of_natural_numbers(3), 6)
        self.assertEqual(Solver.sum_of_natural_numbers(4), 10)
        self.assertEqual(Solver.sum_of_natural_numbers(5), 15)
        self.assertEqual(Solver.sum_of_natural_numbers(6), 21)

    def test_code_number_given_row_and_column(self):
        self.assertEqual(Solver.code_no_for_row_col(1, 1), 1)
        self.assertEqual(Solver.code_no_for_row_col(2, 1), 2)
        self.assertEqual(Solver.code_no_for_row_col(3, 1), 4)
        self.assertEqual(Solver.code_no_for_row_col(4, 1), 7)
        self.assertEqual(Solver.code_no_for_row_col(5, 1), 11)
        self.assertEqual(Solver.code_no_for_row_col(6, 1), 16)
        self.assertEqual(Solver.code_no_for_row_col(1, 2), 3)
        self.assertEqual(Solver.code_no_for_row_col(2, 2), 5)
        self.assertEqual(Solver.code_no_for_row_col(3, 2), 8)
        self.assertEqual(Solver.code_no_for_row_col(4, 2), 12)
        self.assertEqual(Solver.code_no_for_row_col(5, 2), 17)
        self.assertEqual(Solver.code_no_for_row_col(1, 3), 6)
        self.assertEqual(Solver.code_no_for_row_col(2, 3), 9)
        self.assertEqual(Solver.code_no_for_row_col(3, 3), 13)
        self.assertEqual(Solver.code_no_for_row_col(4, 3), 18)
        self.assertEqual(Solver.code_no_for_row_col(1, 4), 10)
        self.assertEqual(Solver.code_no_for_row_col(2, 4), 14)
        self.assertEqual(Solver.code_no_for_row_col(3, 4), 19)
        self.assertEqual(Solver.code_no_for_row_col(1, 5), 15)
        self.assertEqual(Solver.code_no_for_row_col(2, 5), 20)
        self.assertEqual(Solver.code_no_for_row_col(1, 6), 21)

    def test_example_codes(self):
        self.assertEqual(Solver.code_for_row_col(1, 1), 20151125)
        self.assertEqual(Solver.code_for_row_col(2, 1), 31916031)
        self.assertEqual(Solver.code_for_row_col(3, 1), 16080970)
        self.assertEqual(Solver.code_for_row_col(4, 1), 24592653)
        self.assertEqual(Solver.code_for_row_col(5, 1), 77061)
        self.assertEqual(Solver.code_for_row_col(6, 1), 33071741)
        self.assertEqual(Solver.code_for_row_col(1, 2), 18749137)
        self.assertEqual(Solver.code_for_row_col(2, 2), 21629792)
        self.assertEqual(Solver.code_for_row_col(3, 2), 8057251)
        self.assertEqual(Solver.code_for_row_col(4, 2), 32451966)
        self.assertEqual(Solver.code_for_row_col(5, 2), 17552253)
        self.assertEqual(Solver.code_for_row_col(6, 2), 6796745)
        self.assertEqual(Solver.code_for_row_col(1, 3), 17289845)
        self.assertEqual(Solver.code_for_row_col(2, 3), 16929656)
        self.assertEqual(Solver.code_for_row_col(3, 3), 1601130)
        self.assertEqual(Solver.code_for_row_col(4, 3), 21345942)
        self.assertEqual(Solver.code_for_row_col(5, 3), 28094349)
        self.assertEqual(Solver.code_for_row_col(6, 3), 25397450)
        self.assertEqual(Solver.code_for_row_col(1, 4), 30943339)
        self.assertEqual(Solver.code_for_row_col(2, 4), 7726640)
        self.assertEqual(Solver.code_for_row_col(3, 4), 7981243)
        self.assertEqual(Solver.code_for_row_col(4, 4), 9380097)
        self.assertEqual(Solver.code_for_row_col(5, 4), 6899651)
        self.assertEqual(Solver.code_for_row_col(6, 4), 24659492)
        self.assertEqual(Solver.code_for_row_col(1, 5), 10071777)
        self.assertEqual(Solver.code_for_row_col(2, 5), 15514188)
        self.assertEqual(Solver.code_for_row_col(3, 5), 11661866)
        self.assertEqual(Solver.code_for_row_col(4, 5), 10600672)
        self.assertEqual(Solver.code_for_row_col(5, 5), 9250759)
        self.assertEqual(Solver.code_for_row_col(6, 5), 1534922)
        self.assertEqual(Solver.code_for_row_col(1, 6), 33511524)
        self.assertEqual(Solver.code_for_row_col(2, 6), 4041754)
        self.assertEqual(Solver.code_for_row_col(3, 6), 16474243)
        self.assertEqual(Solver.code_for_row_col(4, 6), 31527494)
        self.assertEqual(Solver.code_for_row_col(5, 6), 31663883)
        self.assertEqual(Solver.code_for_row_col(6, 6), 27995004)

    def test_solution(self):
        one = Solver(from_file='input/dec25.in').solve()
        self.assertEqual(one, 19980801)


if __name__ == '__main__':
    unittest.main()
