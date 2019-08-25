
class Checker:

  def __init__(self, color):
    self.color = color;
    self.isKing = False;


  def KingMe(self):
    self.isKing = True;


  def __repr__(self):
    return 'Checker({})'.format(self.color);


  # def Move(self, row, column):
  #   if self.can_move(row, column):
  #     pass
  #   else:
  #     return False;
  #
  #
  # def can_move(self, row, column):
  #   if self.isKing:
  #     if row == self.row + 1 or row == self.row - 1:
  #       pass
  #   elif self.color == 'red':
  #     if row == self.row + 1:
  #       pass
  #   else:
  #     if row == self.row - 1:
  #       pass
