"""This module contains the Board class for the Game of Life."""


class Board:
    """
    A class to represent the board for the Game of Life.

    Methods
    -------
    __init__(size)
        Creates the board with dimensions size x size.
    step()
        Performs one step of the Game of Life simulation.
    cleanBuffer()
        Called periodically to clean portions of the board invisible 
        to the user.
    get(row, col)
        Returns the cell state at a given row and column.
    flipCells(row, col)
        Inverts the state of a cell and updates the neighbor information 
        accordingly.
    updaateNeighbors(nMatrix, row, col, wasAlive)
        Modifies and returns a neighbor matrix given a coordinate and a 
        previous state.
    reset()
        Resets the board to its initial state.
    """

    # hyper-parameters
    BUFFER_SIZE = 5
    BUFFER_LIMIT = 5000

    def __init__(self, size):
        """
        Initializes the attributes of the class.

        Parameters:
            size (int) : The number of cells for a side of the board.
        """

        # user-perceived size
        self.size = size
        # actual size of the underlying matrix
        self.realSize = size + 2 * Board.BUFFER_SIZE

        self.cells = [[False for i in range(self.realSize)]
                      for j in range(self.realSize)]
        self.neighborCounts = [[0 for i in range(self.realSize)]
                               for j in range(self.realSize)]

        # counter for cleaning the buffer
        self.counter = 0

    def step(self):
        """
        Performs one step of the Game of Life simulation. Neighbor 
        matrix will be updated. Dead cells come to life if exactly 
        3 neighbors. Live cells die if not 2 or 3 neighbors.
        """

        # create copies of the current state
        tmp = [row[:] for row in self.cells]
        tmpNeighbor = [row[:] for row in self.neighborCounts]

        # iterate over the entire board, minus a "dead zone" of
        # 1 cell all around.
        for r in range(1, self.realSize - 1):
            for c in range(1, self.realSize - 1):
                neighbors = self.neighborCounts[r][c]
                if (self.cells[r][c] and not (2 <= neighbors <= 3)) or \
                        (not self.cells[r][c] and neighbors == 3):
                    # flip tmp, update neighbors
                    wasAlive = tmp[r][c]
                    tmp[r][c] = not self.cells[r][c]
                    self.updateNeighbors(tmpNeighbor, r, c, wasAlive)

        # replace cells and neighbor counts
        self.cells = tmp
        self.neighborCounts = tmpNeighbor

        # perform buffer cleaning if needed
        self.counter += 1
        if(self.counter >= Board.BUFFER_LIMIT):
            self.cleanBuffer()
            self.counter = 0

    def cleanBuffer(self):
        """
        Kills all cells off-screen. Will be called occasionally, frequency
        determined by BUFFER_LIMIT.
        """

        # The northern region of the buffer
        for r in range(0, Board.BUFFER_SIZE):
            for c in range(0, self.realSize):
                if(self.cells[r][c]):
                    self.flipCell(r - Board.BUFFER_SIZE, c - Board.BUFFER_SIZE)

        # The southern region of the buffer
        for r in range(self.realSize - Board.BUFFER_SIZE, self.realSize):
            for c in range(0, self.realSize):
                if(self.cells[r][c]):
                    self.flipCell(r - Board.BUFFER_SIZE, c - Board.BUFFER_SIZE)

        # The western region of the buffer
        for r in range(Board.BUFFER_SIZE, self.realSize - Board.BUFFER_SIZE):
            for c in range(0, BUFFER_SIZE):
                if(self.cells[r][c]):
                    self.flipCell(r - Board.BUFFER_SIZE, c - Board.BUFFER_SIZE)

        # The eastern region of the buffer
        for r in range(Board.BUFFER_SIZE, self.realSize - Board.BUFFER_SIZE):
            for c in range(self.realSize - Board.BUFFER_SIZE, self.realSize):
                if(self.cells[r][c]):
                    self.flipCell(r - Board.BUFFER_SIZE, c - Board.BUFFER_SIZE)

    def get(self, row, col):
        """
        Returns the cell state for a given row and column.

        Parameters:
            row (int) : The row coordinate.
            col (int) : The column coordinate.
        """

        return self.cells[row + Board.BUFFER_SIZE][col + Board.BUFFER_SIZE]

    def flipCell(self, row, col):
        """
        Inverts the cell state for a given row and column.
        Updates the neighborCounts matrix accordingly

        Parameters:
            row (int) : The row coordinate.
            col (int) : The column coordinate.
        """

        # translate row and col to realsize scale
        row += Board.BUFFER_SIZE
        col += Board.BUFFER_SIZE

        wasAlive = self.cells[row][col]

        self.cells[row][col] = not self.cells[row][col]

        self.neighborCounts = self.updateNeighbors(
            self.neighborCounts, row, col, wasAlive)

    # row and col are real indices
    def updateNeighbors(self, nMatrix, row, col, wasAlive):
        """
        Modifies and returns a neighbor matrix given a coordinate 
        and a previous state.

        Parameters:
            nMatrix (2d array) : A matrix of counts of alive neighbors.
            row (int): The underlying row coordinate (differs from user-
                perceived by BUFFER_SIZE).
            col (int): The underlying column coordinate (differs from 
                user-perceived by BUFFER_SIZE).
            wasAlive (boolean): Whether the inverted cell was alive before.
        """

        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                nMatrix[r][c] += -1 if wasAlive else 1
        return nMatrix

    def reset(self):
        """Resets the board to its original state."""
        self.__init__(self.size)
