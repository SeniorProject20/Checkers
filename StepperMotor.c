#include "StepperMotor.h"
#include "HomeSensors.h"
#include "Comm.h"
#include "asf.h"

#define X_EN_PIN   PIN_PA03
#define X_DIR_PIN  PIN_PA18
#define X_STEP_PIN PIN_PA19

#define Y_EN_PIN   PIN_PB03
#define Y_DIR_PIN  PIN_PB00
#define Y_STEP_PIN PIN_PB01

#define PUSH_IN  false
#define PULL_OUT true

typedef struct {
	bool direction;
	int steps;
	int currentStep;
	int stepsPerSecond;
	int slowDownPoint;
	uint16_t lastProgrammed;
	struct tc_module timer;
	uint32_t clockFreq;
	int maxStepsPerSecond;
	bool isHoming;
	bool abort;
	bool isHome;
	bool step_value;
	uint8_t stepPin;
	uint8_t enablePin;
	uint8_t directionPin;
	bool (*isHomeFunction)(void);
	int acceleration;
} Stepper;

Stepper xStepper;
Stepper yStepper;

static void SetStepperFrequency(Stepper* stepper);
static void EnableStepperMotor(Stepper* stepper);
static void DisableStepperMotor(Stepper* stepper);
static bool IsStepperHome(Stepper* stepper);
static void XStepCallback(struct tc_module* const module);
static void YStepCallback(struct tc_module* const module);
static void StepCallback(Stepper* stepper, struct tc_module *const module);

void StepperMotorInit(void) {
	// Start off assuming not homed
	xStepper.isHome = false;
	yStepper.isHome = false;
	
	// Set up pointer to function to check for home
	xStepper.isHomeFunction = XHomeRead;
	yStepper.isHomeFunction = YHomeRead;
	
	// Pin configuration for output
	struct port_config pin_conf;
    pin_conf.direction = PORT_PIN_DIR_OUTPUT;
	
	// Set up structures with corresponding pins
	xStepper.enablePin    = X_EN_PIN;
	xStepper.directionPin = X_DIR_PIN;
	xStepper.stepPin      = X_STEP_PIN;
	
	yStepper.enablePin    = Y_EN_PIN;
	yStepper.directionPin = Y_DIR_PIN;
	yStepper.stepPin      = Y_STEP_PIN;
	
	// Set up pin configurations and set to default states
    port_pin_set_config      (xStepper.enablePin, &pin_conf);
    port_pin_set_output_level(xStepper.enablePin, true); // disable motor
    port_pin_set_config      (xStepper.directionPin, &pin_conf);
    port_pin_set_output_level(xStepper.directionPin, false);
    port_pin_set_config      (xStepper.stepPin, &pin_conf);
    port_pin_set_output_level(xStepper.stepPin, false); 
	
	port_pin_set_config      (yStepper.enablePin, &pin_conf);
	port_pin_set_output_level(yStepper.enablePin, true); // disable motor
	port_pin_set_config      (yStepper.directionPin, &pin_conf);
	port_pin_set_output_level(yStepper.directionPin, false);
	port_pin_set_config      (yStepper.stepPin, &pin_conf);
	port_pin_set_output_level(yStepper.stepPin, false); 
	
	// Save off clock frequency
	xStepper.clockFreq  = system_gclk_chan_get_hz(GCLK_GENERATOR_0);
	xStepper.steps = 0;
	
	yStepper.clockFreq  = system_gclk_chan_get_hz(GCLK_GENERATOR_0);
	yStepper.steps = 0;
    
    // Setup timers to control rate of stepper motors
    struct tc_config stepTimerConfig;
    tc_get_config_defaults(&stepTimerConfig);
    stepTimerConfig.counter_size = TC_COUNTER_SIZE_16BIT;
    stepTimerConfig.clock_source = GCLK_GENERATOR_0;
    stepTimerConfig.wave_generation = TC_WAVE_GENERATION_MATCH_FREQ;
	
    tc_init(&xStepper.timer, TC3, &stepTimerConfig);
    tc_register_callback(&xStepper.timer, XStepCallback, TC_CALLBACK_OVERFLOW);
    tc_enable_callback(&xStepper.timer, TC_CALLBACK_OVERFLOW);
	
	tc_init(&yStepper.timer, TC4, &stepTimerConfig);
	tc_register_callback(&yStepper.timer, YStepCallback, TC_CALLBACK_OVERFLOW);
	tc_enable_callback(&yStepper.timer, TC_CALLBACK_OVERFLOW);
}


