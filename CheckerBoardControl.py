import CommandInterface as ci
import time

class CheckerBoardControl:
    A1CornerLocation      = (2700, 2900)
    H8CornerLocation      = ( 150,  350)
    ExtraStepsForRemove   = 50
    Speed                 = 12
    Acceleration          = 1
    HomingSpeed           = 8
    MagnetExtendPosition  = 675
    MagnetRetractPosition = 10

    def __init__(self):
        self.comm = ci.CommandInterface()
        self.fullSquareStepsX = int((self.A1CornerLocation[0] - self.H8CornerLocation[0]) / 8)
        self.fullSquareStepsY = int((self.A1CornerLocation[1] - self.H8CornerLocation[1]) / 8)

    def Home(self):
        self.comm.SendCommand("HX", params=[self.HomingSpeed])
        time.sleep(0.5)
        self.comm.SendCommand("HY", params=[self.HomingSpeed])
        time.sleep(0.5)

    def GoToLocation(self, location):
        xSquares = ord(location[0]) - ord('A')
        ySquares = int(location[1]) - 1
        xpos = int(self.A1CornerLocation[0] - (self.fullSquareStepsX * xSquares) - (self.fullSquareStepsX / 2))
        ypos = int(self.A1CornerLocation[1] - (self.fullSquareStepsY * ySquares) - (self.fullSquareStepsY / 2))
        self.comm.SendCommand("GX", params=[xpos, self.Speed, self.Acceleration])
        time.sleep(0.5)
        self.comm.SendCommand("GY", params=[ypos, self.Speed, self.Acceleration])
        time.sleep(0.5)
        
    def GoToLocationEdges(self, location):
        xSquares = ord(location[0]) - ord('A')
        ySquares = int(location[1]) - 1
        xpos = self.A1CornerLocation[0] - (self.fullSquareStepsX * xSquares) - (self.fullSquareStepsX / 2)
        ypos = self.A1CornerLocation[1] - (self.fullSquareStepsY * ySquares) - (self.fullSquareStepsY / 2)
        self.comm.SendCommand("SY", params=[int(-self.fullSquareStepsY / 2), self.Speed, self.Acceleration])
        time.sleep(0.5)
        self.comm.SendCommand("GX", params=[int(xpos - (self.fullSquareStepsX / 2)), self.Speed, self.Acceleration])
        time.sleep(0.5)
        self.comm.SendCommand("GY", params=[ypos, self.Speed, self.Acceleration])
        time.sleep(0.5)
        self.comm.SendCommand("GX", params=[xpos, self.Speed, self.Acceleration])
        time.sleep(0.5)

    def TakePieceOff(self):
        self.comm.SendCommand("SX", params=[int(self.fullSquareStepsX / 2), self.Speed, self.Acceleration])
        time.sleep(0.5)
        self.comm.SendCommand("GY", params=[int(self.A1CornerLocation[1] + self.ExtraStepsForRemove), self.Speed, self.Acceleration])
        time.sleep(0.5)
        
    def MovePiece(self, startLocation, endLocation):
        # goto startLocation
        self.GoToLocation(startLocation)
        time.sleep(0.5)
        # extend magnet
        self.comm.SendCommand("LB", params=[self.MagnetExtendPosition])
        time.sleep(0.5)
        # goto endLocation
        self.GoToLocationEdges(endLocation)
        time.sleep(0.5)
        # retract magnet
        self.comm.SendCommand("LB", params=[self.MagnetRetractPosition])
        time.sleep(0.5)

    def RemovePiece(self, location):
        # goto startLocation
        self.GoToLocation(location)
        time.sleep(0.5)
        # extend magnet
        self.comm.SendCommand("LB", params=[self.MagnetExtendPosition])
        time.sleep(0.5)
        # goto endLocation
        self.TakePieceOff()
        time.sleep(0.5)
        # retract magnet
        self.comm.SendCommand("LB", params=[self.MagnetRetractPosition])
        time.sleep(0.5)
        
