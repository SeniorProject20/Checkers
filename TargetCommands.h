/*Reserved Command Codes
"FR"
"FW"
"GV"
"HB"
"RT"
"EB"
"BV"
"BB"
"SN"
"AB"
*/

// DEVICENAME: RTU Template,A

// TABNAME: HB LED
LUA_DEF_COMMAND(hb_led_enable, "HE", GENERIC_FRU_COMMAND, "status hb_led_enable(bool enable)")
LUA_IN_COMMAND(hb_led_enable, LUA_PARAMETER_BOOLEAN)
LUA_OUT_COMMAND(hb_led_enable, LUA_PARAMETER_STATUS)
RTU_COMMAND("HE", chHbLedEnable, 1)

// TABNAME: HOME SENSORS
LUA_DEF_COMMAND(x_home_read, "RX", GENERIC_FRU_COMMAND, "bool, status x_home_read()")
LUA_OUT_COMMAND(x_home_read, LUA_PARAMETER_BOOLEAN)
LUA_OUT_COMMAND(x_home_read, LUA_PARAMETER_STATUS)
RTU_COMMAND("RX", chXHomeRead, 0)

LUA_DEF_COMMAND(y_home_read, "RY", GENERIC_FRU_COMMAND, "bool, status y_home_read()")
LUA_OUT_COMMAND(y_home_read, LUA_PARAMETER_BOOLEAN)
LUA_OUT_COMMAND(y_home_read, LUA_PARAMETER_STATUS)
RTU_COMMAND("RY", chYHomeRead, 0)

