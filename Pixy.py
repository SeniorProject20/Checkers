# from __future__ import print_function;
import pixy, time;
from ctypes import *;
from pixy import *;
from Interface import Interface;

pixy.init();
pixy.change_prog ("color_connected_components");

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint)];

  def get_pixy_data(self):
    pixy.set_lamp (2, 0);
    blocks = BlockArray(40);
    last_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    iter = 0;
    #sample = 0;
    while (1):
      save = True;
      piece_lst = [];
        #  red = 0;
        #  purple = 0;
        #  blue = 0;
        #  green = 0;
        #  pink = 0;
      color = '';
        #  start = time.time();
      count = pixy.ccc_get_blocks(40, blocks);
      if count > 0:
        for index in range(count):
           if blocks[index].m_signature == 1:
              # red += 1;
              color = 'red';
           elif blocks[index].m_signature == 2:
             # blue += 1;
             color = 'blue';
           elif blocks[index].m_signature == 3:
             # purple += 1;
             color = 'purple';
           elif blocks[index].m_signature == 4:
             # green += 1;
             color = 'green';
           elif blocks[index].m_signature == 5:
             # pink += 1;
             color = 'pink';
           #if not (blocks[index].m_x in range(40, 252)) or not (blocks[index].m_y in range(0, 207)):
           piece_lst.append('SIG=%s X=%d Y=%d' % (color, blocks[index].m_x, blocks[index].m_y));
           # print('[SIG = %s X = %d Y = %d AGE = %3d]'%(color, blocks[index].m_x, blocks[index].m_y, blocks[index].m_age));
        last_counts[iter] = count;
        iter = (iter + 1) % 25;
        if (all(x == last_counts[0] for x in last_counts)):
          return piece_lst;
          
        #      print();
        #      print(str(iter));
        #      print('count ' + str(count));
        #      for each in piece_lst:
        #          print(each);
        #    # print('Num Blocks: %d' %count);
        ##    end = time.time();
        ##    print('Iter time: %f' %(end - start));