// Called externally to perform a relative step from the current position.  Parameters 
// are which stepper, how many relative steps, max steps per second, and step max acceleration
void StepperStep(StepperTag stepperTag, int Steps, int maxStepsPerSecond, int acceleration) {
	// Identify the stepper motor you want to move
	Stepper* stepper = NULL;
	if     (stepperTag == X_STEPPER) { stepper = &xStepper; }
	else if(stepperTag == Y_STEPPER) { stepper = &yStepper; }
	
	// Not a valid stepperTag. return
	if(stepper == NULL) {
		SendStringUnsolicitedPacket(chReachedTargetPositionUns, RESPONSE_STATUS_OK, portMAX_DELAY, "UNKNOWN_STEPPER");
		return;
	}
	
	// If no steps then just return
	if(Steps == 0) {
		SendStringUnsolicitedPacket(chReachedTargetPositionUns, RESPONSE_STATUS_OK, portMAX_DELAY, "ALREADY_AT_TARGET");
		return;
	}
	
	// Direction determined by steps being positive or negative
	stepper->direction = (Steps > 0)? PULL_OUT : PUSH_IN;
	// Set the step count down to positive either way
	stepper->steps = (Steps > 0)? Steps : -Steps;
	// Set acceleration in structure
	stepper->acceleration = acceleration;
	// Start off speed at acceleration
	stepper->stepsPerSecond = stepper->acceleration;
	// Set max speed value in structure for later use
	stepper->maxStepsPerSecond = maxStepsPerSecond;
	
	//  If we don't have time to ramp up to max speed just set the midpoint as half way
	if(stepper->maxStepsPerSecond * 2 / stepper->acceleration > stepper->steps) {
		stepper->slowDownPoint = stepper->steps / 2;
	// Otherwise it is set to the point where we hit the max speed
	} else {
		stepper->slowDownPoint = stepper->maxStepsPerSecond / stepper->acceleration;
	}

	// Set the step frequency based on the stepsPerSecond
	SetStepperFrequency(stepper);
	EnableStepperMotor(stepper);
}

void StepperGoToPosition(StepperTag stepperTag, int targetPosition, int maxStepsPerSecond, int acceleration) {
	// Identify the stepper motor you want to move
	Stepper* stepper = NULL;
	if     (stepperTag == X_STEPPER) { stepper = &xStepper; }
	else if(stepperTag == Y_STEPPER) { stepper = &yStepper; }
		
	// Not a valid stepperTag. return
	if(stepper == NULL) { return; }
	
	// Use the same function as for a relative step, just pass in the difference between current and target steps
	StepperStep(stepperTag, targetPosition - stepper->currentStep, maxStepsPerSecond, acceleration);
}

void StepperHome(StepperTag stepperTag, int stepsPerSecond) {
	// Identify the stepper motor you want to move
	Stepper* stepper = NULL;
	if     (stepperTag == X_STEPPER) { stepper = &xStepper; }
	else if(stepperTag == Y_STEPPER) { stepper = &yStepper; }
		
	// Not a valid stepperTag. return
	if(stepper == NULL) { return; }
		
	// Set steps per second manually with no ramp because we can't ramp down
	// becuase we don't know where the sensors are
	stepper->stepsPerSecond = stepsPerSecond;
	stepper->isHoming = true;
	stepper->direction = PUSH_IN;
	
	// Set the step frequency based on the stepsPerSecond
	SetStepperFrequency(stepper);
	EnableStepperMotor(stepper);
}

int StepperGetSteps(StepperTag stepperTag) {
	Stepper* stepper = NULL;
	if     (stepperTag == X_STEPPER) { stepper = &xStepper; }
	else if(stepperTag == Y_STEPPER) { stepper = &yStepper; }
		
	if(stepper == NULL) { return 0; }
		 
	return stepper->currentStep; 
}


