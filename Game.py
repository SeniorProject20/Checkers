import Board;
import numpy as np;

# static global vars
NUM_ROWS = 8;
NUM_COLUMNS = 8;
NUM_BLACK = 12;
NUM_RED = 12;
BLACK = 1;
RED = 2;
NOT_USED = 0;

class Game:

  def __init__(self):
    self.gameOver = False;
    self.aiTurn = False;
    self.column_key = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7};

  # checks if a move violates and rules
  def isMoveValid(self, board, row, column):
    if (row < NUM_ROWS) and (column < NUM_COLUMNS):
      if Board.isSpaceOpen(board, row, column):
        return True;
    return False;

  def canJump(self, board, row, column):
    pass

  def translate_input(self, input):
    split_in = str(input).split(',');
    column = split_in[0];
    column = self.column_key[column];
    row = int(split_in[1]);
    return column, row;


if __name__ == '__main__':
  game = Game();
  board = Board;
  # Board.initBoard();
  while not game.gameOver:
    if game.aiTurn == False:
      selection = input('Which piece would you like to move? (A-H),(1,8): ').upper();
      to_move_column, to_move_row = game.translate_input(selection);
      move = input('Where would you like to move it? (A-H),(1,8): ').upper();
      place_moving_column, place_moving_row = game.translate_input(move);
      x = 1;