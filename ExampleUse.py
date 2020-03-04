import CheckerBoardControl as cb;

control = cb.CheckerBoardControl();

control.SetButtonLED(True);
control.WaitForButton();
control.SetButtonLED(False);
control.Home();
# control.MovePiece("D4", "F6");
# control.MovePiece("E5", "D4");
# control.RemovePiece("E5");

