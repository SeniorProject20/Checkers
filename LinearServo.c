#include "LinearServo.h"
#include "Comm.h"
#include "AdcArray.h"
#include "SpiControl.h"
#include "ProjectDefines.h"
#include "AdcArray.h"

typedef struct
{
    FpgaPwm         fpgaPwm;
    AdcName         adc;
    float           targetPosition;
    uint16_t        currentPosition;
    bool			isAtTarget;
    MagnetState		state;
    MagnetCmd       cmd;
    QueueHandle_t   cmdQ;
    TickType_t      qWaitDelay;
} MagnetData;


MagnetData magnetServo = {.fpgaPwm = MAG_MOT,  .adc = MAGNET_LINEAR_SERVO_FB, .state = DISABLED};

static TaskHandle_t LinearServoTaskId;

static void LinearServoTask(void *p);

static void LinearServoDisable(void);
static void LinearServoStateMachine(bool directionIsForward);
static void SetPidParamsForMagnet(void);

void LinearServoInit(void)
{
	magnetServo.qWaitDelay = portMAX_DELAY;
    magnetServo.cmdQ = xQueueCreate(1, sizeof(MagnetCmd));

    xTaskCreate(LinearServoTask, "LinearServo", LINEAR_SERVO_TASK_STACK, NULL, LINEAR_SERVO_TASK_PRIORITY, &LinearServoTaskId);
}

static void LinearServoDisable()
{
    LinearServoMotorStop();
    magnetServo.state = DISABLED;
}

void LinearServoCmd(MagnetCmd* cmd)
{
    if ( xQueueSend(magnetServo.cmdQ, cmd, (LINEAR_SERVO_TASK_TIME_MS + 1) * portTICK_PERIOD_MS) != pdTRUE ) {
		//ERROR Command is already in progress
    }
}

bool LinearServoReadSensorPosition(uint16_t* position)
{
    return AdcArrayReadValue(magnetServo.adc, position);
}

 void LinearServoMotorForward(float speed)
{
    FpgaPwmSetPwm(magnetServo.fpgaPwm, true, (uint16_t)((speed * 4095.0) / 100.0));
}

 void LinearServoMotorReverse(float speed)
{
    FpgaPwmSetPwm(magnetServo.fpgaPwm, false, (uint16_t)((speed * 4095.0) / 100.0));
}

 void LinearServoMotorStop()
{
    FpgaPwmSetPwm(magnetServo.fpgaPwm, true, 0);
}

void LinearServoAbort()
{
    LinearServoDisable();
    xQueueReset(magnetServo.cmdQ);
    magnetServo.qWaitDelay = portMAX_DELAY;
    SendStringUnsolicitedPacket(chLinearServoGotoPositionUns, RESPONSE_STATUS_ER, 2, "LINEAR_SERVO_ABORT");
}

static void LinearServoTask(void *p)
{
    TickType_t previousWakeTime;
	
    AdcArrayReadValue(magnetServo.adc, &magnetServo.currentPosition);
    magnetServo.targetPosition = 0;
    LinearServoDisable();
    
    while(1){
        if(xQueueReceive(magnetServo.cmdQ, &magnetServo.cmd, magnetServo.qWaitDelay) == pdTRUE){    
            magnetServo.targetPosition = magnetServo.cmd.targetPosition;
            magnetServo.isAtTarget     = false;
            magnetServo.state          = CONTROL_SERVO;         
        }
        previousWakeTime = xTaskGetTickCount();
        
        if(magnetServo.state == DISABLED){
	        magnetServo.qWaitDelay = portMAX_DELAY;
	        } else{
	        magnetServo.qWaitDelay = 0;
	        LinearServoStateMachine();

	        if(magnetServo.isAtTarget){
		        SendStringUnsolicitedPacket(chLinearServoGotoPositionUns, RESPONSE_STATUS_OK, 2, "AtTarget");
		        LinearServoDisable();
	        }
        }
        vTaskDelayUntil(&previousWakeTime, LINEAR_SERVO_TASK_TIME_MS * portTICK_PERIOD_MS);                   
    }
}

static void LinearServoStateMachine(bool directionIsForward)
{
    switch(magnetServo.state)
    {
        case DISABLED:
        break;
        
        case CONTROL_SERVO:
			AdcArrayReadValue(magnetServo.adc, &magnetServo.currentPosition);

            if(directionIsForward){
                LinearServoMotorForward(DEFAULT_LINEAR_SERVO_SPEED);
            } else {
                LinearServoMotorReverse(DEFAULT_LINEAR_SERVO_SPEED);  
            }

            if(directionIsForward){
                if(magnetServo.currentPosition >= magnetServo.targetPosition){
                    LinearServoMotorStop();
                    magnetServo.isAtTarget = true;
                }
            } else{
                if(magnetServo.currentPosition <= magnetServo.targetPosition){
                    LinearServoMotorStop();
                    magnetServo.isAtTarget = true;
                }
            }
        break;
    }
}
