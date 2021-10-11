# CS3243 Introduction to Artificial Intelligence
# Project 2
import heapq
import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        # self.unassignedVars is a Queue of tuples of the form ((x,y), [possible values])
        unassigned = self.computeUnAssignedVariables(self.ans)
        self.unassignedVars = self.preprocessVar(unassigned)

    def computeUnAssignedVariables(self, currAns):
        unassigned = PriorityQueue()
        for i in range(9):
            for j in range(9):
                if currAns[i][j] == 0:
                    unassigned.push(((i, j), range(1, 10)))
        return unassigned

    def preprocessVar(self, unassigned):
        unassignedVars = copy.deepcopy(unassigned)
        len = unassigned.count
        assert id(unassignedVars) != id(unassigned)
        for index, (priority, c, ((x, y), domain)) in enumerate(unassignedVars.heap):
            # unassigned[index] = priority, count, item
            positions = self.findConstraintPositions((x, y))
            for (i, j) in positions:
                val = self.puzzle[i][j]
                if val != 0:
                    if val in domain:
                        domain.remove(val)
                        len = unassignedVars.update(((x, y), domain))
                        if len == 1:
                            self.ans[x][y] = domain[0]
                            assert self.isConsistent(self.ans)
                            unassignedVars.remove(((x, y), domain))
                            break
        return unassignedVars

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

    def solve(self):
        return self.backtrackingWithInfer(self.ans, self.unassignedVars)

    def backtrackingWithInfer(self, currAns, currUnassignedVars):
        if self.allVarsAreAssigned(currAns):
            return currAns
        (x, y), domain = currUnassignedVars.pop()
        for value in domain:
            currAns[x][y] = value
            if self.isConsistent(currAns):
                inference = self.infer((x, y), currAns, currUnassignedVars)
                if inference: # inference = nextAns, nextUnassignedVars
                    nextAns = inference[0]
                    nextUnassignedVars = inference[1]
                    result = self.backtrackingWithInfer(nextAns, nextUnassignedVars)
                    if result:
                        return result
            currAns[x][y] = 0
        return False

    def infer(self, (i, j), currAns, currUnassignedVars):
        # inference: list of tuples in the form of
        #   ((x-coordinate, y-coordinate), [values the variable cannot take])
        nextAns = copy.deepcopy(currAns)
        nextUnassignedVars = copy.deepcopy(currUnassignedVars)
        varQueue = Queue()
        # varQueue.push((i, j))
        # do part of do-while loop
        # (x, y) = varQueue.pop()
        constrainedVars = self.findConstraintPositions((i, j))
        val = nextAns[i][j]
        for index, (priority, c, ((xx, yy), domain)) in enumerate(nextUnassignedVars.heap):
            assert priority == len(domain)
            if not (xx, yy) in constrainedVars:
                continue
            if val in domain:
                domain.remove(val)
                nextUnassignedVars.update(((xx, yy), domain))
                if len(domain) == 0:
                    return False
                if len(domain) == 1:
                    varQueue.push(((xx, yy), domain))
        # while part of  do-while loop
        while not varQueue.isEmpty():
            (x, y), domainOfLenOne = varQueue.pop()
            assert len(domainOfLenOne) == 1
            nextAns[x][y] = domainOfLenOne[0]
            if self.isConsistent(nextAns):
                nextUnassignedVars.remove(((x, y), domainOfLenOne))
                constrainedPos = self.findConstraintPositions((x, y))
                for index, (priority, c, ((xx, yy), domainOfXxYy)) in enumerate(nextUnassignedVars.heap):
                    if not (xx, yy) in constrainedPos:
                        continue
                    if nextAns[x][y] in domainOfXxYy:
                        domainOfXxYy.remove(nextAns[x][y])
                        nextUnassignedVars.update(((xx, yy), domainOfXxYy))
                        if len(domainOfXxYy) == 0:
                            return False
                        if len(domainOfXxYy) == 1:
                            varQueue.push(((xx, yy), domainOfXxYy))
            else:
                return False
        return nextAns, nextUnassignedVars

    def findConstraintPositions(self, (x, y)):
        positions = set()
        for j in range(9):
            positions.add((x, j)) # variables in the same row
        for i in range(9):
            positions.add((i, y)) # variables in the same column
        xx = x % 3
        yy = y % 3
        xRange = self.computeRange(x, xx)
        yRange = self.computeRange(y, yy)
        for i in xRange:
            for j in yRange:
                positions.add((i, j)) # variables in the same square
        assert len(positions) == 21
        positions.remove((x, y))
        assert len(positions) == 20
        return positions

    def computeRange(self, x, xx):
        if xx == 0:
            return range(x, x+3)
        if xx == 1:
            return range(x-1, x+2)
        if xx == 2:
            return range (x-2, x+1)

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item): # item = (x,y), domain
        priority = len(item[1]) # priority is the size of domain
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def remove(self, item):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item: # find the item in the heap
                del self.heap[index]
                self.count -= 1
                heapq.heapify(self.heap)
                return
        return False

    def index(self, item):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                return index
        return False

    def update(self, (coordinates, domain)): # item = (x, y), domain
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, return false.
        # If item not in priority queue, return false.
        priority = len(domain) # priority is the size of domain
        for index, (p, c, i) in enumerate(self.heap):
            if i[0] == coordinates:
                if p <= priority:
                    return False
                del self.heap[index]
                self.heap.append((priority, c, (coordinates, domain)))
                heapq.heapify(self.heap)
                return priority
                break
        return False


class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))

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
    '''
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")
    '''
    try:
        f = open('CS3243_P2_Sudoku_XX/input_1.txt', 'r')
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

    with open('CS3243_P2_Sudoku_XX/output_1.txt', 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
