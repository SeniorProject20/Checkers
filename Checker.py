
class Checker:

  def __init__(self, color, name):
    self.color = color;
    self.name = name;
    self.isKing = False;

  # make a checker a king
  def KingMe(self):
    self.isKing = True;
    print('{} was Kinged!'.format(self.name));

  # repr for and checker
  def __repr__(self):
    return 'Checker({},{})'.format(self.color, self.name);