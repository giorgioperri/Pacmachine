import numpy as np
from constants import *

class State:
    def __init__(self):
        # Generate a tictactoe board full of 0s.
        self.board = np.zeros((NROWS, NCOLS, 4))

        # Variable for whether game is finished and needs restarting or not.
        self.isEnd = False

        # Initialise p1 to have the first move. 
        # P1 will have symbol 1, P2 will have -1.

    # Get unique hash of current board state.
    # A hash is simply the current board, represented as a single row.
    def getHash(self):
        self.boardHash = str(self.board.reshape(self.sizeX * self.sizeY))
        return self.boardHash
    

    """

    
  
    # Function for checking whether there is a winner in the current state of the board.
    # This will be checked at the beginning of every turn.
    # To check for a winner, check if the numbers sum up to 3 or -3 in any of the directions.
    def winner(self):
        # row
        for i in range(BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        # col
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # tie
        # No more available positions --> game ends.
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # Not end
        self.isEnd = False
        return None

    # Compute the available positions by checking which positions have 0s.
    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    # Given the current board, and the position where the player
    # wants to put his symbol, updates the board to the new state.
    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1
    """