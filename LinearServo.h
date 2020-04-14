#ifndef LINEARSERVO_H_
#define LINEARSERVO_H_

#include <asf.h>
#include "Comm.h"
#include "FpgaPwmControl.h"

#define LINEAR_SERVO_TASK_TIME_MS 10

#define DEFAULT_LINEAR_SERVO_SPEED 100

typedef enum
{
    DISABLED,
    CONTROL_SERVO,
}MagnetState;

typedef struct
{
	uint16_t targetPosition;     
}MagnetCmd;

void LinearServoInit(void);

bool LinearServoReadSensorPosition(uint16_t* position);
void LinearServoCmd(MagnetCmd* cmd);
void LinearServoMotorStop(void);
void LinearServoMotorForward(float speed);
void LinearServoMotorReverse(float speed);

void LinearServoAbort(void);

#endif