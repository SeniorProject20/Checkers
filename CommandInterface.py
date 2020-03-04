import serial

def convert_byte_array_to_string_utf8(byteArray):
  return byteArray.decode("utf-8")

def convert_string_to_byte_array(string):
  s = string
  b = bytearray()
  b.extend(map(ord, s))
  return b

class CommandInterface:
  def __init__(self, tty="/dev/ttyACM0"):
    self.connection = serial.Serial(tty)

  def SendCommand(self, commandCode, params=[], unsolicited=True):
    packet = "[A- " + commandCode + "00 "
    for param in params:
      packet += str(param) + " "
    packet += "0]\r\n"
    # print(packet)
    self.connection.write(convert_string_to_byte_array(packet))
    # print(self.connection.readline())
    self.connection.readline();
    if unsolicited == True:
      print("unsol");
      # print(self.connection.readline())
      self.connection.readline();

  def ToggleButtonLED(self, on):
    self.SendCommand('BE', [on], 0);

  def GetButtonState(self):
    self.connection.write(convert_string_to_byte_array("[A- BP00 0 0]"));
    response = self.connection.readline();
    parsed = int(list(str(response).split(' '))[3]);
    if parsed == 1:
      return False;
    else:
      return True;
