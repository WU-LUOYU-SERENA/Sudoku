# CS3243 Introduction to Artificial Intelligence
# Project 2

import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt
import sys


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.ans = puzzle  # self.puzzle is a list of lists
        # self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        # self.unassignedVars is a Queue of tuples of the form ((x,y), [possible values])
        unassigned = self.computeUnAssignedVariables(self.ans)
        self.unassignedVars = self.preprocessVar(unassigned)

    def computeUnAssignedVariables(self, currAns):
        unassignedVars = [[[] for y in range(9)] for x in range(9)]  # 9 * 9 array of lists
        numOfUnassignedVars = 0
        for i in range(9):
            for j in range(9):
                if currAns[i][j] == 0:
                    unassignedVars[i][j] = range(1, 10)
                    numOfUnassignedVars += 1
                else:
                    unassignedVars[i][j] = [10]
        unassignedVars.append([[numOfUnassignedVars]])
        return unassignedVars

    def preprocessVar(self, unassigned):
        # unassignedVars = pickle.loads(pickle.dumps(unassigned))
        # unassignedVars = copy.deepcopy(unassigned)
        unassignedVars = [list([list(innerlist) for innerlist in outerlist]) for outerlist in unassigned]
        assert id(unassignedVars) != id(unassigned)
        length = len(unassigned)
        # iterator = 0
        varQueue = Queue()
        for x in range(9):
            for y in range(9):
                # domain = unassigned[x][y]  # domain is a list
                # index = unassignedVars.getIndex(((x, y), domain))
                if self.ans[x][y] != 0:
                    assert unassignedVars[x][y] == [10]
                    continue
                assert unassignedVars[x][y] != [10]
                positions = self.findConstraintPositions((x, y))
                for (i, j) in positions:
                    val = self.ans[i][j]
                    if val == 0:
                        continue
                    if val in unassignedVars[x][y]:
                        unassignedVars[x][y].remove(val)
                        if len(unassignedVars[x][y]) == 1:
                            varQueue.push((x, y))
                            '''
                            self.ans[x][y] = unassignedVars[x][y][0]
                            unassignedVars[x][y] = [10]
                            unassignedVars[9][0][0] -= 1
                            for (xx, yy) in positions:
                                if val == 0:  # unassigned
                                    if self.ans[x][y] in unassignedVars[xx][yy]:
                                        unassignedVars[xx][yy].remove(self.ans[x][y])
                                        if len(unassignedVars[xx][yy] == 1):
                                            varQueue.push((xx, yy))
                            '''
                            # unassignedVars.removeIndex(index)
                            # break
        while not varQueue.isEmpty():
            x, y = varQueue.pop()
            assert len(unassignedVars[x][y]) == 1
            self.ans[x][y] = unassignedVars[x][y][0]
            unassignedVars[x][y] = [10]
            unassignedVars[9][0][0] -= 1
            constrainedPos = self.findConstraintPositions((x, y))
            for (xx, yy) in constrainedPos:
                if self.ans[xx][yy] == 0:  # unassigned
                    if self.ans[x][y] in unassignedVars[xx][yy]:
                        unassignedVars[xx][yy].remove(self.ans[x][y])
                        if len(unassignedVars[xx][yy]) == 1:
                            varQueue.push((xx, yy))
        assert length == len(unassigned)
        return unassignedVars

    '''
    def allVarsAreAssigned(self, currAns):
        for i in range(9):
            for j in range(9):
                if currAns[i][j] == 0:
                    return False
        return True
    '''

    def allVarsAreAssigned(self, unassignedVars):
        return unassignedVars[9][0][0] == 0

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
            if not len(rowSet) == 9 - totalZeros:  # the row contains duplicates
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
            if not len(columnSet) == 9 - totalZeros:  # the column contains duplicates
                return False
        # check duplicates in squares
        for x in range(3):
            for y in range(3):
                squareSet = set()
                totalZeros = 0
                for i in range(x * 3, x * 3 + 3):
                    for j in range(y * 3, y * 3 + 3):
                        if currAns[i][j] == 0:
                            totalZeros += 1
                        else:
                            squareSet.add(currAns[i][j])
                if not len(squareSet) == 9 - totalZeros:  # the square contains duplicates
                    return False
        return True

    def mostConstrainedVarHeuristics(self, currUnassignedVars):
        mostX = 10
        mostY = 10
        minLen = 10
        for i in range(9):
            for j in range(9):
                if currUnassignedVars[i][j] == [10]:
                    continue
                if len(currUnassignedVars[i][j]) < minLen:
                    minLen = len(currUnassignedVars[i][j])
                    mostX = i
                    mostY = j
        assert minLen < 10
        assert mostX < 10
        assert mostY < 10
        return mostX, mostY

    def solve(self):
        return self.backtrackingWithInfer(self.ans, self.unassignedVars)

    def backtrackingWithInfer(self, currAns, currUnassignedVars):
        assert self.isConsistent(currAns)
        if self.allVarsAreAssigned(currUnassignedVars):
            return currAns
        x, y = self.mostConstrainedVarHeuristics(currUnassignedVars)
        for value in currUnassignedVars[x][y]:
            currAns[x][y] = value
            # currDomain = currUnassignedVars[x][y]
            # currUnassignedVars[x][y] = [10]
            # if self.isConsistent(currAns):
            inference = self.infer((x, y), currAns, currUnassignedVars)
            if inference:  # inference = nextAns, nextUnassignedVars
                nextAns = inference[0]
                nextUnassignedVars = inference[1]
                result = self.backtrackingWithInfer(nextAns, nextUnassignedVars)
                if result:
                    return result
            currAns[x][y] = 0
        return False

    def findConstraintPositions(self, (x, y)):
        positions = set()
        for j in range(9):
            positions.add((x, j))  # variables in the same row
        for i in range(9):
            positions.add((i, y))  # variables in the same column
        xx = x % 3
        yy = y % 3
        xRange = self.computeRange(x, xx)
        yRange = self.computeRange(y, yy)
        for i in xRange:
            for j in yRange:
                positions.add((i, j))  # variables in the same square
        assert len(positions) == 21
        positions.remove((x, y))
        assert len(positions) == 20
        return positions

    def computeRange(self, x, xx):
        if xx == 0:
            return range(x, x + 3)
        if xx == 1:
            return range(x - 1, x + 2)
        if xx == 2:
            return range(x - 2, x + 1)

    def infer(self, (i, j), currAns, currUnassignedVars):
        # inference: list of tuples in the form of
        #   ((x-coordinate, y-coordinate), [values the variable cannot take])
        # nextAns = pickle.loads(pickle.dumps(currAns))
        # nextAns = copy.deepcopy(currAns)
        nextAns = [list(lst) for lst in currAns]
        # nextUnassignedVars = pickle.loads(pickle.dumps(currUnassignedVars))
        # nextUnassignedVars = copy.deepcopy(currUnassignedVars)
        nextUnassignedVars = [list([list(innerlist) for innerlist in outerlist]) for outerlist in currUnassignedVars]
        varQueue = Queue()
        # varQueue.push((i, j))
        # do part of do-while loop
        # (x, y) = varQueue.pop()
        val = nextAns[i][j]
        nextUnassignedVars[i][j] = [10]
        nextUnassignedVars[9][0][0] -= 1
        constrainedVars = self.findConstraintPositions((i, j))
        # for (xx, yy), domain in nextUnassignedVars:
        # find unassigned variables that are affected
        for (xx, yy) in constrainedVars:
            if nextUnassignedVars[xx][yy] == [10]:  # already assigned
                continue
            if val in nextUnassignedVars[xx][yy]:
                nextUnassignedVars[xx][yy].remove(val)
                if len(nextUnassignedVars[xx][yy]) == 0:
                    return False
                if len(nextUnassignedVars[xx][yy]) == 1:
                    varQueue.push((xx, yy))
        # while part of  do-while loop
        while not varQueue.isEmpty():
            (x, y) = varQueue.pop()
            assert len(nextUnassignedVars[x][y]) == 1
            nextAns[x][y] = nextUnassignedVars[x][y][0]
            if self.isConsistent(nextAns):
                # nextUnassignedVars.removeItem(((x, y), domainOfLenOne))
                nextUnassignedVars[9][0][0] -= 1
                nextUnassignedVars[x][y] = [10]
                constrainedPos = self.findConstraintPositions((x, y))
                for (xx, yy) in constrainedPos:
                    if nextAns[x][y] in nextUnassignedVars[xx][yy]:
                        nextUnassignedVars[xx][yy].remove(nextAns[x][y])
                        if len(nextUnassignedVars[xx][yy]) == 0:
                            return False
                        if len(nextUnassignedVars[xx][yy]) == 1:
                            varQueue.push((xx, yy))
            else:
                return False
        return nextAns, nextUnassignedVars

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."

    def __init__(self):
        self.list = []

    def __getitem__(self, index):
        return self.list[index]

    def getIndex(self, item):
        i = 0
        while (i < len(self.list)):
            if item == self.list[i]:
                return i
            i += 1
        return False

    def push(self, item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0, item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def popMostConstrainedVar(self):
        minLen = 10
        minIndex = 0
        i = 0
        while (i < len(self.list)):
            if len(self.list[i][1]) < minLen:
                minLen = len(self.list[i][1])
                minIndex = i
            i += 1
        if minLen == 10:
            return False
        return self.removeIndex(minIndex)

    # Override
    def removeIndex(self, index):
        return self.list.pop(index)

    def removeItem(self, item):
        i = 0
        while (i < len(self.list)):
            if item == self.list[i]:
                self.list.remove(item)
            i += 1
        return False

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

    def __len__(self):
        "Returns the length of the list"
        return len(self.list)

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
if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here

    try:
        f = open('CS3243_P2_Sudoku_XX/input_4.txt', 'r')
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

    with open('CS3243_P2_Sudoku_XX/output_4.txt', 'a') as f:
        f.truncate(0)
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")

'''