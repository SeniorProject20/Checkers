import CheckerBoardControl as cb;

control = cb.CheckerBoardControl();

control.ButtonLEDOn(True);
control.WaitForButton();
control.ButtonLEDOn(False);
control.Home();
# control.MovePiece("D4", "F6");
# control.MovePiece("E5", "D4");
# control.RemovePiece("E5");

