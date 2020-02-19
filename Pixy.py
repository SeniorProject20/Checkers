from __future__ import print_function;
import pixy, time;
from ctypes import *;
from pixy import *;
from Board import Board;

pixy.init();
pixy.change_prog ("color_connected_components");

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    # ("m_width", c_uint),
    # ("m_height", c_uint),
    # ("m_angle", c_uint),
    # ("m_index", c_uint),
    ("m_age", c_uint)];

pixy.set_lamp (2, 0);
blocks = BlockArray(40);
last_counts = [];
iter = 0;
# sample = 0;
while 1:
  save = True;
  piece_lst = [];
  red = 0;
  purple = 0;
  blue = 0;
  green = 0;
  pink = 0;
  color = '';
  # start = time.time();
  count = pixy.ccc_get_blocks(40, blocks);
  if count > 0:
    # print('sample %3d:' % (sample));
    # sample += 1;
    for index in range(count):
      if blocks[index].m_signature == 1:
        red += 1;
        color = 'red';
      elif blocks[index].m_signature == 2:
        blue += 1;
        color = 'blue';
      elif blocks[index].m_signature == 3:
        purple += 1;
        color = 'purple';
      elif blocks[index].m_signature == 4:
        green += 1;
        color = 'green';
      elif blocks[index].m_signature == 5:
        pink += 1;
        color = 'pink';
      piece_lst.append('SIG=%s X=%d Y=%d AGE=%3d' % (color, blocks[index].m_x,
             blocks[index].m_y, blocks[index].m_age));
      if blocks[index].m_age != 255:
        save = False;
      # print('[SIG = %s X = %d Y = %d AGE = %3d]' %
      #       (color, blocks[index].m_x,
      #        blocks[index].m_y, blocks[index].m_age));
    last_counts[iter] = count;
    iter = (iter + 1) % 50;
    if save and all(x == last_counts[0] for x in last_counts):
      Board.BEST_CAMERA_CAPTURE = piece_lst;
    # print('Num Blocks: %d' %count);
    # end = time.time();
    # print('Iter time: %f' %(end - start));
