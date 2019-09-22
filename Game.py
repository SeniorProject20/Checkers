from Board import Board;
from Checker import Checker;
from AI import AI;


class Game:

  AI_TURN = False; # Player always moves first
  GAME_OVER = False; # Game isn't over till the fat lady sings
  COLUMN_KEY = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7};

  # Converting column name to 0-7 index
  def translate_input_to_zero_base(self, input):
    split_in = str(input).split(',');
    column = split_in[1];
    column = self.COLUMN_KEY[column];
    row = int(split_in[0]) - 1;
    return row, column;

  def translate_list_to_board(self, input):
    row = input[0] + 1;
    column = list(self.COLUMN_KEY.keys())[list(self.COLUMN_KEY.values()).index(input[1])]
    return [row, column];

  # Getting the checker to move from input
  def get_checker_to_move(self, caption):
    try:
      piece = input(caption).upper();
      if piece in b.CHECKERS:
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
    except (TypeError, ValueError):
      return None;

  # Getting where to move from input
  def get_move_to_location(self, b):
    try:
      move = input('Where would you like to move it? (1,8),(A-H): ').upper();
      row, column  = game.translate_input_to_zero_base(move);
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

  # is game over ** Look for ways to make this FAST **
  def is_game_over(self, b):
    r, bl = 0, 0;
    for each in b.CHECKERS:
      if each.startswith('R'):
        r += 1;
      else: # black checker case
        bl += 1;
    if r == 0 or bl == 0:
      return True;
    else:
      return False;

  # Checks who won
  def who_won(self, b):
    r, b = 0, 0;
    for each in b.CHECKERS:
      if each.startswith('R'):
        r += 1;
      else:  # black checker case
        b += 1;
    if r == 0:
      return 'Black';
    elif b == 0:
      return 'Red';

  # Lets the player select the
  def select_move_from_list(self, in_list):
    i = 1;
    try:
      # poss_moves.append([checker, spot, pieces_to_jump, new_board]); How the packet is stuffed
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
  game = Game();
  ai = AI();
  b = Board();
  b.InitializeBoard();
  b.Move('B9', 3, 1);
  b.Move('B9', 4, 2);
  b.Move('B10', 3, 3);
  b.Move('B10', 4, 4);
  b.Move('B6', 2, 4);
  b.Move('B5', 2, 2);
  while not game.GAME_OVER:
    if not game.AI_TURN: # Players turn
      print("Player 1's turn:");
      jump = ai.IsJumpPossible(game.AI_TURN, b);
      if jump != []:
        selected = game.select_move_from_list(jump);
        b = selected[3];
        b.PrintBoard();
      else:
        piece = game.get_checker_to_move('Which piece would you like to move? (R0-R11)');
        new_row, new_column = None, None;
        if piece != None:
          new_row, new_column = game.get_move_to_location(b);
        if new_row != None and new_column != None: #  if no error in input
          if b.Move(piece, new_row, new_column):
            pass;
          else:
            print('Invalid move, please try again.');
            game.AI_TURN = not game.AI_TURN;  # just to reset it to your move again
        else:
          print('Invalid move, please try again.');
          game.AI_TURN = not game.AI_TURN;  # just to reset it to your move again
    else:
      # this is where AI will go as soon as logic is developed
      print("Player 2's turn:");
      jump = ai.IsJumpPossible(game.AI_TURN, b);
      if jump != []:
        selected = game.select_move_from_list(jump);
        b = selected[3];
        b.PrintBoard();
      else:
        piece = game.get_checker_to_move('Which piece would you like to move? (B0-B11)');
        new_row, new_column = None, None;
        if piece != None:
          new_row, new_column = game.get_move_to_location(b);
        if new_row != None and new_column != None:  # if no error in input
          if b.Move(piece, new_row, new_column):
            pass;
          else:
            print('Invalid move, please try again');
            game.AI_TURN = not game.AI_TURN;  # just to reset it to your move again
        else:
          print('Invalid move, please try again.');
          game.AI_TURN = not game.AI_TURN;  # just to reset it to your move again
    # AI goes above
    if game.is_game_over(b):
      winner = game.who_won(b);
      print('Game Over! ' + winner + ' wins!!');
    game.AI_TURN = not game.AI_TURN;
