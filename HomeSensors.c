#include "HomeSensors.h"

#include "asf.h"

#define xSwitchPin PIN_PB22
#define ySwitchPin PIN_PB23

void HomeSensorsInit(void) {
	struct port_config pin;
	pin.direction = PORT_PIN_DIR_INPUT;
	port_pin_set_config(xSwitchPin, &pin);
	port_pin_set_config(ySwitchPin, &pin);
}

bool XHomeRead(void) {
	return port_pin_get_input_level(xSwitchPin);
}

bool YHomeRead(void) {
	return port_pin_get_input_level(ySwitchPin);
}
//nSwitch 1 pb22 J14 Pin 1
//nSwitch 2 pb23 J14 Pin 2
//nSwitch 3 pb30 J17 Pin 1
//nSwitch 4 pb31 J17 Pin 2