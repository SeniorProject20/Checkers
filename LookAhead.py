from Board import Board;
from Checker import Checker;

class LookAhead:

  NUMBER_OF_LOOK_AHEAD_STEPS = 2;

  # Looks at possible boards and selects best one
  def ChooseBestMove(self, poss_moves, board_obj):
    step, i, score, boards, best = 0, 0, 0, [], [[] for i in range(self.NUMBER_OF_LOOK_AHEAD_STEPS)];
    try:
      letter = 'B' if board_obj.AI_TURN else 'R';
      # if no jumps are possible pick the best possible move
      if len(poss_moves) == 0:
        for checker in board_obj.CHECKERS:
          if checker.startswith(letter):
            row, column = board_obj.get_checker_location_from_name(checker);
            moves = self.CanCheckerMove(board_obj, checker);
            if len(moves) == 0:
              continue;
            for each in moves:
              temp_board = board_obj;
              r, c = each[0], each[1];
              for step in range(self.NUMBER_OF_LOOK_AHEAD_STEPS):
                if self.CanCheckerMove(temp_board, checker):
                  if step == 0:
                    boards, score, new_board_obj = self.CheckFirstTurn(boards, temp_board, checker, r, c, row, column);
                    score = score * 2;
                  else:
                    score, new_board_obj = self.CheckNextTurns(temp_board, checker);
                    score = int(score * (1 / step));
                  best[i].append(score);
                  score = 0;
                  temp_board = new_board_obj;
                  letter = 'B' if letter == 'R' else 'R';
                  temp_board.AI_TURN = not temp_board.AI_TURN;
                  if self.IsGameOver(new_board_obj):
                    break;
            i += 1;
        j, final = 0, [];
        while j < len(best):
          temp_score = sum(best[j]);
          final.append(temp_score);
          j += 1;
        higest = final.index(max(final));
        # higest = [max(x) for x in final];
        # higest = higest.index(max(higest));
        return boards[higest];

      # if jumps are possible, pick the best one, no point in looking further ahead as jumps are mandatory.
      else:
        while (i < len(poss_moves)):
          board_obj = poss_moves[i][3];
          checker = poss_moves[i][0];
          checker_obj = board_obj.get_checker_object_from_name(checker);
          new_board_obj = board_obj.CopyBoard();
          new_board_obj.Move(checker, poss_moves[i][1][0], poss_moves[i][1][1]);
          new_checker_obj = new_board_obj.get_checker_object_from_name(checker);
          became_kinged = (checker_obj.isKing == False) and (new_checker_obj.isKing == True);
          poss_moves[i].append(became_kinged);
          check = self.CheckForOpponentJumps(board_obj) # checking to see if this move makes me jumpable
          if check != []:
            if poss_moves[i][2] != []:
              score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                           became_kinged, len(check[0][2]), len(poss_moves[i][2]));
            else:
              score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                          became_kinged, len(check[0][2]), 0);
          else:
            if poss_moves[i][2] != []:
              score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                          became_kinged, 0, len(poss_moves[i][2]));
            else:
              score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                          became_kinged, 0, 0);
          best[step].append(score);
          score = 0;
          i += 1;
        x = best[step].index(max(best[step]));

      return poss_moves[x];
    except (IndexError, TypeError) as e:
      print('ChooseBestMove ' + str(e));

  def CheckFirstTurn(self, boards, temp_board, checker, r, c, row, column):
    try:
      letter = 'B' if temp_board.AI_TURN else 'R';
      checker_obj = temp_board.get_checker_object_from_name(checker);
      new_board_obj = temp_board.CopyBoard();
      new_board_obj.Move(checker, r, c);
      new_checker_obj = new_board_obj.get_checker_object_from_name(checker);
      # Checking if checker gets kinged because of this move
      became_kinged = (checker_obj.isKing == False) and (new_checker_obj.isKing == True);
      # packing up the same as get_all_jumps
      boards.append([checker, [r, c], '', new_board_obj, [row, column], became_kinged]);
      # checking to see if this move makes me jumpable
      check = self.CheckForOpponentJumps(new_board_obj);
      if check != []:
        score = self.CalculateScore(r, c, letter, checker_obj.isKing, became_kinged, len(check[0][2]), 0);
      else:
        score = self.CalculateScore(r, c, letter, checker_obj.isKing, became_kinged, 0, 0);
      return boards, score, new_board_obj;
    except (IndexError, TypeError) as e:
      print('CheckFirstTurn ' + str(e));

  def CheckNextTurns(self, temp_board, checker):
    poss_moves, most_jumps = [], [];
    try:
      poss_moves = self.GetAllJumps(temp_board, checker, poss_moves);
      if poss_moves != []:
        score, new_return = self.GetBestJumpMove(poss_moves);
      else:
        score, new_return = self.GetBestSingleMove(temp_board);

      new_board_obj = new_return[3];

      return score, new_board_obj;
    except (IndexError, TypeError) as e:
      print('CheckNextTurns ' + str(e));

  def GetBestSingleMove(self, temp_board):
    best, score, boards = [], 0, [];
    try:
      letter = 'B' if temp_board.AI_TURN else 'R';
      for checker in temp_board.CHECKERS:
        if checker.startswith(letter):
          row, column = temp_board.get_checker_location_from_name(checker);
          moves = self.CanCheckerMove(temp_board, checker);
          if len(moves) == 0:
            continue;
          for each in moves:
            r, c = each[0], each[1];
            checker_obj = temp_board.get_checker_object_from_name(checker);
            new_board_obj = temp_board.CopyBoard();
            new_board_obj.Move(checker, r, c);
            new_checker_obj = new_board_obj.get_checker_object_from_name(checker);
            became_kinged = (checker_obj.isKing == False) and (new_checker_obj.isKing == True);
            boards.append([checker, [r, c], '', new_board_obj, [row, column], became_kinged]);  # packing up the same as get_all_jumps
            check = self.CheckForOpponentJumps(new_board_obj);  # checking to see if this move makes me jumpable
            if check != []:
              score = self.CalculateScore(r, c, letter, checker_obj.isKing, became_kinged, len(check[0][2]), 0);
            else:
              score = self.CalculateScore(r, c, letter, checker_obj.isKing, became_kinged, 0, 0);
            best.append(score);
            score = 0;
      x = best.index(max(best));
      return max(best), boards[x];
    except (IndexError, TypeError) as e:
      print('GetBestSingleMove ' + str(e));

  def GetBestJumpMove(self, poss_moves):
    try:
      i, best = 0, [];
      while (i < len(poss_moves)):
        score = 0;
        board_obj = poss_moves[i][3];
        letter = 'B' if board_obj.AI_TURN else 'R';
        checker = poss_moves[i][0];
        checker_obj = board_obj.get_checker_object_from_name(checker);
        new_board_obj = board_obj.CopyBoard();
        new_board_obj.Move(checker, poss_moves[i][1][0], poss_moves[i][1][1]);
        new_checker_obj = new_board_obj.get_checker_object_from_name(checker);
        became_kinged = (checker_obj.isKing == False) and (new_checker_obj.isKing == True);
        poss_moves[i].append(became_kinged);
        check = self.CheckForOpponentJumps(board_obj)  # checking to see if this move makes me jumpable
        check = self.CheckForOpponentJumps(new_board_obj);  # checking to see if this move makes me jumpable
        if check != []:
          if poss_moves[i][2] != []:
            score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                        became_kinged, len(check[0][2]), len(poss_moves[i][2]));
          else:
            score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                        became_kinged, len(check[0][2]), 0);
        else:
          if poss_moves[i][2] != []:
            score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                        became_kinged, 0, len(poss_moves[i][2]));
          else:
            score = self.CalculateScore(poss_moves[i][1][0], poss_moves[i][1][1], letter, checker_obj.isKing,
                                        became_kinged, 0, 0);
        best.append(score);
        i += 1;
      x = best.index(max(best));
      return max(best), poss_moves[x];
    except (IndexError, TypeError) as e:
      print('GetBestJumpMove ' + str(e));

  # Takes all the info from ChooseBestMove to calculate a score
  def CalculateScore(self, row, column, letter, currently_kinged, became_kinged, opp_jumps_poss, my_jumps):
    try:
      score = 0;
      score += self.PointForStayingCenter(column);  # points for staying toward the middle
      if currently_kinged:  # point for staying toward the middle
        score += self.PointForStayingCenter(row) * 2;  # unique to kings
      else:  # unique to non-kings
        score += ((7 - row) * 2) if letter == 'B' else (row * 2);

      if became_kinged:
        score += 15;

      score -= opp_jumps_poss * 20;
      score += my_jumps * 20;

      return score;

    except (IndexError, TypeError) as e:
      print('CalculateScore' + str(e));

  # Calculates more points for staying toward the center of the board
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
  def GetAllJumps(self, board_obj, checker, poss_moves):
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
  def GetNextMove(self, board_obj):
    poss_moves = [];
    try:
      if board_obj.AI_TURN:
        for checker in board_obj.CHECKERS:
          if checker.startswith('B'):
            poss_moves = self.GetAllJumps(board_obj, checker, poss_moves);
        return self.ChooseBestMove(poss_moves, board_obj);
      else:
        for checker in board_obj.CHECKERS:
          if checker.startswith('R'):
            poss_moves = self.GetAllJumps(board_obj, checker, poss_moves);
        return self.ChooseBestMove(poss_moves, board_obj);
    except (IndexError, TypeError) as e:
      print('GetNextMove ' + str(e));

  # Same as GetNextMove, but doesn't recurse for ChooseBestMove
  def CheckForOpponentJumps(self, board_obj):
    poss_moves = [];
    try:
      if not board_obj.AI_TURN:
        for checker in board_obj.CHECKERS:
          if checker.startswith('B'):
            poss_moves = self.GetAllJumps(board_obj, checker, poss_moves);
        return poss_moves;
      else:
        for checker in board_obj.CHECKERS:
          if checker.startswith('R'):
            poss_moves = self.GetAllJumps(board_obj, checker, poss_moves);
      return poss_moves;
    except (IndexError, TypeError) as e:
      print('CheckForOpponentJumps' + str(e));

  # determins if a given checker can move or if it is trapped
  def CanCheckerMove(self, board_obj, checker):
    try:
      moves = []
      checker_obj = board_obj.get_checker_object_from_name(checker);
      row, column = board_obj.get_checker_location_from_name(checker);

      if checker_obj.isKing:
        if row < 7 and column < 7:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.DestMoveCheck(u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 0 and column < 7:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.DestMoveCheck(d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.DestMoveCheck(u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.DestMoveCheck(d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'black':
        if row > 0 and column < 7:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.DestMoveCheck(d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 0 and column > 0:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.DestMoveCheck(d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      else:
        if row < 7 and column < 7:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.DestMoveCheck(u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 7 and column > 0:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.DestMoveCheck(u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError, NameError):
      pass;
    
  # populates the moves list for CanCheckerMove
  def DestMoveCheck(self, space, v, h, row, column):
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
          dest = self.DestJumpCheck(board_obj, checker_obj, u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 1 and column < 6:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.DestJumpCheck(board_obj, checker_obj, d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.DestJumpCheck(board_obj, checker_obj, u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.DestJumpCheck(board_obj, checker_obj, d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      elif checker_obj.color == 'black':
        if row > 1 and column < 6:
          d_r = board_obj.board[row - 1][column + 1];
          dest = self.DestJumpCheck(board_obj, checker_obj, d_r, -1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row > 1 and column > 1:
          d_l = board_obj.board[row - 1][column - 1];
          dest = self.DestJumpCheck(board_obj, checker_obj, d_l, -1, -1, row, column);
          if dest != None:
            moves.append(dest);
      else:
        if row < 6 and column < 6:
          u_r = board_obj.board[row + 1][column + 1];
          dest = self.DestJumpCheck(board_obj, checker_obj, u_r, 1, 1, row, column);
          if dest != None:
            moves.append(dest);
        if row < 6 and column > 1:
          u_l = board_obj.board[row + 1][column - 1];
          dest = self.DestJumpCheck(board_obj, checker_obj, u_l, 1, -1, row, column);
          if dest != None:
            moves.append(dest);
      return moves;
    except (IndexError, TypeError) as e:
      pass;

  # verifies the jump is legal for CanCheckerMove
  def DestJumpCheck(self, board_obj, checker_obj, space, v, h, row, column):
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

  # Checks if game is won or draw
  def IsGameOver(self, b_obj):
    r, bl = 0, 0;
    for each in b_obj.CHECKERS:
      if each.startswith('R'):
        r += 1;
      else: # black checker case
        bl += 1;
    if r == 0 or bl == 0 or b_obj.MOVES_WITHOUT_JUMP > 14:
      self.GAME_OVER = True;
      return True;
    else:
      return False;