from Board import Board;
from Checker import Checker;
# from Game import Game;

class AI:

  # Looks at possible boards and selects best one
  def GetBestMove(self):
    pass

  # determines if there is a jump possible for the current move
  def IsJumpPossible(self, ai_turn, board_obj):
    poss_moves = [];
    try:
      if ai_turn:
        for checker in board_obj.CHECKERS:
          holder = [];
          if checker.startswith('B'):
            holder = self.CanCheckerJump(board_obj, checker);
            if holder != []:
              new_board = self.CreateandCopyExistingBoard(board_obj);
              poss_moves.append(checker, holder);
      else:
        for checker in board_obj.CHECKERS:
          holder = [];
          if checker.startswith('R'):
            holder = self.CanCheckerJump(board_obj, checker);
            if holder != []:
              new_board = self.CreateandCopyExistingBoard(board_obj);
              poss_moves.append(checker, holder);
      return poss_moves;
    except (IndexError):
      pass

  # determins if a given checker can move or if it is trapped
  def CanCheckerMove(self, board_obj, checker):
    try:
      moves = []
      checker_obj = board_obj.get_checker_object_from_name(checker);
      row, column = board_obj.get_checker_index_from_name(checker);

      if checker_obj.isKing:
        if row < 7 and column < 7:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.dest_move_check(u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row > 0 and column < 7:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_move_check(d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_move_check(u_l, 1, -1);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_move_check(d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'black':
        if row < 7 and column < 7:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.dest_move_check(u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_move_check(u_l, 1, -1);
          if dest != None:
            moves.append(dest);
      else:
        if row > 0 and column < 7:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_move_check(d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_move_check(d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError):
      pass
    
  # populates the moves list for CanCheckerMove
  def dest_move_check(self, board_obj, space, v, h):
    if type(space) == Checker.Checker:
      if space.color != checker_obj.color and board_obj.board[row + (v * 2)][column + (h * 2)] == board_obj.FREE_SPACE:
        return row + (v * 2), column + (h * 2);
      else:
        return None;
    elif space == 0:
      return row + (v * 1), column + (h * 1);
    else:
      return None;
    
  # determins if a given checker can move or if it is trapped
  def CanCheckerJump(self, board_obj, checker):
    try:
      moves = []
      checker_obj = board_obj.get_checker_object_from_name(checker);
      row, column = board_obj.get_checker_index_from_name(checker);

      if checker_obj.isKing:
        if row < 6 and column < 6:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.dest_jump_check(board_obj, checker_obj, u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row > 1 and column < 6:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, u_l, 1, -1);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'Black':
        if row < 6 and column < 6:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.dest_jump_check(board_obj, checker_obj, u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, u_l, 1, -1);
          if dest != None:
            moves.append(dest);
      else:
        if row > 1 and column < 6:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError):
      pass
    
  # verifies the jump is legal for CanCheckerMove
  def dest_jump_check(self, board_obj, checker_obj, space, v, h):
    if type(space) == str:
      checker_to_jump_obj = board_obj.get_checker_obj_from_index(v, h)
      if checker_to_jump_obj.color != checker_obj.color and board_obj.board[row + (v * 2)][column + (h * 2)] == board_obj.FREE_SPACE:
        return row + (v * 2), column + (h * 2);
      else:
        return None;
    else:
      return None;

  def CreateandCopyExistingBoard(self, board_obj):
    new_board = board_obj.CopyBoard();
    return new_board;
