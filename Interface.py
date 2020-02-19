import re;
from Board import Board;
from Checker import Checker;

class Interface():

  BestCameraCapture = ['sample 330:',
                         '[SIG=red X=202 Y=88 AGE=255]',
                         '[SIG=red X=75 Y=110 AGE=255]',
                         '[SIG=pink X=82 Y=62 AGE=255]',
                         '[SIG=pink X=199 Y=139 AGE=255]',
                         '[SIG=blue X=227 Y=117 AGE=255]',
                         '[SIG=green X=228 Y=66 AGE=255]',
                         '[SIG=blue X=99 Y=89 AGE=255]',
                         '[SIG=red X=128 Y=64 AGE=255]',
                         '[SIG=red X=158 Y=37 AGE=255]',
                         '[SIG=green X=179 Y=63 AGE=255]',
                         '[SIG=blue X=123 Y=166 AGE=255]',
                         '[SIG=blue X=150 Y=88 AGE=255]',
                         '[SIG=green X=106 Y=41 AGE=255]',
                         '[SIG=green X=124 Y=118 AGE=255]'];

  def __init__(self):
    self.pixels_per_square = 26;

  def CreateGameBoard(self):
    board = Board();
    board.InitializeBoard();
    parsed_lst = [];
    parsed_lst = self.parse_camera_data();
    board = board.CreateNewBoardFromInterface(parsed_lst);
    return board;

  def parse_camera_data(self):
    pieces = [];
    try:
      for each in self.BestCameraCapture: #Board.BEST_CAMERA_CAPTURE:
        if self.Strip(re.findall('(X=\S+)', each)):
          x_coord = int(self.Strip(re.findall('(X=\d+)', each)));
          y_coord = int(self.Strip(re.findall('(Y=\d+)', each)));
          piece_color = self.Strip(re.findall('(SIG=\S+)', each));
          lst_loc = self.DecodeCoordinates(x_coord, y_coord);
          pieces.append([piece_color, lst_loc]);
      return pieces;
    except (ValueError, IndexError, TypeError) as e:
      print(str(e));

  def DecodeCoordinates(self, x_pos, y_pos):
    x_in = round((x_pos - 40) / self.pixels_per_square);
    y_loc = round((int(y_pos) / self.pixels_per_square));
    x_loc = self.TranslateXToBoard(x_in);
    place = [y_loc, x_loc];
    return place;

  def TranslateXToPacket(self, x):
    COLUMN_KEY = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1, 'H': 0};
    x_t = list(COLUMN_KEY.keys())[list(COLUMN_KEY.values()).index(x)];
    return x_t;

  def TranslateXToBoard(self, x):
    COLUMN_KEY = {0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0};
    x_t = list(COLUMN_KEY.keys())[list(COLUMN_KEY.values()).index(x)];
    return x_t;

  def WaitForButton(self):
    while not(Board.AI_Turn):
      time.sleep(0.05);
    Board.AI_Turn = False;


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