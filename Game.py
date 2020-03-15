import time;
from Board import Board;
from Interface import Interface;
from Checker import Checker;
from LookAhead import LookAhead;
# import CheckerBoardControl as cb;
# from Camera import Blocks;


class Game:

  GAME_OVER = False; # Game isn't over till the fat lady sings
  COLUMN_KEY = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7};

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
    return str(column) + str(row);

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
    if r == 0 or bl == 0 or b.MOVES_WITHOUT_JUMP > 14:
      self.GAME_OVER = True;
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
        print('You had only one jump availible, so you moved {} to {} jumping {}'.format(str(in_list[0][0]).strip(' '),
                                                                                         place, pieces));
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
          print('{}: Move {} to {} jumping {}'.format(str(i), str(each[0]).strip(' '), place, pieces));
          i += 1;
      move = input('Which move would you like to make? (1 - ' + str(len(in_list)) + ')');
      return in_list[int(move) - 1];
    except (IndexError):
      pass;

if __name__ == '__main__':
  Game_obj = Game();
  Interface = Interface();
  LA = LookAhead();
  # pixy_obj = Blocks();
  # control = cb.CheckerBoardControl();
  while (1):
    move_counter = 0;
    start_time = time.time();
    B_obj = Board();
    # control.SetButtonLED(False);
    # control.Home();
    first = True;
    while not Game_obj.GAME_OVER:
      # if (move_counter > 4):
      #   # control.Home();
      #   move_counter = 0;
      #   pass;
      if True: #control.STAND_ALONE:
        # control.SetButtonLED(False);
        B_obj.AI_TURN = not B_obj.AI_TURN;
        piece_lst = [];
        # piece_lst = pixy_obj.get_pixy_data();
        if first:
          B_obj = Interface.CreateGameBoard(piece_lst, B_obj.AI_TURN);
          B_obj.PrintBoard();
          first = False;
        move_info = LA.IsJumpPossible(B_obj);
        from_place = str(Game_obj.translate_list_to_board(move_info[4])).replace("'", '');
        to_place = str(Game_obj.translate_list_to_board(move_info[1])).replace("'", '');
        # control.MovePiece(from_place, to_place);
        move_counter += 1;
        if move_info[2] != '':
          for jumped_checkers in move_info[2]:
            location = B_obj.get_checker_location_from_name(jumped_checkers);
            jumped_checker_place = str(Game_obj.translate_list_to_board(location)).replace("'", '');
            move_counter += 1;
            # control.RemovePiece(jumped_checker_place);
          B_obj.MOVES_WITHOUT_JUMP = 0;
          pieces = str(move_info[2]).replace("'", '');
          pieces = pieces.replace('[', '');
          pieces = pieces.replace(']', '');
          pieces = pieces.replace(',', ' &');
          pieces = pieces.replace('  ', ' ');
          if B_obj.AI_TURN:
            print('Blue moved {} to {} jumping {}\n'.format(str(move_info[0]).strip(' '), to_place, pieces));
          else:
            print('Red moved {} to {} jumping {}\n'.format(str(move_info[0]).strip(' '), to_place, pieces));
        else:
          if B_obj.AI_TURN:
            print('Blue moved {} to {}\n'.format(str(move_info[0]).strip(' '), to_place));
          else:
            print('Red moved {} to {}\n'.format(str(move_info[0]).strip(' '), to_place));
        if move_info[5]: # got kinged
          #do something from board control
          pass;
        B_obj = move_info[3];
        B_obj.PrintBoard();

      else:
        # print("AI's turn:");
        # control.SetButtonLED(True);
        # control.WaitForButton();
        # control.SetButtonLED(False);
        piece_lst = [];
        # piece_lst = pixy_obj.get_pixy_data();
        if first:
          B_obj = Interface.CreateGameBoard(piece_lst, True); # always AI turn in this game mode
          B_obj.PrintBoard();
          first = False;
        move_info = LA.IsJumpPossible(B_obj);
        from_place = Game_obj.translate_list_to_board(move_info[4]);
        to_place = Game_obj.translate_list_to_board(move_info[1]);
        # control.MovePiece(from_place, to_place);
        move_counter += 1;
        if move_info[2] != '':
          for jumped_checkers in move_info[2]:
            location = B_obj.get_checker_location_from_name(jumped_checkers);
            jumped_checker_place = str(Game_obj.translate_list_to_board(location));
            # control.RemovePiece(jumped_checker_place);
            move_counter += 1;
          pieces = str(move_info[2]).replace("'", '');
          pieces = pieces.replace('[', '');
          pieces = pieces.replace(']', '');
          pieces = pieces.replace(',', ' &');
          pieces = pieces.replace('  ', ' ');
          print('AI moved {} to {} jumping {}\n'.format(str(move_info[0]).strip(' '), to_place, pieces));
        else:
          print('AI moved {} to {}\n'.format(str(move_info[0]).strip(' '), to_place));
        if move_info[5]: # got kinged
          pass;
          #do something from board control
        B_obj = move_info[3];
        B_obj.PrintBoard();

      if Game_obj.is_game_over(B_obj):
        winner = Game_obj.who_won(B_obj);
        stop_time = time.time();
        if winner[0]:
          if winner[1] == 'Black':
            print('\nGame Over! Blue wins!!\n');
            #set LED blue
          else:
            print('\nGame Over! Red wins!!\n');
            #set LED Red
        else:
          print('\nGame is a Draw\n');
          #do something else
        print('Game took {} minutes.'.format(str((stop_time - start_time) / 60)));
        print('moves: ' + str(move_counter))
        del(B_obj); # deleting game object in preperation of new game
        Game_obj.GAME_OVER = False;
        # control.SetButtonLED(True); # Wait for new game to be acknowledged
        # control.WaitForButton();
        break; # Just start a new game
