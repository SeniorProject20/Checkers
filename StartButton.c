#include "StartButton.h"

#include "asf.h"

#define startButtonPin PIN_PB30
#define startButtonLEDPin PIN_PB31

void StartButtonInit(void) {
	struct port_config pin;
	pin.direction = PORT_PIN_DIR_INPUT;
	port_pin_set_config(startButtonPin, &pin);
}

void StartButtonLEDInit(void) {
	struct port_config pin;
	pin.direction = PORT_PIN_DIR_OUTPUT;
	port_pin_set_config(startButtonLEDPin, &pin);
	port_pin_set_output_level(startButtonLEDPin, false);
}

bool StartButtonPress(void) {
	return port_pin_get_input_level(startButtonPin);
}

void StartButtonLED(bool enable) {
	port_pin_set_output_level(startButtonLEDPin, enable);
}
//nSwitch 1 pb22 J14 Pin 1
//nSwitch 2 pb23 J14 Pin 2
//nSwitch 3 pb30 J17 Pin 1
//nSwitch 4 pb31 J17 Pin 2