from Board import Board;
from Checker import Checker;
from Game import Game;

class AI:

  JUMP_MOVE = 10000;

  def __init__(self):
    pass

  # Looks at possible boards and selects best one
  def GetBestMove(self, board):
    pass

  # determines if there is a jump possible for the current move
  def IsJumpPossible(self, board):
    try:
      if Game.AI_TURN: # AI turn
        for each in Board.CHECKERS:
          pass
      else: # players turn, not worrying about this for now
        pass

    except (IndexError):
      pass

  # determins if a given checker can move or if it is trapped
  def CanCheckerMove(self, checker):
    checker_obj = Board.get_checker_object_from_name(checker);
    row, column = Board.get_checker_index_from_name(Board.board, checker);
