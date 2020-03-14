import re, time;
from Board import Board;
from Checker import Checker;

class Interface():

  def __init__(self):
    self.pixels_per_square = 26;

    # self.BEST_CAMERA_CAPTURE = ['sample 330:',
    # '[SIG=red X=202 Y=88 AGE=255]', #
    # '[SIG=red X=75 Y=110 AGE=255]',
    # '[SIG=pink X=82 Y=62 AGE=255]',
    # # '[SIG=pink X=199 Y=139 AGE=255]', # only leave this for red to show win
    # '[SIG=blue X=227 Y=117 AGE=255]',
    # '[SIG=green X=228 Y=66 AGE=255]',
    # # '[SIG=blue X=99 Y=89 AGE=255]', #
    # '[SIG=red X=55 Y=64 AGE=255]',
    # '[SIG=red X=158 Y=37 AGE=255]',
    # '[SIG=green X=179 Y=63 AGE=255]',
    # '[SIG=blue X=123 Y=166 AGE=255]',
    # '[SIG=blue X=150 Y=88 AGE=255]',
    # '[SIG=green X=106 Y=41 AGE=255]',
    # '[SIG=green X=124 Y=118 AGE=255]'];

    # blue has 2 jumps, red has one
    # self.BEST_CAMERA_CAPTURE = ['[SIG=red X=60 Y=36]',
    # '[SIG=green X=188 Y=170]',
    # '[SIG=red X=158 Y=90]',
    # '[SIG=blue X=109 Y=143]',
    # '[SIG=red X=80 Y=10]',
    # '[SIG=blue X=158 Y=198]',
    # '[SIG=blue X=212 Y=143]',
    # '[SIG=red X=135 Y=67]',
    # '[SIG=blue X=160 Y=146]',
    # '[SIG=red X=240 Y=66]',
    # '[SIG=red X=85 Y=71]',
    # '[SIG=red X=189 Y=68]',
    # '[SIG=blue X=52 Y=200]',
    # '[SIG=blue X=135 Y=169]',
    # '[SIG=red X=110 Y=92]',
    # '[SIG=blue X=105 Y=197]'];

    # blue has 4 jumps
    # self.BEST_CAMERA_CAPTURE = ['[SIG=red X=188 Y=120]',
    # '[SIG=blue X=190 Y=172]',
    # '[SIG=red X=54 Y=35]',
    # '[SIG=red X=158 Y=90]',
    # '[SIG=red X=85 Y=70]',
    # '[SIG=blue X=109 Y=143]',
    # '[SIG=red X=83 Y=119]',
    # '[SIG=blue X=158 Y=198]',
    # '[SIG=red X=135 Y=67]',
    # '[SIG=green X=161 Y=144]',
    # '[SIG=red X=80 Y=12]',
    # '[SIG=blue X=212 Y=144]',
    # '[SIG=red X=240 Y=67]',
    # '[SIG=red X=189 Y=68]',
    # '[SIG=blue X=52 Y=199]',
    # '[SIG=blue X=133 Y=168]',
    # '[SIG=blue X=86 Y=171]'];

    # red has 4 jumps
    # self.BEST_CAMERA_CAPTURE = ['[SIG=red X=160 Y=37]',
    # '[SIG=red X=186 Y=9]',
    # '[SIG=red X=55 Y=36]',
    # '[SIG=red X=135 Y=67]',
    # '[SIG=blue X=135 Y=172]',
    # '[SIG=red X=109 Y=39]',
    # '[SIG=red X=240 Y=66]',
    # '[SIG=red X=81 Y=10]',
    # '[SIG=red X=215 Y=40]',
    # '[SIG=red X=189 Y=68]',
    # '[SIG=blue X=80 Y=118]',
    # '[SIG=blue X=80 Y=66]'];
    
    # No Jumps
    # self.BEST_CAMERA_CAPTURE = ['[SIG=pink X=80 Y=64]',
    # '[SIG=red X=216 Y=40]',
    # '[SIG=blue X=162 Y=196]',
    # '[SIG=red X=135 Y=65]',
    # '[SIG=blue X=214 Y=201]',
    # '[SIG=green X=83 Y=174]',
    # '[SIG=red X=55 Y=35]',
    # '[SIG=blue X=135 Y=174]',
    # '[SIG=blue X=190 Y=171]',
    # '[SIG=red X=240 Y=66]',
    # '[SIG=red X=161 Y=38]',
    # '[SIG=red X=185 Y=10]',
    # '[SIG=red X=189 Y=68]',
    # '[SIG=red X=107 Y=39]',
    # '[SIG=red X=80 Y=11]',
    # '[SIG=blue X=105 Y=198]'];

  def CreateGameBoard(self, piece_lst, ai_turn):
    parsed_lst = [];
#    print(piece_lst)
    board_obj = Board();
    board_obj.InitializeBoard();
    board_obj.AI_TURN = ai_turn;
    # piece_lst = self.BEST_CAMERA_CAPTURE; # REMOVE!!!
    print('# from cam: ' + str(len(piece_lst)))
    parsed_lst = self.parse_camera_data(piece_lst);
    # print(parsed_lst); # just for debug
    board_obj = board_obj.CreateNewBoardFromInterface(parsed_lst);
    return board_obj;

  def parse_camera_data(self, piece_lst):
    pieces = [];
    try:
      for each in piece_lst:
        if re.findall('(X=\S+)', each):
          x_coord = int(self.Strip(re.findall('(X=\d+)', each)));
          y_coord = int(self.Strip(re.findall('(Y=\d+)', each)));
          piece_color = self.Strip(re.findall('(SIG=\S+)', each));
          lst_loc = self.DecodeCoordinates(x_coord, y_coord);
          pieces.append([piece_color, lst_loc]);
      return pieces;
    except (ValueError, IndexError, TypeError) as e:
      print(str(e));

  def DecodeCoordinates(self, x_pos, y_pos):
    x_in = int(round((x_pos - 40) / self.pixels_per_square));
    if x_in > 7:
      x_in = 7;
    if x_in < 0:
      x_in = 0;
    y_loc = int(round(y_pos / self.pixels_per_square));
    if y_loc > 7:
      y_loc = 7;
    if y_loc < 0:
      y_loc = 0;
    x_loc = self.TranslateXToBoard(x_in);
    place = [y_loc, x_loc];
    return place;

  def TranslateXToBoard(self, x):
    COLUMN_KEY = {0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0};
    x_t = list(COLUMN_KEY.keys())[list(COLUMN_KEY.values()).index(x)];
    return x_t;

  def Strip(self, passed_in):
    new = str(passed_in).replace("'", '');
    new = new.replace('"', '');
    new = new.replace(']', '');
    new = new.replace('[', '');
    new = new.replace('X=', '');
    new = new.replace('Y=', '');
    new = new.replace('SIG=', '');
    new = new.strip();
    out = new;

    return out;