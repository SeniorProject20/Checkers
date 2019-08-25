from Board import Board;
from Checker import Checker;
import numpy as np;


class Game:

  AI_TURN = False; # Player always moves first
  GAME_OVER = False; # Game isn't over till the fat lady sings
  COLUMN_KEY = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7};

  def translate_input(self, input):
    split_in = str(input).split(',');
    column = split_in[0];
    column = self.column_key[column];
    row = int(split_in[1]) - 1;
    return column, row;

  def get_checker_to_move(self):
    piece = input('Which piece would you like to move? (R0-R11)').upper();
    return piece;

  def get_move_to(self):
    move = input('Where would you like to move it? (1,8),(A-H): ').upper();
    row, column  = game.translate_input(move);
    return place_moving_column, place_moving_row;

if __name__ == '__main__':
  game = Game();
  board = Board();
  while not game.GAME_OVER:
    if not game.AI_TURN:
      piece = game.get_checker_to_move();
      row, column = game.get_move_to();
      if board.Move(piece, row, column):
        # update board
        pass
      else:
        # throw error, ask for new move
        pass
    else:
      pass # AI makes move