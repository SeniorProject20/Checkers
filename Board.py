import copy;
from Checker import Checker;

class Board:

  NUM_ROWS = 8;
  NUM_COLUMNS = 8;
  NUM_BLACK = 12;
  NUM_RED = 12;
  FREE_SPACE = '000';
  INVALID_SPACE = None;
  MOVES_WITHOUT_JUMP = 0;
  PRINT_QUEUE = '';

  def __init__(self):
    self.board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]];
    self.CHECKERS = {}; # key: name, value: object

  # creates a board set to begin play
  def InitializeBoard(self):
    self.mark_invalid_spaces();
    self.set_pieces_to_default();
    self.PrintBoard();

  # mark invalid spaces
  def mark_invalid_spaces(self):
    row, column = 0, 0;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if (row + column) % 2:
          self.board[row][column] = self.INVALID_SPACE;
  
  # returns if the position in question is open
  def IsSpaceOpen(self, row, column):
    if self.board[row][column] == self.FREE_SPACE:
      return True;
    else:
      return False;

  # move a checker
  def Move(self, checker_name, new_row, new_column, print = False):
    current_row, current_column = self.get_checker_index_from_name(checker_name);
    checker_obj = self.get_checker_object_from_name(checker_name);
    if self.is_move_valid(checker_obj, current_row, current_column, new_row, new_column):
      self.board[new_row][new_column] = checker_name;
      self.board[current_row][current_column] = self.FREE_SPACE;
      if (new_row == 0 and checker_obj.color == 'red') or (new_row == 7 and checker_obj.color == 'black'):
        self.PRINT_QUEUE = checker_obj.KingMe();
      if print:
        self.PrintBoard();
      return True;
    else:
      return False;

  # check if a move is valid
  def is_move_valid(self, checker_obj, current_row, current_column, new_row, new_column):
    if self.board[new_row][new_column] != self.INVALID_SPACE:
      if self.board[new_row][new_column] == self.FREE_SPACE:
        if abs(current_row - new_row) < 2:
          if self.check_free_space_move(checker_obj, current_row, current_column, new_row, new_column):
            self.MOVES_WITHOUT_JUMP += 1;
            return True;
          else:
            return False;
        else:
          if self.check_single_jump_move(checker_obj, current_row, current_column, new_row, new_column):
            self.MOVES_WITHOUT_JUMP = 0;
            return True;
          else:
            return False;
      else:
        print('Your move to selection was not a free space.');
        return False;
    else:
      print('Your move to selection was not a valid space.');
      return False;

  # proforms a free space move
  def check_free_space_move(self, checker_obj, current_row, current_column, new_row, new_column):
    if checker_obj.isKing:
      if (new_row == (current_row + 1)) or (new_row == (current_row - 1)):
        if (new_column == (current_column + 1)) or (new_column == (current_column - 1)):
          return True;
        else:
          print('Your column selection was wrong.');
          return False;
      else:
        print('Your row selection was wrong.');
        return False;
    elif checker_obj.color == 'black':
      if (new_row == current_row + 1):
        if (new_column == (current_column + 1)) or (new_column == (current_column - 1)):
          return True;
        else:
          print('Your column selection was wrong.');
          return False;
      else:
        print('Your row selection was wrong.');
        return False;
    elif checker_obj.color == 'red':
      if (new_row == (current_row - 1)):
        if (new_column == (current_column + 1)) or (new_column == (current_column - 1)):
          return True;
        else:
          print('Your column selection was wrong.');
          return False;
      else:
        print('Your row selection was wrong.');
        return False;

  # checks to see if a legal jump is possible
  def check_single_jump_move(self, checker_obj, current_row, current_column, new_row, new_column):
    move_left, move_forward = True, True;
    if new_column > current_column:
      move_left = False;
    if new_row < current_row:
      move_forward = False;

    checker_to_jump, r, c = \
      self.get_checker_obj_to_jump(checker_obj, current_row, current_column, move_left, move_forward);
    if checker_to_jump != False:
      if checker_to_jump.color != checker_obj.color:
        if checker_obj.isKing:
          if (new_row == (current_row + 2)) or (new_row == (current_row - 2)):
            if (new_column == (current_column + 2)) or (new_column == (current_column - 2)):
              self.board[r][c] = self.FREE_SPACE;
              self.CHECKERS.pop(checker_to_jump.name);
              del checker_to_jump;
              return True;
            else:
              print('Your column selection was wrong.');
              return False;
          else:
            print('Your row selection was wrong.');
            return False;
        elif checker_obj.color == 'black':
          if (new_row == (current_row + 2)):
            if (new_column == (current_column + 2)) or (new_column == (current_column - 2)):
              self.board[r][c] = self.FREE_SPACE;
              self.CHECKERS.pop(checker_to_jump.name);
              del checker_to_jump;
              return True;
            else:
              print('Your column selection was wrong.');
              return False;
          else:
            print('Your row selection was wrong.');
            return False;
        elif checker_obj.color == 'red':
          if (new_row == (current_row - 2)):
            if (new_column == (current_column + 2)) or (new_column == (current_column - 2)):
              self.board[r][c] = self.FREE_SPACE;
              self.CHECKERS.pop(checker_to_jump.name);
              del checker_to_jump;
              return True;
            else:
              print('Your column selection was wrong.');
              return False;
          else:
            print('Your row selection was wrong.');
            return False;
        else:
          print('Bad color arg.')
          return False;
      else:
        print('Cannot jump your own color.');
        return False;
    else:
      print('checker_to_jump = False.');
      return False;

  # gets the obj of the checker that is to be jumped based on coordinates
  def get_checker_obj_to_jump(self, checker, current_row, current_column, left, move_forward):
    move_up, move_down, move_left, move_right = current_row + 1, current_row - 1, current_column - 1, current_column + 1;
    if move_forward:
      if left:
        if self.board[move_up][move_left] == self.FREE_SPACE or \
            self.get_checker_obj_from_index(move_up, move_left).color == checker.color:
          return False;
        checker_to_jump = self.get_checker_obj_from_index(move_up, move_left);
        return checker_to_jump, move_up, move_left;
      else:
        if self.board[move_up][move_right] == self.FREE_SPACE or \
            self.get_checker_obj_from_index(move_up, move_right).color == checker.color:
          return False;
        checker_to_jump = self.get_checker_obj_from_index(move_up, move_right);
        return checker_to_jump, move_up, move_right;
    else:
      if left:
        if self.board[move_down][move_left] == self.FREE_SPACE or \
            self.get_checker_obj_from_index(move_down, move_left).color == checker.color:
          return False;
        checker_to_jump = self.get_checker_obj_from_index(move_down, move_left);
        return checker_to_jump, move_down, move_left;
      else:
        if self.board[move_down][move_right] == self.FREE_SPACE or \
            self.get_checker_obj_from_index(move_down, move_right).color == checker.color:
          return False;
        checker_to_jump = self.get_checker_obj_from_index(move_down, move_right);
        return checker_to_jump, move_down, move_right;

  # makes a deepcopy of the board passed in
  def CopyBoard(self):
    new_board = Board();
    new_board = copy.deepcopy(self);
    return new_board;

  # given a checker name, return the index for self.board
  def get_checker_index_from_name(self, name):
    current_row, current_column = 0, 0;
    for i in range(len(self.board)):
      try:
        column = self.board[i].index(name);
        current_row = i;
        current_column = column;
        return current_row, current_column;
      except (ValueError) as e:
        pass

  # given a checker name, return the object
  def get_checker_object_from_name(self, name):
    return self.CHECKERS[name];

  # given a checker index, return the object
  def get_checker_obj_from_index(self, row, column):
    name = self.board[row][column];
    return self.CHECKERS[name];

  # sets all checkers to their default position
  def set_pieces_to_default(self):
    b, r = 0, 0;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if (row == 3 or row == 4) and not (self.board[row][column] == self.INVALID_SPACE):
          name = self.FREE_SPACE;
        else:
          if row < 3 and b < self.NUM_BLACK and not (self.board[row][column] == self.INVALID_SPACE):
            if b < 10:
              name = 'B' + str(b) + ' ';
            else:
              name = 'B' + str(b);
            ref = Checker('black', name);
            self.CHECKERS[name] = ref;
            b += 1;
          elif row > 4 and r < self.NUM_RED and not (self.board[row][column] == self.INVALID_SPACE):
            if r < 10:
              name = 'R' + str(r) + ' ';
            else:
              name = 'R' + str(r);
            ref = Checker('red', name);
            self.CHECKERS[name] = ref;
            r += 1;
        if name != None:
          self.board[row][column] = name;
        name = None;

  # print a board in the way we expect to see it
  def PrintBoard(self):
    i, header = 8, '    A      B     C      D      E     F      G     H';
    copy = self.board[::-1]
    print(''); # new line to make new board obvious
    print(header)
    for each in copy:
      print('{} {} {}'.format(str(i), each, str(i)));
      i -= 1;
    print(header);
    if self.PRINT_QUEUE != '':
      print(self.PRINT_QUEUE);
      self.PRINT_QUEUE = '';

  # Trying jump 5
  def InitRiggedBoard1(self):
    self.mark_invalid_spaces();
    name = None;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if self.board[row][column] != self.INVALID_SPACE:
          name = self.FREE_SPACE;
        if name != None:
          self.board[row][column] = name;
        name = None;


    ref = Checker('red', 'R4');
    self.CHECKERS['R4'] = ref;
    self.board[6][2] = 'R4';

    ref = Checker('red', 'R9');
    self.CHECKERS['R9'] = ref;
    self.board[6][4] = 'R9';

    ref = Checker('red', 'R11');
    self.CHECKERS['R11'] = ref;
    self.board[4][2] = 'R11';

    ref = Checker('red', 'R5');
    self.CHECKERS['R5'] = ref;
    self.board[3][3] = 'R5';

    ref = Checker('red', 'R8');
    self.CHECKERS['R8'] = ref;
    self.board[4][6] = 'R8';

    ref = Checker('black', 'B4');
    ref.KingMe();
    self.CHECKERS['B4'] = ref;
    self.board[1][5] = 'B4';
    self.PrintBoard();

  # 4 different jumps poss
  def InitRiggedBoard2(self):
    self.mark_invalid_spaces();
    name = None;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if self.board[row][column] != self.INVALID_SPACE:
          name = self.FREE_SPACE;
        if name != None:
          self.board[row][column] = name;
        name = None;


    ref = Checker('red', 'R4');
    ref.KingMe();
    self.CHECKERS['R4'] = ref;
    self.board[4][4] = 'R4';

    ref = Checker('black', 'B0');
    self.CHECKERS['B0'] = ref;
    self.board[5][5] = 'B0';

    ref = Checker('black', 'B1');
    self.CHECKERS['B1'] = ref;
    self.board[5][3] = 'B1';

    ref = Checker('black', 'B2');
    self.CHECKERS['B2'] = ref;
    self.board[3][5] = 'B2';

    ref = Checker('black', 'B3');
    self.CHECKERS['B3'] = ref;
    self.board[3][3] = 'B3';

    ref = Checker('black', 'B4');
    self.CHECKERS['B4'] = ref;
    self.board[1][5] = 'B4';

    ref = Checker('black', 'B5');
    self.CHECKERS['B5'] = ref;
    self.board[5][1] = 'B5';

    self.PrintBoard();

  # Checking Kinged message
  def InitRiggedBoard3(self):
    self.mark_invalid_spaces();
    name = None;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if self.board[row][column] != self.INVALID_SPACE:
          name = self.FREE_SPACE;
        if name != None:
          self.board[row][column] = name;
        name = None;


    ref = Checker('red', 'R4');
    self.CHECKERS['R4'] = ref;
    self.board[2][4] = 'R4';

    ref = Checker('black', 'B0');
    self.CHECKERS['B0'] = ref;
    self.board[1][5] = 'B0';

    ref = Checker('black', 'B1');
    self.CHECKERS['B1'] = ref;
    self.board[1][3] = 'B1';

    self.PrintBoard();

  # Checking draw game
  def InitRiggedBoard4(self):
    self.mark_invalid_spaces();
    name = None;
    for row in range(self.NUM_ROWS):
      for column in range(self.NUM_COLUMNS):
        if self.board[row][column] != self.INVALID_SPACE:
          name = self.FREE_SPACE;
        if name != None:
          self.board[row][column] = name;
        name = None;

    ref = Checker('red', 'R4');
    ref.KingMe();
    self.CHECKERS['R4'] = ref;
    self.board[5][3] = 'R4';

    ref = Checker('black', 'B0');
    ref.KingMe();
    self.CHECKERS['B0'] = ref;
    self.board[1][5] = 'B0';

if __name__ == '__main__': # for debugging this file
  x = Board();
  x.InitializeBoard();
  for each in x.CHECKERS:
    print(each)
  x.Move('R0', 4,2);
  x.Move('R0',3,3);
  x.Move('B9',4,4);
  x.Move('R1',3,5);
  print(x.IsSpaceOpen(3,1));
  print(x.CHECKERS);

# I will pass down [current_row, current_column, new_row, new_column] to Tyson's board to move piece with steppers.