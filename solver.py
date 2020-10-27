#!/usr/bin/env python
# coding:utf-8

import sys
import math
from itertools import product
import time

ROW = "ABCDEFGHI"
COL = "123456789"
CENTERS = [(i, j) for i in [1, 4, 7] for j in [2, 5, 8]]
TIME_LIMIT = 1.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'puzzles.txt'

class SudokuCSP:
    def __init__(self, board):
        self.board = board
        self.domain = [x for x in range(1, 10)]
        self.variables = {ROW[r] + COL[c]: self.board[ROW[r] + COL[c]] for r in range(9) for c in range(9)}
        self.assignment = {}
        self.num_zeroes = list(board.values()).count(0)

    def solve(self):
        if len(self.assignment) == self.num_zeroes:
            return self

        var = self.select_unassigned(self.assignment)
        for val, conflicts in self.order_domain(var):
            if conflicts == 0:
                self.assign(var, val)
                result = self.solve()
                if result:
                    return result
            self.unassign(var)
        return None

    def count_conflicts(self, var, val):
        """
        Count the number of times this variable:value combination causes a conflict
        """
        if not var:
            return 0
        values = self.get_loc_col(var)
        values += self.get_loc_row(var)
        values += self.get_loc_square(var)
        conflicts = 0
        for value in values:
            conflicts += 1 if value == val else 0
        return conflicts

    def order_domain(self, var):
        self.domain.sort(key=lambda v: self.count_conflicts(var, v))
        return [(x, self.count_conflicts(var, x)) for x in self.domain]

    def select_unassigned(self, assignment):
        variables = [v for v in self.variables if self.board[v] == 0 and v not in assignment]
        if not variables:
            return 0
        return min(variables, key=lambda v: self.remaining_values(v, assignment))

    def remaining_values(self, var, assignment):
        col = self.get_loc_col(var)
        row = self.get_loc_row(var)
        sqr = self.get_loc_square(var)
        legal_domain = []
        for d in self.domain:
            if d in col or d in row or d in sqr or d in assignment:
                pass
            else:
                legal_domain.append(d)
        return len(legal_domain)

    def get_loc_row(self, loc):
        return self.get_row(loc[0])

    def get_row(self, index):
        if isinstance(index, int):
            index = ROW[index - 1]
        return [self.board["%s%s" % (index, i)] for i in COL]

    def get_loc_col(self, loc):
        return self.get_col(loc[1])

    def get_col(self, index):
        return [self.board["%s%s" % (i, index)] for i in ROW]

    def get_neighbors_locs(self, loc):
        x, y = loc
        if not isinstance(loc, tuple):
            x = ROW.index(x)
            y = int(y)
        center = None
        distance = float("inf")
        for c in CENTERS:
            d = self.get_distance(c, (x, y))
            if d < distance:
                distance = d
                center = c
        return ["%s%d" % (ROW[r], c) for r, c in self.get_neighbors(center)]

    def get_loc_square(self, loc):
        return [self.board[x] for x in self.get_neighbors_locs(loc)]

    def assign(self, var, val):
        self.assignment[var] = val
        self.board[var] = val

    def unassign(self, var):
        if var in self.assignment:
            self.assignment.pop(var)
        self.board[var] = 0

    def print_board(self):
        """
        Helper function to print board as a labeled square.
        """
        for a, v in self.assignment.items():
            self.variables[a] = v

        print("\n    1 2 3 4 5 6 7 8 9")
        print("  .-------------------.")
        for i in ROW:
            row = i + ' | '
            for j in COL:
                row += (str(self.variables[i + j]) + " ")
            row += '| ' + i
            print(row)
        print("  '-------------------'")
        print("    1 2 3 4 5 6 7 8 9\n")

    def __str__(self):
        ordered_vals = []
        for r in ROW:
            for c in COL:
                ordered_vals.append(str(self.board[r + c]))
        return ''.join(ordered_vals)

    def write(self, fout=out_filename, mode='w+'):
        """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
        """
        outfile = open(fout, mode)
        outfile.write(self.__str__())
        outfile.write('\n')
        outfile.close()

    @staticmethod
    def get_neighbors(loc):
        x, y = loc
        if not isinstance(loc, tuple):
            x = ROW.index(x)
            y = int(y)
        return [c for c in product(*(range(n - 1, n + 2) for n in (x, y)))]

    @staticmethod
    def check_unique(x):
        vals = set()
        return not any(i in vals or vals.add(i) for i in x)

    @staticmethod
    def get_distance(a, b):
        """
        Calculate the distance between two numbers using the Manhattan formula
        """
        ax, ay = a
        bx, by = b
        return (bx - ax) ** 2 + (by - ay) ** 2

def string_to_board(s):
    """
    Helper function to convert a string to board dictionary.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c]) for r in range(9) for c in range(9)}

def time_string(start_time):
    elapsed = (time.time() - start_time) * 1000.0
    unit = "ms"
    if elapsed > 1000:
        unit = "sec"
        elapsed /= 1000
    elapsed = "%.2f" % elapsed
    return "%6s %3s" % (elapsed, unit)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) != 81:
            print(
                "\033[91m[ERROR] A valid sudoku is exactly 81 digits long. Empty spaces are represented by a zero.\033[0m")
            exit()
        csp = SudokuCSP(string_to_board(sys.argv[1]))
        csp.print_board()
        start = time.time()
        solution = csp.solve()
        print("Solved in", time_string(start))
        solution.print_board()
        solution.write(mode="w+")
    else:
        sudoku_list = None
        print("Solving all puzzles from %s" % src_filename)

        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        count = 0
        times = []
        easiest = None, None, float("inf")
        hardest = None, None, float("-inf")
        average = 0

        for line in sudoku_list.split("\n"):
            count += 1
            if len(line) < 9:
                continue

            csp = SudokuCSP(string_to_board(line))
            start = time.time()
            solution = csp.solve()

            # Keep track of how long it takes to solve each board
            end = (time.time() - start) * 1000.0
            time_str = time_string(start)
            if easiest[2] > end:
                easiest = count, time_str, end
            if hardest[2] < end:
                hardest = count, time_str, end
            times.append(end)
            average = (sum(times) / len(times))
            print("[SOLVED] board #%3.3d in %s, averaging %8s ms per board" % (count, time_str, "%3.3f" % average))
            solution.write(mode="a+")

        print("\nFinished all boards in %3.3f seconds." % (sum(times) / 1000.0))
        print("The solver averaged %3.3f milliseconds per puzzle." % average)
        print("The easiest board to solve was #%3.3d, which took %s" % (easiest[0], easiest[1]))
        print("The hardest board to solve was #%3.3d, which took %s" % (hardest[0], hardest[1]))