static void SetStepperFrequency(Stepper* stepper) {
	// One step is the step pin going high then low so divide freq in hz by stepsPerSecond multiplied by 2
	uint16_t timerCount = stepper->clockFreq / (stepper->stepsPerSecond * 2);
	// Only set the frequency if it's different from the last time it was programmed
	if (timerCount != stepper->lastProgrammed) {
		tc_set_top_value(&stepper->timer, timerCount);
		stepper->lastProgrammed = timerCount;
	}
}

static void EnableStepperMotor(Stepper* stepper) {
	// clear abort flag
	stepper->abort = false;
	// set enable and direction pin
	port_pin_set_output_level(stepper->enablePin, false);
	port_pin_set_output_level(stepper->directionPin, stepper->direction);
	// setup callback for step timer
	tc_enable(&stepper->timer);
	tc_enable_callback(&stepper->timer, TC_CALLBACK_OVERFLOW);
}

static void DisableStepperMotor(Stepper* stepper) {
	// Turn off motor and stop the timer
	stepper->steps = 0;
	port_pin_set_output_level(stepper->enablePin, true);
	tc_disable(&stepper->timer);
}

static bool IsStepperHome(Stepper* stepper) {
	// check return from saved off
	bool retVal = (stepper->isHomeFunction() == false);
	// set current step to 0 if at home
	if (retVal) {
		stepper->currentStep = 0;
	}
	return retVal;
}

// Both callbacks feed into the same handler with their own respective structure
static void XStepCallback(struct tc_module* const module) {
	StepCallback(&xStepper, module);
}

static void YStepCallback(struct tc_module* const module) {
	StepCallback(&yStepper, module);
}

// This gets called at the frequency determined by the stepsPerSecond value
static void StepCallback(Stepper* stepper, struct tc_module *const module) {
	// Control for homing
	if(stepper->isHoming) {
		// Check if home
		if(IsStepperHome(stepper)) {
			// When home stop motor, send response, and set flags
			DisableStepperMotor(stepper);
			SendStringUnsolicitedPacket(chReachedTargetPositionUns, RESPONSE_STATUS_OK, portMAX_DELAY, "OK");
			stepper->isHoming = false;
			stepper->isHome = true;
			return;
		} else {
			//if not at home just toggle step pin
			port_pin_set_output_level(stepper->stepPin, stepper->step_value);
		
			if (stepper->step_value) {
				stepper->step_value = false;
			} else {
				stepper->step_value = true;
			}
		}
	} else {
		// If step counter has reached 0 or abort is called then stop the motor and send response
		if (stepper->steps <= 0 || stepper->abort) {
			DisableStepperMotor(stepper);
			SendStringUnsolicitedPacket(chReachedTargetPositionUns, RESPONSE_STATUS_OK, portMAX_DELAY, "OK");
		} else {
			// Otherwise normal step 
			// set frequency
			SetStepperFrequency(stepper);
			
			// toggle step pin
			port_pin_set_output_level(stepper->stepPin, stepper->step_value);

			// on the positive edge of the step pin toggle
			if (stepper->step_value) {
				// toggle step value
				stepper->step_value = false;
				// decrement step counter
				stepper->steps--;
				// increment or decrement current step depending on direction
				stepper->currentStep += (stepper->direction == PULL_OUT) ? 1 : -1;
				
				// check if at slowDownPoint yet
				if (stepper->steps < stepper->slowDownPoint) {
					// if so start decrementing by acceleration value
					stepper->stepsPerSecond -= stepper->acceleration;
					// if less the acceleration set to acceleration for minimum movement
					if (stepper->stepsPerSecond < stepper->acceleration) {
						stepper->stepsPerSecond = stepper->acceleration;
					}
				// if not at slowDownPoint yet
				} else {
					// increment by acceleration value
					stepper->stepsPerSecond += stepper->acceleration;
					// clip at max speed
					if (stepper->stepsPerSecond > stepper->maxStepsPerSecond) {
						stepper->stepsPerSecond = stepper->maxStepsPerSecond;
					}
				}
			} else {
				// if on negative edge just toggle step value
				stepper->step_value = true;
			}
		}
	}
}