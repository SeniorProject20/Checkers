import Checker, copy;

class Board:

  NUM_ROWS = 8;
  NUM_COLUMNS = 8;
  NUM_BLACK = 12;
  NUM_RED = 12;
  NOT_USED = 0;

  def __init__(self):
    self.board = [[self.NUM_ROWS],[self.NUM_COLUMNS]];
    self.InitializeBoard();

  # creates a board set to begin play
  def InitializeBoard(self):
    self.mark_invalid_spaces();
    self.set_pieces_to_default();

  # mark invalid spaces
  def mark_invalid_spaces(self):
    row, column = 0, 0;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if (row + column) % 2:
          self.board[row][column] = None;
  
  # returns if the position in question is open
  def IsSpaceOpen(self, row, column):
    if self.board[[row],[column]] == self.NOT_USED:
      return True;
    else:
      return False;

  # makes a deepcopy of the board passed in
  def CopyBoard(self):
    new_board = copy.deepcopy(self.board);
    return new_board;

  # sets all checkers to their default position
  def set_pieces_to_default(self):
    b, r = 0, 0;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if (row == 3 or row == 4):
          name = self.NOT_USED;
        else:
          if x < 3 and b < self.NUM_BLACK and not (row + column) % 2:
            name = 'b' + str(b);
            name = Checker('black');
            b += 1;
          elif x > 4 and r < self.NUM_RED and not (row + column) % 2:
            name = 'r' + str(r);
            name = Checker('red');
            r += 1;
        board[[row], [column]] = name;


x = 6;






