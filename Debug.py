## Scratch paper file to try functions
# from Checker import Checker;
# from Board import Board;
# from Game import Game;
# from LookAhead import CheckJumps;

# import itertools
# import pygame as pg
#
#
# pg.init()
#
# BLACK = pg.Color('black')
# WHITE = pg.Color('white')
#
# screen = pg.display.set_mode((700, 700))
# clock = pg.time.Clock()
#
# colors = itertools.cycle((WHITE, BLACK))
# tile_size = 60
# width, height = 8 * tile_size, 8 * tile_size
# background = pg.Surface((width, height))
#
# for y in range(0, height, tile_size):
#     for x in range(0, width, tile_size):
#       rect = (x, y, tile_size, tile_size)
#       pg.draw.rect(background, next(colors), rect)
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

# x.Move('R0', 4, 2);
# x.Move('R0', 3, 3)
# x.Move('B9', 4, 4)
# x.Move('R1', 3, 5)

# if type(d_r) == Checker.Checker:
#   if d_r.color != checker_obj.color and Board.board[row - 2][column + 2] == Board.FREE_SPACE:
#     moves.append(row - 2, column + 2);
# elif d_r == 0:
#   moves.append(row - 1, column + 1);

# else:
# for checker in board_obj.CHECKERS:
#   if checker.startswith('R'):
#     poss_moves = self.GetAllJumps(board_obj, checker, poss_moves);
#     poss_jumps_list, spot, multi = [], [], False;
#     poss_jumps_list = self.CanCheckerJump(board_obj, checker);
#     # if poss_jumps_list != []: # if there are jumps possible
#     for each in poss_jumps_list:
#       new_board = board_obj.CopyBoard();
#       new_board.Move(checker, each[0], each[1]);
#       next_jump = self.CanCheckerJump(new_board, checker);
#       while next_jump != []:
#         multi = True;
#         new_board = new_board.CopyBoard();
#         new_board.Move(checker, next_jump[0][0], next_jump[0][1]);
#         current_jump = next_jump[0];
#         next_jump = [];
#         next_jump = self.CanCheckerJump(new_board, checker);
#       if multi:
#         spot = [current_jump[0], current_jump[1]];
#       else:
#         spot = [each[0], each[1]];
#       poss_moves.append([checker, spot, new_board]);
#       multi = False;
# return poss_moves;

# # given a checker name, return the index for self.board
# def get_checker_index_from_name(self, name):
#   current_row, current_column = 0, 0;
#   num = re.findall('[0-9]', name);
#   num = int(num[0]);
#   for i in range(len(self.board)):
#     try:
#       if num > 9:
#         current_column = self.board[i].index(name);
#       else:
#         current_column = self.board[i].index(name + ' ');
#       current_row = i;
#       return current_row, current_column;
#     except (ValueError) as e:
#       pass;  # print(str(e));

from Interface import Interface
inter = Interface();
hi = [];
hi = inter.CreateGameBoard();
print(type(hi));
print(len(hi.CHECKERS))
hi.PrintBoard();
# last_counts = [0,0,0,0,0,0,1,0,0,0,0]
# print(len(last_counts))
# print(all(x == last_counts[0] for x in last_counts))
