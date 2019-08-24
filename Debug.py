## Scratch paper file to try functions
import numpy as np

# static global vars
NUM_ROWS = 8;
NUM_COLUMNS = 8;
NUM_BLACK = 12;
NUM_RED = 12;
BLACK = 1;
RED = 2;
NOT_USED = 0;

board = []
for i in range(64):
  board.append([])
print(len(board))
board[0].append(3)
board[0].append(4)
board[0].append(True)
print(board)
for i in range(len(board)):
  if i % 2:
    board[i].append(None);
print(board)


# # Checks if a space has a red checker
# def isRedChecker(self, column, row):
#   return self.board[column][row] == 2;
#
#
# # Checks if a space has a red checker
# def isBlackChecker(self, column, row):
#   return self.board[column][row] == 1;
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