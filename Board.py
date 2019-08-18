import numpy as np;

# static global vars
NUM_ROWS = 8;
NUM_COLUMNS = 8;
NUM_BLACK = 12;
NUM_RED = 12;
BLACK = 1;
RED = 2;
NOT_USED = 0;

class Board:

  # initializing class vars
  def __init__(self):
    self.board = None;
    self.blackCheckers = [[],[],[],[],[],[],[],[],[],[],[],[]];
    self.redCheckers = [[],[],[],[],[],[],[],[],[],[],[],[]];

  # delete objects
  def __del__(self):
    pass;

  # create a board that is ready to start playing
  def initBoard(self):
    self.create_board();
    self.mark_invalid_spaces();
    self.set_pieces_to_default();
    self.printBoard();

  # create an empty board
  def create_board(self):
    self.board = np.zeros((NUM_ROWS, NUM_COLUMNS));

  # mark invalid spaces
  def mark_invalid_spaces(self):
    x, y = 0, 0;
    for x in range(NUM_ROWS):
      for y in range(NUM_COLUMNS):
        if (x + y) % 2:
          self.board[x][y] = -1;

  # check if any given space on any board is open
  def isSpaceOpen(self, board, row, column):
    return self.board[row][column] == 0;

  # make a copy of the board passed in
  def copyBoard(self, old_board):
    new_board = old_board;
    return new_board;

  # sets all pieces back to their default position
  def set_pieces_to_default(self):
    b, r = 0, 0;
    for x in range(NUM_ROWS):
      for y in range(NUM_COLUMNS):
        if not (x == 3 or x == 4):
          if x < 3 and b < 12 and not (x + y) % 2:
            self.blackCheckers[b] = [x, y];
            self.board[x][y] = BLACK;
            b += 1;
          elif x > 4 and r < 12 and not (x + y) % 2:
            self.redCheckers[r] = [x, y];
            self.board[x][y] = RED;
            r += 1;


  # prints the board with AI pieces(black, 1) at bottom
  def printBoard(self):
    print(np.flip(self.board, 0))




ex = Board();
ex.initBoard();
ex.printBoard();