## Scratch paper file to try functions
import numpy as np
import pygame

# # static global vars
# NUM_ROWS = 8;
# NUM_COLUMNS = 8;
# NUM_BLACK = 12;
# NUM_RED = 12;
# BLACK = 1;
# RED = 2;
# NOT_USED = 0;
#
# board = []
# for i in range(64):
#   board.append([])
# print(len(board))
# board[0].append(3)
# board[0].append(4)
# board[0].append(True)
# print(board)
# for i in range(len(board)):
#   if i % 2:
#     board[i].append(None);
# print(board)


# # Checks if a space has a red checker
# def isRedChecker(self, column, row):
#   return self.board[column][row] == 2;
#
#
# # Checks if a space has a red checker
# def isBlackChecker(self, column, row):
#   return self.board[column][row] == 1;

#BOARD
  # static class vars
#   NUM_ROWS = 8;
#   NUM_COLUMNS = 8;
#   NUM_BLACK = 12;
#   NUM_RED = 12;
#   BLACK = 1;
#   RED = 2;
#   NOT_USED = 0;
#
#   # initializing class vars
#   def __init__(self, board):
#     self.board = board;
#
#   # delete objects
#   def __del__(self):
#     pass;
#
#   # create a board that is ready to start playing
#   def initBoard(self):
#     self.create_board();
#     self.mark_invalid_spaces();
#     self.set_pieces_to_default();
#     self.printBoard();
#
#   # create an empty board
#   def create_board(self):
#     self.board = np.zeros((self.NUM_COLUMNS, self.NUM_ROWS));
#
#   # check if any given space is open
#   def isSpaceOpen(self, board, column, row):
#     return self.board[column][row] == 0;
#
#   # returns if a space is playable
#   def isSpaceValid(self, column, row):
#     return not (self.board[column][row] == None);
#
#   # make a copy of the board passed in
#   def copyBoard(self, old_board):
#     new_board = old_board;
#     return new_board;
#
#   # sets all pieces back to their default position
#   def set_pieces_to_default(self):
#     b, r = 0, 0;
#     for x in range(self.NUM_COLUMNS):
#       for y in range(self.NUM_ROWS):
#         if not (x == 3 or x == 4):
#           if x < 3 and b < 12 and not (x + y) % 2:
#             self.blackCheckers[b] = [x, y];
#             self.board[x][y] = BLACK;
#             b += 1;
#           elif x > 4 and r < 12 and not (x + y) % 2:
#             self.redCheckers[r] = [x, y];
#             self.board[x][y] = RED;
#             r += 1;
#
#   # prints the board with AI pieces(black, 1) at bottom
#   def printBoard(self, board):
#     print(np.flip(board, 0))
#
#
#
#
# ex = Board([], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]]);
# ex.initBoard();
# ex.printBoard();
#
# # mark invalid spaces
# def mark_invalid_spaces(self):
#   x, y = 0, 0;
#   for x in range(self.NUM_COLUMNS):
#     for y in range(self.NUM_ROWS):
#       if (x + y) % 2:
#         self.board[x][y] = None;

# np.ones(# of col)
# np.zeros()
# np.linspace(from, to, numElems)
# np.array([put python list])
# np.random.seed(0)
# np.random.randint(maxNum, size=#of elems)

# import itertools
# import pygame as pg
#
#
# pg.init()
#
# BLACK = pg.Color('black')
# WHITE = pg.Color('white')
#
# screen = pg.display.set_mode((800, 600))
# clock = pg.time.Clock()
#
# colors = itertools.cycle((WHITE, BLACK))
# tile_size = 40
# width, height = 8*tile_size, 8*tile_size
# background = pg.Surface((width, height))
#
# for y in range(0, height, tile_size):
#     for x in range(0, width, tile_size):
#         rect = (x, y, tile_size, tile_size)
#         pg.draw.rect(background, next(colors), rect)
#     next(colors)
#
# game_exit = False
# while not game_exit:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             game_exit = True
#
#     screen.fill((60, 70, 90))
#     screen.blit(background, (100, 100))
#
#     pg.display.flip()
#     clock.tick(30)
#
# pg.quit()