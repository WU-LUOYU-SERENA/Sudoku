# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def isGoal(self):
        for i in range(9):
            for j in range(9):
                if self.ans[i][j] == 0:
                    return False
        return True

    def allVarsAreAssigned(self, currAns):
        for i in range(9):
            for j in range(9):
                if currAns[i][j] == 0:
                    return False
        return True

    def isConsistent(self, currAns):
        # check duplicates in rows
        for i in range(9):
            rowSet = set()
            totalZeros = 0
            for j in range(9):
                if currAns[i][j] == 0:
                    totalZeros += 1
                else:
                    rowSet.add(currAns[i][j])
            if not len(rowSet) == 9 - totalZeros: # the row contains duplicates
                return False
        # check duplicates in columns
        for j in range(9):
            columnSet = set()
            totalZeros = 0
            for i in range(9):
                if currAns[i][j] == 0:
                    totalZeros += 1
                else:
                    columnSet.add(currAns[i][j])
            if not len(columnSet) == 9 - totalZeros: # the column contains duplicates
                return False
        # check duplicates in squares
        for x in range(3):
            for y in range(3):
                squareSet = set()
                totalZeros = 0
                for i in range(x * 3, x * 3 + 3):
                    for j in range (y * 3, y * 3 + 3):
                        if currAns[i][j] == 0:
                            totalZeros += 1
                        else:
                            squareSet.add(currAns[i][j])
                if not len(squareSet) == 9 - totalZeros: # the square contains duplicates
                    return False
        return True

    def improvedBackTrackingSearch(self, currAns):
        if self.allVarsAreAssigned(currAns):
            return currAns
        i, j = self.pickUnassignedVar(currAns)
        for value in range(1, 10):
            currAns[i][j] = value
            if self.isConsistent(currAns):
                result = self.improvedBackTrackingSearch(currAns)
                if not result == False:
                    return result
                currAns[i][j] = 0
        return False


    def solve(self):
        return self.improvedBackTrackingSearch(self.ans)
        #return self.puzzle

    def computeUnAssignedVariables(self, currAns):
        unassignedVars = Queue()
        for i in range(9):
            for j in range(9):
                if currAns[i][j] == 0:
                    unassignedVars.push((i, j))
        return unassignedVars

    # pick first value in the unassigned variables list
    def pickUnassignedVar(self, currAns):
        return self.computeUnAssignedVariables(currAns).pop()

    def infer(self):
        # inference: list of tuples in the form of
        #   ((x-coordinate, y-coordinate), [values the variable cannot take])
        inference = []
        varQueue = Queue()
        while not varQueue.isEmpty():
            y = varQueue.pop()

        return []

    def constraint(self, assignedVar, comparedVar):
        return not assignedVar[1] == comparedVar[1]

'''
    def solve(self):
        if self.isGoal():
            return self.ans
        coordinate, currVal, domain = self.pickUnassignedVar()
        for value in domain:
            self.ans[coordinate[0]][coordinate[1]] = value
            inference = self.infer
            for inferredCoord, inferredVal in inference:
                self.ans[inferredCoord[0]][inferredCoord[1]] = inferredVal
            if not inference == 0:
'''


    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0, item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    f = open('test_output/input_5.txt', 'r')

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open('test_output/output_5.txt', 'r+') as f:
        f.truncate(0)
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")

'''
if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
'''