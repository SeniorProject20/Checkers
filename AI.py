# from Board import Board;
# from Checker import Checker;
# from Game import Game;

class AI:

  # Looks at possible boards and selects best one
  def GetBestMove(self):
    pass

  # determines if there is a jump possible for the current move
  def IsJumpPossible(self):
    poss_moves, holder = [], [];
    try:
      if Game.AI_TURN:
        for checker in Board.CHECKERS:
          if checker.startswith('B'):
            holder = self.CanCheckerJump(checker);
            if holder != []:
              poss_moves.append(checker, holder);
      else:
        for checker in Board.CHECKERS:
          if checker.startswith('R'):
            holder = self.CanCheckerJump(checker);
            if holder != []:
              poss_moves.append(checker, holder);
      return poss_moves;
    except (IndexError):
      pass

  # determins if a given checker can move or if it is trapped
  def CanCheckerMove(self, checker):
    try:
      moves = []
      checker_obj = Board.get_checker_object_from_name(checker);
      row, column = Board.get_checker_index_from_name(checker);

      if checker_obj.isKing:
        if row < 7 and column < 7:
          u_r = Board.board[row + 1][column + 1];
          dest = self.dest_move_check(u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row > 0 and column < 7:
          d_r = Board.board[row - 1][column + 1];
          dest = self.dest_move_check(d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = Board.board[row + 1][column - 1];
          dest = self.dest_move_check(u_l, 1, -1);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = Board.board[row - 1][column - 1];
          dest = self.dest_move_check(d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'Black':
        if row < 7 and column < 7:
          u_r = Board.board[row + 1][column + 1];
          dest = self.dest_move_check(u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = Board.board[row + 1][column - 1];
          dest = self.dest_move_check(u_l, 1, -1);
          if dest != None:
            moves.append(dest);
      else:
        if row > 0 and column < 7:
          d_r = Board.board[row - 1][column + 1];
          dest = self.dest_move_check(d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = Board.board[row - 1][column - 1];
          dest = self.dest_move_check(d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError):
      pass
    
  # populates the moves list for CanCheckerMove
  def dest_move_check(self, space, v, h):
    if type(space) == Checker.Checker:
      if space.color != checker_obj.color and Board.board[row + (v * 2)][column + (h * 2)] == Board.FREE_SPACE:
        return row + (v * 2), column + (h * 2);
      else:
        return None;
    elif space == 0:
      return row + (v * 1), column + (h * 1);
    else:
      return None;
    
  # determins if a given checker can move or if it is trapped
  def CanCheckerJump(self, checker):
    try:
      moves = []
      checker_obj = Board.get_checker_object_from_name(checker);
      row, column = Board.get_checker_index_from_name(checker);

      if checker_obj.isKing:
        if row < 6 and column < 6:
          u_r = Board.board[row + 1][column + 1];
          dest = self.dest_jump_check(u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row > 1 and column < 6:
          d_r = Board.board[row - 1][column + 1];
          dest = self.dest_jump_check(d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = Board.board[row + 1][column - 1];
          dest = self.dest_jump_check(u_l, 1, -1);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = Board.board[row - 1][column - 1];
          dest = self.dest_jump_check(d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'Black':
        if row < 6 and column < 6:
          u_r = Board.board[row + 1][column + 1];
          dest = self.dest_jump_check(u_r, 1, 1);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = Board.board[row + 1][column - 1];
          dest = self.dest_jump_check(u_l, 1, -1);
          if dest != None:
            moves.append(dest);
      else:
        if row > 1 and column < 6:
          d_r = Board.board[row - 1][column + 1];
          dest = self.dest_jump_check(d_r, -1, 1);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = Board.board[row - 1][column - 1];
          dest = self.dest_jump_check(d_l, -1, -1);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError):
      pass
    
  # populates the jumps list for CanCheckerMove
  def dest_jump_check(self, space, v, h):
    if type(space) == Checker.Checker:
      if space.color != checker_obj.color and Board.board[row + (v * 2)][column + (h * 2)] == Board.FREE_SPACE:
        return row + (v * 2), column + (h * 2);
      else:
        return None;
    else:
      return None;
