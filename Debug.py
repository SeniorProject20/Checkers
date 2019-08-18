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

board = np.zeros((NUM_COLUMNS, NUM_ROWS));
board[1][1] = None;
print(board)

# np.ones(# of col)
# np.zeros()
# np.linspace(from, to, numElems)
# np.array([put python list])
# np.random.seed(0)
# np.random.randint(maxNum, size=#of elems)