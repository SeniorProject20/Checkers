import time;
from Board import Board;
from Checker import Checker;
from LookAhead import CheckJumps;


class Game:

  AI_TURN = False; # Player always moves first
  GAME_OVER = False; # Game isn't over till the fat lady sings
  COLUMN_KEY = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7};

  #test cases
  def test_cases(self, B_obj):

    # Set the board with jumps possible
    B_obj.Move('B9 ', 3, 1);
    B_obj.Move('B9 ', 4, 2);
    B_obj.Move('B10', 3, 3);
    B_obj.Move('B10', 4, 4);
    B_obj.Move('B6 ', 2, 4);
    B_obj.Move('B5 ', 2, 2, True);

    ## Trying jump 5
    # B_obj.InitRiggedBoard1();

    ## 4 different jumps poss
    # B_obj.InitRiggedBoard2();

    ## Checking Kinged message
    # B_obj.InitRiggedBoard3();

    ## Checking draw game
    # B_obj.InitRiggedBoard4();
    # moves = [B_obj.Move('R4', 4, 4), B_obj.Move('R4', 5, 3), B_obj.Move('B0', 2, 4), B_obj.Move('B0', 1, 5)]
    # while True:
    #   for each in moves:
    #     each;
    #   if Game_obj.is_game_over(B_obj):
    #     winner = Game_obj.who_won(B_obj);
    #     stop_time = time.time();
    #     if winner[0]:
    #       print('\n\nGame Over! {} wins!!\n\n'.format(str(winner[1])));
    #     else:
    #       print('Game is a *Draw*');
    #     print('Game took {} minutes.'.format(str((stop_time - start_time) / 60)));
    #     exit(0);
    pass

  # Converting column name to 0-7 index
  def translate_input_to_zero_base(self, input):
    split_in = str(input).split(',');
    column = split_in[1];
    column = self.COLUMN_KEY[column];
    row = int(split_in[0]) - 1;
    return row, column;

  # Convert from 0-7 index to named column
  def translate_list_to_board(self, input):
    row = input[0] + 1;
    column = list(self.COLUMN_KEY.keys())[list(self.COLUMN_KEY.values()).index(input[1])]
    return [row, column];

  # Getting the checker to move from input
  def get_checker_to_move(self, B_obj):
    try:
      piece = input('Which piece would you like to move? (0 - 11)').upper();
      if self.AI_TURN:
        if int(piece) < 10:
          piece = 'B' + piece + ' ';
        else:
          piece = 'B' + piece
      else:
        if int(piece) < 10:
          piece = 'R' + piece + ' ';
        else:
          piece = 'R' + piece;
      if piece in B_obj.CHECKERS:
        if (self.AI_TURN) and (piece.startswith('R')):  # AI can't move Red pieces
          print("Player 2 can't move Red pieces"); # take out with real AI
          return None;
        elif (not self.AI_TURN) and (piece.startswith('B')):  # Player can't move Black pieces
          print("Player 1 can't move Black pieces");
          return None;
        else:
          return piece;
      else:
        print('No piece with that name.')
        return None;
    except (TypeError, ValueError, NameError):
      return None;

  # Getting where to move from input
  def get_move_to_location(self, b):
    try:
      move = input('Where would you like to move it? (1,8),(A-H):').upper();
      row, column  = Game_obj.translate_input_to_zero_base(move);
      if b.board[row][column] != b.INVALID_SPACE:
        if row in range(b.NUM_ROWS):
          if column in range(b.NUM_COLUMNS):
            return row, column;
          else:
            print('Column outside range.');
            return None, None;
        else:
          print('Row outside range.')
          return None, None;
      else:
        print('Invalid space selected.')
        return None, None;
    except (TypeError, ValueError, IndexError, KeyError):
      return None, None;

  # Checks if game is won or draw ** Look for ways to make this FAST **
  def is_game_over(self, b):
    r, bl = 0, 0;
    for each in b.CHECKERS:
      if each.startswith('R'):
        r += 1;
      else: # black checker case
        bl += 1;
    if r == 0 or bl == 0 or b.MOVES_WITHOUT_JUMP >= 15:
      return True;
    else:
      return False;

  # Checks who won or draw
  def who_won(self, B_obj):
    try:
      red, black = 0, 0;
      for each in B_obj.CHECKERS:
        if each.startswith('R'):
          red += 1;
        else:  # black checker case
          black += 1;
      if red == 0:
        return [True, 'Black'];
      elif black == 0:
        return [True, 'Red'];
      else:
        return [False, False];
    except (AttributeError) as e:
      print(str(e))

  # Lets the player select the
  def select_move_from_list(self, in_list):
    i = 1;
    try:
      # poss_moves.append([checker, spot, pieces_to_jump, new_board]); How the packet is stuffed
      if len(in_list) == 1:
        place = str(self.translate_list_to_board(in_list[0][1])).replace("'", '');
        pieces = str(in_list[0][2]).replace("'", '');
        pieces = pieces.replace('[', '');
        pieces = pieces.replace(']', '');
        pieces = pieces.replace(',', ' &');
        print('You had only one jump availible, so you moved {} to {} jumping {}'.format(in_list[0][0], place, pieces));
        move = input('Press any key then enter to continue.');
        return in_list[0];
      else:
        print('Which move would you like to make:');
        for each in in_list:
          place = str(self.translate_list_to_board(each[1])).replace("'", '');
          pieces = str(each[2]).replace("'", '');
          pieces = pieces.replace('[', '');
          pieces = pieces.replace(']', '');
          pieces = pieces.replace(',', ' &');
          print('{}: Move {} to {} jumping {}'.format(str(i), each[0], place, pieces));
          i += 1;
      move = input('Which move would you like to make? (1 - ' + str(len(in_list)) + ')');
      return in_list[int(move) - 1];
    except (IndexError):
      pass;