// TABNAME: STEP
LUA_DEF_COMMAND(step_x, "SX", GENERIC_FRU_COMMAND, "status step_x(int steps, int maxStepsPerSecond, int acceleration)")
LUA_IN_COMMAND(step_x, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(step_x, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(step_x, LUA_PARAMETER_INTEGER)
LUA_RES_COMMAND(step_x, "XY")
LUA_OUT_COMMAND(step_x, LUA_PARAMETER_STATUS)
RTU_COMMAND("SX", chStepX, 3)

LUA_DEF_COMMAND(step_y, "SY", GENERIC_FRU_COMMAND, "status step_y(int steps, int maxStepsPerSecond, int acceleration)")
LUA_IN_COMMAND(step_y, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(step_y, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(step_y, LUA_PARAMETER_INTEGER)
LUA_RES_COMMAND(step_y, "XY")
LUA_OUT_COMMAND(step_y, LUA_PARAMETER_STATUS)
RTU_COMMAND("SY", chStepY, 3)

LUA_DEF_COMMAND(x_read_steps, "Sx", GENERIC_FRU_COMMAND, "int, status x_read_steps()")
LUA_OUT_COMMAND(x_read_steps, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(x_read_steps, LUA_PARAMETER_STATUS)
RTU_COMMAND("Sx", chXReadSteps, 0)

LUA_DEF_COMMAND(y_read_steps, "Sy", GENERIC_FRU_COMMAND, "int, status y_read_steps()")
LUA_OUT_COMMAND(y_read_steps, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(y_read_steps, LUA_PARAMETER_STATUS)
RTU_COMMAND("Sy", chYReadSteps, 0)

LUA_DEF_COMMAND(x_home, "HX", GENERIC_FRU_COMMAND, "status x_home(int stepsPerSecond)")
LUA_IN_COMMAND(x_home, LUA_PARAMETER_INTEGER)
LUA_RES_COMMAND(x_home, "XY")
LUA_OUT_COMMAND(x_home, LUA_PARAMETER_STATUS)
RTU_COMMAND("HX", chXHome, 1)

LUA_DEF_COMMAND(y_home, "HY", GENERIC_FRU_COMMAND, "status y_home(int stepsPerSecond)")
LUA_IN_COMMAND(y_home, LUA_PARAMETER_INTEGER)
LUA_RES_COMMAND(y_home, "XY")
LUA_OUT_COMMAND(y_home, LUA_PARAMETER_STATUS)
RTU_COMMAND("HY", chYHome, 1)

LUA_DEF_COMMAND(x_goto_pos, "GX", GENERIC_FRU_COMMAND, "status x_goto_pos(int targetPosition, int maxStepsPerSecond, int acceleration)")
LUA_IN_COMMAND(x_goto_pos, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(x_goto_pos, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(x_goto_pos, LUA_PARAMETER_INTEGER)
LUA_RES_COMMAND(x_goto_pos, "XY")
LUA_OUT_COMMAND(x_goto_pos, LUA_PARAMETER_STATUS)
RTU_COMMAND("GX", chXGotoPosition, 3)

LUA_DEF_COMMAND(y_goto_pos, "GY", GENERIC_FRU_COMMAND, "status y_goto_pos(int targetPosition, int maxStepsPerSecond, int acceleration)")
LUA_IN_COMMAND(y_goto_pos, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(y_goto_pos, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(y_goto_pos, LUA_PARAMETER_INTEGER)
LUA_RES_COMMAND(y_goto_pos, "XY")
LUA_OUT_COMMAND(y_goto_pos, LUA_PARAMETER_STATUS)
RTU_COMMAND("GY", chYGotoPosition, 3)

RTU_UNSOLICITED("XY", chReachedTargetPositionUns)

// TABNAME: LinearServo
LUA_DEF_COMMAND(linear_servo_goto_sensor_position, "LB", GENERIC_FRU_COMMAND, "bool,infoString linear_servo_goto_sensor_position(string servoName, int position, {int stepSize})\\n")
LUA_IN_COMMAND(linear_servo_goto_sensor_position, LUA_PARAMETER_INTEGER)
LUA_RES_COMMAND(linear_servo_goto_sensor_position, "OS")
LUA_OUT_COMMAND(linear_servo_goto_sensor_position, LUA_PARAMETER_STATUS)
LUA_OUT_COMMAND(linear_servo_goto_sensor_position, LUA_PARAMETER_STRING)
RTU_COMMAND("LB", chLinearServoGotoSensorPos, 1) // Parameters(s): linear_servo_goto_sensor_position(int position)

LUA_DEF_COMMAND(linear_servo_read_sensor_position, "LI", GENERIC_FRU_COMMAND, "int,status,infoString linear_servo_read_sensor_position()\\n")
LUA_OUT_COMMAND(linear_servo_read_sensor_position, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(linear_servo_read_sensor_position, LUA_PARAMETER_STATUS)
LUA_OUT_COMMAND(linear_servo_read_sensor_position, LUA_PARAMETER_STRING)
RTU_COMMAND("LI", chLinearServoReadSensorPos, 0) // Parameters(s): linear_servo_read_sensor_position()

RTU_UNSOLICITED("OS", chLinearServoGotoPositionUns)
RTU_UNSOLICITED("EV", chLinearServoDebugUns)

RTU_COMMAND("T1", chTestGetLinearServoMotorFPGArev, 0)

RTU_COMMAND("LF", chLinearServoForward, 1)
RTU_COMMAND("LR", chLinearServoReverse, 1)
RTU_COMMAND("LS", chLinearServoStop,    0)

// TABNAME: NeoPixel
LUA_DEF_COMMAND(neo_set_rgb, "NR", GENERIC_FRU_COMMAND, "status neo_set_rgb(int red, int green, int blue)\\n 0-255 for values\\n")
LUA_IN_COMMAND(neo_set_rgb, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_set_rgb, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_set_rgb, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(neo_set_rgb, LUA_PARAMETER_STATUS)
RTU_COMMAND("NR", chNeoSetRgb, 3)

LUA_DEF_COMMAND(neo_clear_pattern, "NL", GENERIC_FRU_COMMAND, "status,infoString neo_clear_pattern()\n Clears neopixel pattern\\n")
LUA_OUT_COMMAND(neo_clear_pattern, LUA_PARAMETER_STATUS)
RTU_COMMAND("NL", chNeoClearPattern, 0)

LUA_DEF_COMMAND(neo_add_color, "NP", GENERIC_FRU_COMMAND, "status neo_add_color(int red, int green, int blue)\n(0-255) rgb values\\n")
LUA_IN_COMMAND(neo_add_color, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_add_color, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_add_color, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(neo_add_color, LUA_PARAMETER_STATUS)
RTU_COMMAND("NP", chNeoAddColor, 3)

LUA_DEF_COMMAND(neo_clear_sequence, "NC", GENERIC_FRU_COMMAND, "status,infoString neo_clear_sequence()\n Clears neopixel sequence\\n")
LUA_OUT_COMMAND(neo_clear_sequence, LUA_PARAMETER_STATUS)
RTU_COMMAND("NC", chNeoClearSequence, 0)

LUA_DEF_COMMAND(neo_add_step, "NA", GENERIC_FRU_COMMAND, "status neo_add_step(int fadeTime_ms)\\n Add current pattern\\n")
LUA_IN_COMMAND(neo_add_step, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(neo_add_step, LUA_PARAMETER_STATUS)
RTU_COMMAND("NA", chNeoAddStep, 1)

LUA_DEF_COMMAND(neo_add_step_solid, "NO", GENERIC_FRU_COMMAND, "status neo_add_step_solid(int red, int green, int blue, int fadeTime_ms)\n(0-255) rgb values\\n")
LUA_IN_COMMAND(neo_add_step_solid, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_add_step_solid, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_add_step_solid, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_add_step_solid, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(neo_add_step_solid, LUA_PARAMETER_STATUS)
RTU_COMMAND("NO", chNeoAddStepSolid, 4)

LUA_DEF_COMMAND(neo_start_sequence, "NS", GENERIC_FRU_COMMAND, "status,infoString neo_start_sequence(int loopCount, int loopBackIndex)\\n")
LUA_IN_COMMAND(neo_start_sequence, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND(neo_start_sequence, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(neo_start_sequence, LUA_PARAMETER_STATUS)
RTU_COMMAND("NS", chNeoStartSequence, 2)

// TABNAME: StartButton
LUA_DEF_COMMAND(startButton_led_enable, "BE", GENERIC_FRU_COMMAND, "status start_button_led_enable(bool enable)")
LUA_IN_COMMAND(startButton_led_enable, LUA_PARAMETER_BOOLEAN)
LUA_OUT_COMMAND(startButton_led_enable, LUA_PARAMETER_STATUS)
RTU_COMMAND("BE", chStartButtonLED, 1)

LUA_DEF_COMMAND(start_button_pressed, "BP", GENERIC_FRU_COMMAND, "bool, status start_button_pressed()")
LUA_OUT_COMMAND(start_button_pressed, LUA_PARAMETER_BOOLEAN)
LUA_OUT_COMMAND(start_button_pressed, LUA_PARAMETER_STATUS)
RTU_COMMAND("BP", chStartButtonPress, 0)

// TABNAME: Template
LUA_DEF_COMMAND(example, "XX", GENERIC_FRU_COMMAND, "status,int,double example(int, double)\n Used to show how to create a command.")
LUA_IN_COMMAND(example, LUA_PARAMETER_INTEGER)
LUA_IN_COMMAND_CONSTANT(example, "5")
LUA_IN_COMMAND(example, LUA_PARAMETER_FLOAT)
LUA_OUT_COMMAND(example, LUA_PARAMETER_STATUS)
LUA_OUT_COMMAND(example, LUA_PARAMETER_INTEGER)
LUA_OUT_COMMAND(example, LUA_PARAMETER_FLOAT)
RTU_COMMAND("XX", chExampleCommand, 3) // Parameter(s): exampleInt (int), exampleDouble (double) \n ReturnValue(s): exampleInt (int), exampleDouble (double)

RTU_UNSOLICITED("xx", chExampleUnsolicitedCommand)

LUA_QUERYABLE("ExampleInt", "0", LUA_QUERYABLE_NOT_CHANGEABLE)
LUA_QUERYABLE("ExampleDouble", "0.0", LUA_QUERYABLE_NOT_CHANGEABLE)

LUA_UNSOLICITED_COMMAND("xx", UPDATE_QUERYABLE, "0", "ExampleInt")
LUA_UNSOLICITED_COMMAND("xx", UPDATE_QUERYABLE, "1", "ExampleDouble")
