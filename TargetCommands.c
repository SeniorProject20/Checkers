#include "Comm.h"
#include "HbLed.h"
#include "HomeSensors.h"
#include "StepperMotor.h"
#include "LinearServo.h"
#include "NeoPixel.h"
#include "StartButton.h"
#include <asf.h>
#include <stdbool.h>

void chExampleCommand(CommandPacket* cp)
{
    // example of getting parameters
    ResponsePacket rp;

    int exampleInt = atoi(cp->parameters[0]);
    double exampleDouble = atof(cp->parameters[1]);

    InitializeResponsePacket(&rp, cp, RESPONSE_STATUS_OK);
    AddIntParameterToResponsePacket(&rp, exampleInt);
    AddFloatParameterToResponsePacket(&rp, exampleDouble, 2);
    SendResponsePacket(&rp);

    // and an example of sending an unsolicited packet
    InitializeUnsolicitedPacket(&rp, chExampleUnsolicitedCommand, RESPONSE_STATUS_OK, portMAX_DELAY);
    AddIntParameterToResponsePacket(&rp, exampleInt);
    AddFloatParameterToResponsePacket(&rp, exampleDouble, 2);
    SendResponsePacket(&rp);
}

void chHbLedEnable(CommandPacket* cp) {
	HbLedEnable(atoi(cp->parameters[0]));
	SendResponseSuccess(cp);
}

void chXHomeRead(CommandPacket* cp) {
	bool XHome = XHomeRead();
	SendIntResponsePacket(cp, RESPONSE_STATUS_OK, XHome);
}

void chYHomeRead(CommandPacket* cp) {
	bool YHome = YHomeRead();
	SendIntResponsePacket(cp, RESPONSE_STATUS_OK, YHome);
}

void chStepX(CommandPacket* cp) {
	StepperStep(X_STEPPER, atoi(cp->parameters[0]), atoi(cp->parameters[1]), atoi(cp->parameters[2]));
	SendResponseSuccess(cp);
}

void chStepY(CommandPacket* cp) {
	StepperStep(Y_STEPPER, atoi(cp->parameters[0]), atoi(cp->parameters[1]), atoi(cp->parameters[2]));
	SendResponseSuccess(cp);
}

void chXReadSteps(CommandPacket* cp) {
	SendIntResponsePacket(cp, RESPONSE_STATUS_OK, StepperGetSteps(X_STEPPER));
}

void chYReadSteps(CommandPacket* cp) {
	SendIntResponsePacket(cp, RESPONSE_STATUS_OK, StepperGetSteps(Y_STEPPER));
}

void chXHome(CommandPacket* cp) {
	StepperHome(X_STEPPER, atoi(cp->parameters[0]));
	SendResponseSuccess(cp);
}

void chYHome(CommandPacket* cp) {
	StepperHome(Y_STEPPER, atoi(cp->parameters[0]));
	SendResponseSuccess(cp);
}

void chXGotoPosition(CommandPacket* cp) {
	StepperGoToPosition(X_STEPPER, atoi(cp->parameters[0]), atoi(cp->parameters[1]), atoi(cp->parameters[2]));
	SendResponseSuccess(cp);
}

void chYGotoPosition(CommandPacket* cp) {
	StepperGoToPosition(Y_STEPPER, atoi(cp->parameters[0]), atoi(cp->parameters[1]), atoi(cp->parameters[2]));
	SendResponseSuccess(cp);
}

///////// Linear Servo /////////
void chLinearServoReadSensorPos(CommandPacket * commandPacket)
{
	ResponsePacket responsePacket;
	uint16_t position = 0;

	LinearServoReadSensorPosition(&position);

	InitializeResponsePacket(&responsePacket, commandPacket, RESPONSE_STATUS_OK);
	AddIntParameterToResponsePacket(&responsePacket, position);
	SendResponsePacket(&responsePacket);
}

void chLinearServoGotoSensorPos(CommandPacket* commandPacket)
{
	MagnetCmd cmd;
	cmd.targetPosition = atoi(commandPacket->parameters[0]);

	LinearServoCmd(&cmd);

	SendResponseSuccess(commandPacket);
}

void chLinearServoForward(CommandPacket* commandPacket)
{
	LinearServoMotorForward(100);
	SendResponseSuccess(commandPacket);
}

void chLinearServoReverse(CommandPacket* commandPacket)
{
	LinearServoMotorReverse(100);
	SendResponseSuccess(commandPacket);
}

void chLinearServoStop(CommandPacket* commandPacket)
{
	LinearServoMotorStop();
	SendResponseSuccess(commandPacket);
}

void chTestGetLinearServoMotorFPGArev(CommandPacket * commandPacket)
{
	ResponsePacket responsePacket;
	InitializeResponsePacket(&responsePacket, commandPacket, RESPONSE_STATUS_OK);
	AddIntParameterToResponsePacket(&responsePacket, FpgaPwmGetVersion());
	SendResponsePacket(&responsePacket);
}

///NEOPIXEL///

/// NeoPixel
void chNeoSetRgb(CommandPacket* commandPacket) {
	NeoPixelSetRgb(atoi(commandPacket->parameters[0]), atoi(commandPacket->parameters[1]), atoi(commandPacket->parameters[2]));
	SendResponseSuccess(commandPacket);
}

void chNeoClearPattern(CommandPacket* commandPacket) {
	NeoPixelClearPattern();
	SendResponseSuccess(commandPacket);
}

void chNeoAddColor(CommandPacket* commandPacket) {
	NeoPixelAddColorToPattern(atoi(commandPacket->parameters[0]), atoi(commandPacket->parameters[1]), atoi(commandPacket->parameters[2]));
	SendResponseSuccess(commandPacket);
}

void chNeoClearSequence(CommandPacket* commandPacket) {
	NeoPixelClearSequence();
	SendResponseSuccess(commandPacket);
}

void chNeoAddStep(CommandPacket* commandPacket) {
	NeoPixelAddCurrentPatternToSequence(atoi(commandPacket->parameters[0]));
	SendResponseSuccess(commandPacket);
}

void chNeoAddStepSolid(CommandPacket* commandPacket) {
	NeoPixelAddSolidColorPatternToSequence(atoi(commandPacket->parameters[0]), atoi(commandPacket->parameters[1]), atoi(commandPacket->parameters[2]), atoi(commandPacket->parameters[3]));
	SendResponseSuccess(commandPacket);
}

void chNeoStartSequence(CommandPacket* commandPacket) {
	NeoPixelStartSequence(atoi(commandPacket->parameters[0]), atoi(commandPacket->parameters[1]));
	SendResponseSuccess(commandPacket);
}

///StartButton///

void chStartButtonLED(CommandPacket* cp) {
	StartButtonLED(atoi(cp->parameters[0]));
	SendResponseSuccess(cp);
}

void chStartButtonPress(CommandPacket* cp) {
	bool ButtonPressed = StartButtonPress();
	SendIntResponsePacket(cp, RESPONSE_STATUS_OK, ButtonPressed);
}




void chAbortHardware(CommandPacket* commandPacket)
{
    // This should call the appropriate hardware routines to stop all active control loops
	LinearServoAbort();
    SendResponseSuccess(commandPacket);
}