if __name__ == '__main__':
  start_time = time.time();
  Game_obj = Game();
  LA = CheckJumps();
  B_obj = Board();
  B_obj.InitializeBoard();
  Game_obj.test_cases(B_obj);
  while not Game_obj.GAME_OVER:
    if not Game_obj.AI_TURN: # Players turn
      print("Player 1's turn:");
      jump = LA.IsJumpPossible(Game_obj.AI_TURN, B_obj);
      if jump != []:
        selected = Game_obj.select_move_from_list(jump);
        B_obj = selected[3]; # replacing the board object with the updated one from the jump
        B_obj.MOVES_WITHOUT_JUMP = 0;
        B_obj.PrintBoard();
      else:
        piece = Game_obj.get_checker_to_move(B_obj);
        new_row, new_column = None, None;
        if piece != None:
          new_row, new_column = Game_obj.get_move_to_location(B_obj);
        if new_row != None and new_column != None: #  if no error in input
          if B_obj.Move(piece, new_row, new_column, True):
            pass;
          else:
            print('Invalid move, please try again.');
            Game_obj.AI_TURN = not Game_obj.AI_TURN;  # just to reset it to your move again
        else:
          print('Invalid move, please try again.');
          Game_obj.AI_TURN = not Game_obj.AI_TURN;  # just to reset it to your move again
    else:
      print("AI's turn:");
      st = time.time();
      new_board = LA.IsJumpPossible(Game_obj.AI_TURN, B_obj);
      B_obj = new_board; #jumped count reset
      B_obj.PrintBoard();
      end = time.time()
      print('calc time: ' + str(end - st));
    if Game_obj.is_game_over(B_obj):
      winner = Game_obj.who_won(B_obj);
      stop_time = time.time();
      if winner[0]:
        print('\nGame Over! {} wins!!\n'.format(str(winner[1])));
      else:
        print('\nGame is a Draw\n');
      print('Game took {} minutes.'.format(str((stop_time - start_time) / 60)));
      exit(0);
    Game_obj.AI_TURN = not Game_obj.AI_TURN;