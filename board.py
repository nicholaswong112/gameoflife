BUFFER_SIZE = 5
BUFFER_LIMIT = 50000
COUNTER = 0


class Board:
    def __init__(self, size):
        self.size = size
        self.realSize = size + 2 * BUFFER_SIZE
        self.cells = [[False for i in range(self.realSize)] for j in range(
            self.realSize)]  # all False (dead) initially
        self.neighborCounts = [[0 for i in range(self.realSize)] for j in range(
            self.realSize)]  # all 0 initially
    # runs a step of the simulation, updating the cells matrix
    # governed by these rules
    # dead -> alive if exactly 3 neighbors
    # alive -> dead if not exactly 2 or 3 neighbors

    def step(self):
        global COUNTER
        tmp = [row[:] for row in self.cells]
        tmpNeighbor = [row[:] for row in self.neighborCounts]
        for r in range(1, self.realSize - 1):
            for c in range(1, self.realSize - 1):
                neighbors = self.neighborCounts[r][c]
                if (self.cells[r][c] and not (2 <= neighbors <= 3)) or \
                        (not self.cells[r][c] and neighbors == 3):
                    # flip tmp, update neighbors
                    wasAlive = tmp[r][c]
                    tmp[r][c] = not self.cells[r][c]
                    self.updateNeighbors(tmpNeighbor, r, c, wasAlive)
                COUNTER += 1
        self.cells = tmp
        self.neighborCounts = tmpNeighbor
        if(COUNTER >= BUFFER_LIMIT):
            self.cleanBuffer()
            COUNTER = 0

    def cleanBuffer(self):
        # The northern region of the buffer
        for r in range(0, BUFFER_SIZE):
            for c in range(0, self.realSize):
                if(self.cells[r][c]):
                    self.flipCell(r - BUFFER_SIZE, c - BUFFER_SIZE)
        # The southern region of the buffer
        for r in range(self.realSize - BUFFER_SIZE, self.realSize):
            for c in range(0, self.realSize):
                if(self.cells[r][c]):
                    self.flipCell(r - BUFFER_SIZE, c - BUFFER_SIZE)
        # The western region of the buffer
        for r in range(BUFFER_SIZE, self.realSize - BUFFER_SIZE):
            for c in range(0, BUFFER_SIZE):
                if(self.cells[r][c]):
                    self.flipCell(r - BUFFER_SIZE, c - BUFFER_SIZE)
        # The eastern region of the buffer
        for r in range(BUFFER_SIZE, self.realSize - BUFFER_SIZE):
            for c in range(self.realSize - BUFFER_SIZE, self.realSize):
                if(self.cells[r][c]):
                    self.flipCell(r - BUFFER_SIZE, c - BUFFER_SIZE)

    def get(self, row, col):
        return self.cells[row + BUFFER_SIZE][col + BUFFER_SIZE]
    # row and col are user-perceived indices

    def flipCell(self, row, col):
        row += BUFFER_SIZE
        col += BUFFER_SIZE
        # now row and col are the real thing
        wasAlive = self.cells[row][col]
        self.cells[row][col] = not self.cells[row][col]
        self.neighborCounts = self.updateNeighbors(
            self.neighborCounts, row, col, wasAlive)

    # row and col are real indices
    def updateNeighbors(self, nMatrix, row, col, wasAlive):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                nMatrix[r][c] += -1 if wasAlive else 1
        return nMatrix

    def reset(self):
        self.__init__(self.size)
