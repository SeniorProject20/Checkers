import CommandInterface as ci;
from CommandInterface import CommandInterface as cmd;
import time;

class CheckerBoardControl:
  A1CornerLocation = (2670, 2900);
  H8CornerLocation = (120, 350);
  ExtraStepsForRemove = 50;
  Speed = 12;
  Acceleration = 5;
  HomingSpeed = 10;
  MagnetExtendPosition = 600;
  MagnetRetractPosition = 10;
  Wait_Time_For_Next_Move = 0.2;
  STAND_ALONE = False;

  def __init__(self):
    self.comm = ci.CommandInterface()
    self.fullSquareStepsX = int((self.A1CornerLocation[0] - self.H8CornerLocation[0]) / 8);
    self.fullSquareStepsY = int((self.A1CornerLocation[1] - self.H8CornerLocation[1]) / 8);

  def Home(self):
    self.comm.SendCommand("HX", params=[self.HomingSpeed])
    time.sleep(self.Wait_Time_For_Next_Move)
    self.comm.SendCommand("HY", params=[self.HomingSpeed])
    time.sleep(self.Wait_Time_For_Next_Move)

  def GoToLocation(self, location):
    xSquares = ord(location[0]) - ord('A');
    ySquares = int(location[1]) - 1;
    xpos = int(self.A1CornerLocation[0] - (self.fullSquareStepsX * xSquares) - (self.fullSquareStepsX / 2));
    ypos = int(self.A1CornerLocation[1] - (self.fullSquareStepsY * ySquares) - (self.fullSquareStepsY / 2));
    self.comm.SendCommand("GX", params=[xpos, self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);
    self.comm.SendCommand("GY", params=[ypos, self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);

  def GoToLocationEdges(self, location):
    xSquares = ord(location[0]) - ord('A');
    ySquares = int(location[1]) - 1;
    xpos = self.A1CornerLocation[0] - (self.fullSquareStepsX * xSquares) - (self.fullSquareStepsX / 2);
    ypos = self.A1CornerLocation[1] - (self.fullSquareStepsY * ySquares) - (self.fullSquareStepsY / 2);
    self.comm.SendCommand("SY", params=[int(-self.fullSquareStepsY / 2), self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);
    self.comm.SendCommand("GX", params=[int(xpos - (self.fullSquareStepsX / 2)), self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);
    self.comm.SendCommand("GY", params=[ypos, self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);
    self.comm.SendCommand("GX", params=[xpos, self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);

  def TakePieceOff(self):
    self.comm.SendCommand("SX", params=[int(self.fullSquareStepsX / 2), self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);
    self.comm.SendCommand("GY", params=[int(self.A1CornerLocation[1] + self.ExtraStepsForRemove),
                                        self.Speed, self.Acceleration]);
    time.sleep(self.Wait_Time_For_Next_Move);

  def MovePiece(self, startLocation, endLocation):
    # goto startLocation
    self.GoToLocation(startLocation);
    time.sleep(self.Wait_Time_For_Next_Move);
    # extend magnet
    self.comm.SendCommand("LB", params=[self.MagnetExtendPosition]);
    time.sleep(self.Wait_Time_For_Next_Move);
    # goto endLocation
    self.GoToLocationEdges(endLocation);
    time.sleep(self.Wait_Time_For_Next_Move);
    # retract magnet
    self.comm.SendCommand("LB", params=[self.MagnetRetractPosition]);
    time.sleep(self.Wait_Time_For_Next_Move);

  def RemovePiece(self, location):
    # goto startLocation
    self.GoToLocation(location);
    time.sleep(self.Wait_Time_For_Next_Move);
    # extend magnet
    self.comm.SendCommand("LB", params=[self.MagnetExtendPosition]);
    time.sleep(self.Wait_Time_For_Next_Move);
    # goto endLocation
    self.TakePieceOff();
    time.sleep(self.Wait_Time_For_Next_Move);
    # retract magnet
    self.comm.SendCommand("LB", params=[self.MagnetRetractPosition]);
    # time.sleep(self.Wait_Time_For_Next_Move);

  def ButtonLEDOn(self, bool):
    if bool:
      cmd.ToggleButtonLED(1);
    else:
      cmd.ToggleButtonLED(0);

  def WaitForButton(self):
    while not cmd.GetButtonState():
      continue;
    start = time.time();
    while cmd.GetButtonState():
      continue;
    end = time.time();
    if (end - start > 3):
      STAND_ALONE = True;
