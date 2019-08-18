import Board;
import numpy as np;


class Game:

  def __init__(self, gameOver, aiTurn, column_key):
    self.gameOver = gameOver;
    self.aiTurn = aiTurn;
    self.column_key = column_key;

  # checks if a move violates and rules
  def isMoveValid(self, board, to_move_column, to_move_row, place_moving_column, place_moving_row):
    if self.aiTurn:
      if (row < Board.NUM_ROWS) and (column < Board.NUM_COLUMNS):
        if Board.isSpaceOpen(board, place_moving_column, place_moving_row):
          return True;
    else:
      pass
    return False;

  def canJump(self, board, row, column):
    if self.aiTurn:
      pass

  def translate_input(self, input):
    split_in = str(input).split(',');
    column = split_in[0];
    column = self.column_key[column];
    row = int(split_in[1]) - 1;
    return column, row;

  def get_move_from(self):
    selection = input('Which piece would you like to move? (A-H),(1,8): ').upper();
    to_move_column, to_move_row = game.translate_input(selection);
    return to_move_column, to_move_row;

  def get_move_to(self):
    move = input('Where would you like to move it? (A-H),(1,8): ').upper();
    place_moving_column, place_moving_row = game.translate_input(move);
    return place_moving_column, place_moving_row;


if __name__ == '__main__':
  game = Game(False, False, {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7});
  # board = Board([], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]]);
  # board.initBoard();
  while not game.gameOver:
    if game.aiTurn == False:
      to_move_column, to_move_row = game.get_move_from();
      place_moving_column, place_moving_row = game.get_move_to();
      if game.isMoveValid(board, to_move_column, to_move_row, place_moving_column, place_moving_row):
        pass
    else:
      pass # AI makes move