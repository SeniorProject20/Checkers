#ifndef STARTBUTTON_H_
#define STARTBUTTON_H_

#include <stdbool.h>

void StartButtonInit(void);
void StartButtonLEDInit(void);
bool StartButtonPress(void);
void StartButtonLED(bool enable);




#endif /* STARTBUTTON_H_ */
