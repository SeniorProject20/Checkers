from Board import Board;
from Checker import Checker;

class LookAhead:

  # Looks at possible boards and selects best one
  def ChooseBestMove(self, poss_moves, board_obj):
    i, score, best, boards = 0, 0, [], [];
    try:
      if board_obj.AI_TURN:
        letter = 'B';
      else:
        letter = 'R';
      # if no jumps are possible pick the best possible move
      if len(poss_moves) == 0:
        for checker in board_obj.CHECKERS:
          if checker.startswith(letter):
            row, column = board_obj.get_checker_location_from_name(checker);
            moves = self.CanCheckerMove(board_obj, checker);
            if len(moves) == 0:
              continue;
            for each in moves:
              # unique to kings
              checker_obj = board_obj.get_checker_object_from_name(checker);
              is_king_before = checker_obj.isKing;
              score += self.PointForStayingCenter(each[1]);  # points for staying toward the middle
              if checker_obj.isKing:  # point for staying toward the middle
                score += self.PointForStayingCenter(each[0]) * 2;  # points for staying toward the middle
              else:  # unique to non-kings
                if letter == 'B':
                  score += (7 - each[0]) * 2;
                else:
                  score += each[0] * 2;
              # common to kings and not kings
              new_board_obj = board_obj.CopyBoard();
              new_board_obj.Move(checker, each[0], each[1]);
              checker_obj = new_board_obj.get_checker_object_from_name(checker);
              is_king_after = checker_obj.isKing;
              is_kinged =  (is_king_before == False) and (is_king_after == True); # Push this through all functs
              if is_kinged:
                score += 15;
              boards.append([checker, [each[0], each[1]], '', new_board_obj, [row, column], is_kinged]); # packing up the same as get_all_jumps
              check = self.CheckForOpponentJumps(new_board_obj);  # checking to see if this move makes me jumpable
              if check != []:
                for every in range(len(check[0][2])):
                  score -= 20;
              best.append(score);
              score = 0;
        x = best.index(max(best));
        return boards[x];

      # if jumps are possible, pick the best one
      else:
        while (i < len(poss_moves)):
          score = 0;
          board_obj = poss_moves[i][3];
          checker = poss_moves[i][0];
          # unique to kings
          checker_obj = board_obj.get_checker_object_from_name(checker);
          is_king_before = checker_obj.isKing;
          score += self.PointForStayingCenter(poss_moves[i][1][1]);  # point for staying toward the middle
          if checker_obj.isKing: # point for staying toward the middle
            score += self.PointForStayingCenter(poss_moves[i][1][0]) * 2;
          else: # unique to non-kings
            if letter == 'B':
              score += (7 - (poss_moves[i][1][0])) * 2;
            else:
              score += (poss_moves[i][1][0]) * 2;
          # common to kings and not kings
          new_board_obj = board_obj.CopyBoard();
          new_board_obj.Move(checker, poss_moves[i][1][0], poss_moves[i][1][1]);
          checker_obj = new_board_obj.get_checker_object_from_name(checker);
          is_king_after = checker_obj.isKing;
          is_kinged = (is_king_before == False) and (is_king_after == True);
          if is_kinged:
            score += 15;
          poss_moves[i].append(is_kinged);
          check = self.CheckForOpponentJumps(board_obj) # checking to see if this move makes me jumpable
          if check != []:
            for each in range(len(check[0][2])):
              score -= 20;
          for each in poss_moves[i][2]: # point for each checker that you can jump
            score += 20;
          best.append(score);
          i += 1;
        x = best.index(max(best));
      return poss_moves[x];
    except (IndexError, TypeError) as e:
      print(str(e));

  def PointForStayingCenter(self, position):
    if position == 0 or position == 7:
      return 1;
    if position == 1 or position == 6:
      return 2;
    if position == 2 or position == 5:
      return 3;
    if position == 3 or position == 4:
      return 4;

  # local function to keep track of all jumps possible by a checker
  def get_all_jumps(self, board_obj, checker, poss_moves):
    poss_jumps_list, pieces_to_jump, spot, start_pos, multi = [], [], [], [], False;
    poss_jumps_list = self.CanCheckerJump(board_obj, checker);
    row, column = board_obj.get_checker_location_from_name(checker);
    start_pos = [row, column];
    for each in poss_jumps_list:
      new_board = board_obj.CopyBoard();
      new_board.Move(checker, each[0], each[1]);
      pieces_to_jump.append(each[2]);
      next_jump = self.CanCheckerJump(new_board, checker);
      while next_jump != [] and next_jump != None:
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
      poss_moves.append([checker, spot, pieces_to_jump, new_board, start_pos]);
      multi = False;
      pieces_to_jump = [];
    return poss_moves;

  # determines if there is a jump possible for the current move
  def IsJumpPossible(self, board_obj):
    poss_moves = [];
    try:
      if board_obj.AI_TURN:
        for checker in board_obj.CHECKERS:
          if checker.startswith('B'):
            poss_moves = self.get_all_jumps(board_obj, checker, poss_moves);
        return self.ChooseBestMove(poss_moves, board_obj);
      else:
        for checker in board_obj.CHECKERS:
          if checker.startswith('R'):
            poss_moves = self.get_all_jumps(board_obj, checker, poss_moves);
      return self.ChooseBestMove(poss_moves, board_obj); #poss_moves;
    except (IndexError, TypeError) as e:
      print(e);

  # Same as IsJumpPossible, but doesn't recurse for ChooseBestMove
  def CheckForOpponentJumps(self, board_obj):
    poss_moves = [];
    try:
      if not board_obj.AI_TURN:
        for checker in board_obj.CHECKERS:
          if checker.startswith('B'):
            poss_moves = self.get_all_jumps(board_obj, checker, poss_moves);
        return poss_moves;
      else:
        for checker in board_obj.CHECKERS:
          if checker.startswith('R'):
            poss_moves = self.get_all_jumps(board_obj, checker, poss_moves);
      return poss_moves;
    except (IndexError, TypeError) as e:
      print(e);

  # determins if a given checker can move or if it is trapped
  def CanCheckerMove(self, board_obj, checker):
    try:
      moves = []
      checker_obj = board_obj.get_checker_object_from_name(checker);
      row, column = board_obj.get_checker_location_from_name(checker);

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
      else:
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
      return moves;
    except (IndexError, NameError):
      pass;
    
  # populates the moves list for CanCheckerMove
  def dest_move_check(self, space, v, h, row, column):
    if space == Board.FREE_SPACE:
      return [row + v , column + h];
    else:
      return None;
    
  # determins if a given checker can move or if it is trapped
  def CanCheckerJump(self, board_obj, checker):
    try:
      moves = [];
      checker_obj = board_obj.get_checker_object_from_name(checker);
      row, column = board_obj.get_checker_location_from_name(checker);

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
      else:
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
      return moves;
    except (IndexError, TypeError) as e:
      # print(str(e))
      pass;

  # verifies the jump is legal for CanCheckerMove
  def dest_jump_check(self, board_obj, checker_obj, space, v, h, row, column):
    if str(space).startswith('R') or str(space).startswith('B'):
      checker_to_jump_obj = board_obj.get_checker_object_from_name(space);
      if checker_to_jump_obj.color != checker_obj.color and board_obj.board[row + (v * 2)][column + (h * 2)] == Board.FREE_SPACE:
        new_r = row + (v * 2);
        new_col = column + (h * 2);
        return [new_r, new_col, checker_to_jump_obj.name];
      else:
        return None;
    else:
      return None;
