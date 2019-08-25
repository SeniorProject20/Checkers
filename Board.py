import copy;
from Checker import Checker;

class Board:

  NUM_ROWS = 8;
  NUM_COLUMNS = 8;
  NUM_BLACK = 12;
  NUM_RED = 12;
  FREE_SPACE = 0;
  INVALID_SPACE = None;

  def __init__(self):
    self.board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]];
    self.CHECKERS = {};

  # creates a board set to begin play
  def InitializeBoard(self):
    self.mark_invalid_spaces();
    self.set_pieces_to_default();
    self.PrintBoard();

  # mark invalid spaces
  def mark_invalid_spaces(self):
    row, column = 0, 0;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if (row + column) % 2:
          self.board[row][column] = self.INVALID_SPACE;
  
  # returns if the position in question is open
  def IsSpaceOpen(self, row, column):
    if self.board[row][column] == self.FREE_SPACE:
      return True;
    else:
      return False;

  # move a checker
  def Move(self, checker_name, row, column):
    index = self.board.index(checker_name);
    checker_obj = self.CHECKERS[checker_name];
    if self.is_move_valid(checker_obj, row, column):
      self.board[row][column] = checker_name;
      self.board[moving_from_row][moving_from_column] = self.FREE_SPACE;
      return True;
    else:
      return False;

  # check if a move is valid
  def is_move_valid(self, checker_obj, row, column):
    if self.board[row][column] != self.INVALID_SPACE:
      name = self.board[moving_from_row][moving_from_column];
      if self.board[row][column] == self.FREE_SPACE :
        if checker_obj.isKing:
          if (moving_from_row == (row + 1)) or (moving_from_row == (row - 1)):
            pass
        elif checker_obj.color == 'red':
          if moving_from_row == row + 1:
            pass
        else:
          if moving_from_row == row - 1:
            pass
    else:
      return False;

  # makes a deepcopy of the board passed in
  def CopyBoard(self):
    new_board = copy.deepcopy(self);
    return new_board;

  # sets all checkers to their default position
  def set_pieces_to_default(self):
    b, r = 0, 0;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if (row == 3 or row == 4) and not (row + column) % 2:
          name = self.FREE_SPACE;
        else:
          if row < 3 and b < self.NUM_BLACK and not (row + column) % 2:
            name = 'B' + str(b);
            ref = Checker('black', name);
            self.CHECKERS[name] = ref;
            b += 1;
          elif row > 4 and r < self.NUM_RED and not (row + column) % 2:
            name = 'R' + str(r);
            ref = Checker('red', name);
            self.CHECKERS[name] = ref;
            r += 1;
        if name != None:
          self.board[row][column] = name;
        name = None;

  # print a board in the way we expect to see it
  def PrintBoard(self):
    copy = self.board[::-1]
    for each in copy:
      print(each)

if __name__ == '__main__': # for debugging this file
  x = Board();
  x.Move('B8', 3,1)
  x.PrintBoard();
  print(x.IsSpaceOpen(3,1))
  print(x.CHECKERS)
