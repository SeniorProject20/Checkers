import numpy as np;


class Board:
  # static class vars
  NUM_ROWS = 8;
  NUM_COLUMNS = 8;
  NUM_BLACK = 12;
  NUM_RED = 12;
  BLACK = 1;
  RED = 2;
  NOT_USED = 0;

  # initializing class vars
  def __init__(self, board, blackCheckers, redCheckers):
    self.board = board;
    self.blackCheckers = blackCheckers;
    self.redCheckers = redCheckers;

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
    self.board = np.zeros((self.NUM_COLUMNS, self.NUM_ROWS));

  # mark invalid spaces
  def mark_invalid_spaces(self):
    x, y = 0, 0;
    for x in range(self.NUM_COLUMNS):
      for y in range(self.NUM_ROWS):
        if (x + y) % 2:
          self.board[x][y] = None;

  # check if any given space is open
  def isSpaceOpen(self, board, column, row):
    return self.board[column][row] == 0;

  # returns if a space is playable
  def isSpaceValid(self, column, row):
    return not (self.board[column][row] == None);

  # Checks if a space has a red checker
  def isRedChecker(self, column, row):
    return self.board[column][row] == 2;

  # Checks if a space has a red checker
  def isBlackChecker(self, column, row):
    return self.board[column][row] == 1;

  # make a copy of the board passed in
  def copyBoard(self, old_board):
    new_board = old_board;
    return new_board;

  # sets all pieces back to their default position
  def set_pieces_to_default(self):
    b, r = 0, 0;
    for x in range(self.NUM_COLUMNS):
      for y in range(self.NUM_ROWS):
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
  def printBoard(self, board):
    print(np.flip(board, 0))




ex = Board([], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]]);
ex.initBoard();
ex.printBoard();