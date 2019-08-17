import numpy as num;

class Board:

  def create_board(self):
    self.board = num.zeros((8, 8));
    for y in range(1, 8):
      for x in range(1, 8):
        if (x * y) % 2 == 1:
          self.board[x][y] = 'X';
    print(self.board);


  def InitBoard(self):
    create_board();
    # self.locations =

board = Board();
Board.create_board(board);