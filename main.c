#include "Comm.h"
#include "EepromInterface.h"
#include "CommonDefines.h"
#include "HbLed.h"
#include "HomeSensors.h"
#include "StepperMotor.h"
#include "SpiControl.h"
#include "LinearServo.h"
#include "NeoPixel.h"
#include "StartButton.h"

#include <asf.h>

#define FILENUM 1

bool my_callback_cdc_enable()  { return true; }
void my_callback_cdc_disable() {              }

int main (void)
{
	system_init();
	delay_init();
	ConfigureEeprom();
    CheckFruRevision();
	ConfigureSpi();
	CommInit();

	HbLedInit();
	HomeSensorsInit();
	StepperMotorInit();
	LinearServoInit();
    NeoPixelInit();
	StartButtonInit();
	StartButtonLEDInit();

	vTaskStartScheduler();

	while (1);
}


