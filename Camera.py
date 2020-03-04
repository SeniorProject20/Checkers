from __future__ import print_function;
import pixy;
from ctypes import *;
from pixy import *;

pixy.init();
pixy.change_prog ("color_connected_components");

class Blocks (Structure):

  def get_pixy_data(self):
    _fields_ = [("m_signature", c_uint),
                ("m_x", c_uint),
                ("m_y", c_uint)];
    pixy.set_lamp (2, 0);
    blocks = BlockArray(100);
    num_iter = 25;
    last_counts = [];
    for i in range(num_iter):
      last_counts.append(0);
    iter = 0;
    while (1):
      save = True;
      piece_lst = [];
      color = '';
      count = pixy.ccc_get_blocks(100, blocks);
      if count > 0:
    # print('count' + str(count))
        for index in range(count):
          if blocks[index].m_signature == 1:
            color = 'red';
          elif blocks[index].m_signature == 2:
           color = 'blue';
          elif (blocks[index].m_signature == 3) or (blocks[index].m_signature == 5):
            color = 'pink';
          elif blocks[index].m_signature == 4:
            color = 'green';
#          if not (blocks[index].m_x in range(40, 252)) or not (blocks[index].m_y in range(0, 207)):
#            save = False;
#          else:
          piece_lst.append('SIG=%s X=%d Y=%d' % (color, blocks[index].m_x, blocks[index].m_y));
           # print('[SIG = %s X = %d Y = %d]'%(color, blocks[index].m_x, blocks[index].m_y));
        last_counts[iter] = count;
        iter = (iter + 1) % num_iter;
        if save and (all(x == last_counts[0] for x in last_counts)):
          return piece_lst;

if __name__ == '__main__':
  bl = Blocks();
  while (1):
    piece_lst = bl.get_pixy_data();
    print('len: ' + str(len(piece_lst)));
    for each in piece_lst:
      print(each);
    print('');
