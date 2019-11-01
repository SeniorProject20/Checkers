from Board import Board;
from Checker import Checker;

class CheckJumps:

  # Looks at possible boards and selects best one
  def ChooseBestMove(self, poss_moves, board_obj):
    i, score, best, boards = 0, 0, [], [];

    # if no jumps are possible pick the best possible
    if len(poss_moves) == 0:
      for checker in board_obj.CHECKERS:
        if checker.startswith('B'):
          moves = self.CanCheckerMove(board_obj, checker); # moves = [row, column]
          if len(moves) == 0:
            continue;
          for each in moves:
            # unique to kings
            checker_obj = board_obj.get_checker_object_from_name(checker);
            if checker_obj.isKing:  # point for staying toward the middle
              if each[0] < 6 or each[0] > 2:
                score += 2;
            else:  # unique to non-kings
              score += (each[0]) * 2;
            # common to kings and not kings
            new_board = board_obj.CopyBoard();
            new_board.Move(checker, each[0], each[1]);
            boards.append(new_board);
            check = self.IsJumpPossible(False, new_board)  # checking to see if this move makes me jumpable
            for all in check:
              for jumps in all[2]:
                score -= 20;
            if each[1] < 6 or each[1] > 1:  # points for staying toward the middle
              score += 2;
            best.append(score);
            score = 0;

      x = best.index(max(best));
      return boards[x];

    # if only 1 jump is possible return that board
    if len(poss_moves) == 1:
      return poss_moves[0][3];

    # if multiple jumps are possible, pick the best one
    while (i < len(poss_moves)):
      score = 0;
      # unique to kings
      if Board.get_checker_object_from_name(poss_moves[i][0]).IsKing: # point for staying toward the middle
        if poss_moves[i][1][0] < 6 or poss_moves[i][1][0] > 2:
          score += 2;
      else: # unique to non-kings
        score += (poss_moves[i][1][0]) * 2;
      # common to kings and not kings
      check = self.IsJumpPossible(False, poss_moves[i][3]) # checking to see if this move makes me jumpable
      for each in check:
        for jumps in each[2]:
          score -= 20;
      for each in poss_moves[i][2]: # point for each checker that you can jump
        score += 20;
      if poss_moves[i][1][1] < 6 or poss_moves[i][1][1] > 1: # point for staying toward the middle
        score += 2;
      best.append(score);
      i += 1;

    x = best.index(max(best));
    return poss_moves[x][3];

  # local function to keep track of all jumps possible by a checker
  def get_all_jumps(self, board_obj, checker, poss_moves):
    poss_jumps_list, pieces_to_jump, spot, multi = [], [], [], False;
    poss_jumps_list = self.CanCheckerJump(board_obj, checker);
    for each in poss_jumps_list:
      new_board = board_obj.CopyBoard();
      new_board.Move(checker, each[0], each[1]);
      pieces_to_jump.append(each[2]);
      next_jump = self.CanCheckerJump(new_board, checker);
      while next_jump != []:
        multi = True;
        new_board = new_board.CopyBoard();
        pieces_to_jump.append(next_jump[0][2]);
        new_board.Move(checker, next_jump[0][0], next_jump[0][1]);
        current_jump = next_jump[0];
        next_jump = [];
        next_jump = self.CanCheckerJump(new_board, checker);
      if multi:
        spot = [current_jump[0], current_jump[1]];
      else:
        spot = [each[0], each[1]];
      poss_moves.append([checker, spot, pieces_to_jump, new_board]);
      multi = False;
      pieces_to_jump = [];
    return poss_moves;

  # determines if there is a jump possible for the current move
  def IsJumpPossible(self, ai_turn, board_obj):
    poss_moves = [];
    try:
      if ai_turn:
        for checker in board_obj.CHECKERS:
          if checker.startswith('B'):
            poss_moves = self.get_all_jumps(board_obj, checker, poss_moves);
        return self.ChooseBestMove(poss_moves, board_obj);
      else:
        for checker in board_obj.CHECKERS:
          if checker.startswith('R'):
            poss_moves = self.get_all_jumps(board_obj, checker, poss_moves);
      return poss_moves;
    except (IndexError) as e:
      print(e);

  # determins if a given checker can move or if it is trapped
  def CanCheckerMove(self, board_obj, checker):
    try:
      moves = []
      checker_obj = board_obj.get_checker_object_from_name(checker);
      row, column = board_obj.get_checker_index_from_name(checker);

      if checker_obj.isKing:
        if row < 7 and column < 7:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.dest_move_check(u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 0 and column < 7:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_move_check(d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_move_check(u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_move_check(d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'black':
        if row < 7 and column < 7:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.dest_move_check(u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_move_check(u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
      else:
        if row > 0 and column < 7:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_move_check(d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_move_check(d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError):
      pass
    
  # populates the moves list for CanCheckerMove
  def dest_move_check(self, space, v, h, row, column):
    if space == Board.FREE_SPACE:
      return [row + (v * 1), column + (h * 1)];
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
          dest = self.dest_jump_check(board_obj, checker_obj, u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 1 and column < 6:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'black':
        if row < 6 and column < 6:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.dest_jump_check(board_obj, checker_obj, u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
      else:
        if row > 1 and column < 6:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.dest_jump_check(board_obj, checker_obj, d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError):
      pass
    
  # verifies the jump is legal for CanCheckerMove
  def dest_jump_check(self, board_obj, checker_obj, space, v, h, row, column):
    if str(space).startswith('R') or str(space).startswith('B'):
      checker_to_jump_obj = board_obj.get_checker_object_from_name(space);
      if checker_to_jump_obj.color != checker_obj.color and board_obj.board[row + (v * 2)][column + (h * 2)] == Board.FREE_SPACE:
        new_r = row + (v * 2);
        new_col = column + (h * 2);
        return new_r, new_col, checker_to_jump_obj.name;
      else:
        return None;
    else:
      return None;
