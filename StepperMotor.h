#ifndef STEPPERMOTOR_H_
#define STEPPERMOTOR_H_

typedef enum {
	X_STEPPER,
	Y_STEPPER,
}StepperTag;

void StepperMotorInit   (void);
int  StepperGetSteps    (StepperTag stepperTag);
void StepperStep        (StepperTag stepperTag, int Steps,          int maxStepsPerSecond, int acceleration);
void StepperGoToPosition(StepperTag stepperTag, int targetPosition, int maxStepsPerSecond, int acceleration);
void StepperHome        (StepperTag stepperTag, int stepsPerSecond);

#endif