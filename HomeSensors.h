#ifndef HOMESENSORS_H_
#define HOMESENSORS_H_

#include <stdbool.h>

void HomeSensorsInit(void);
bool XHomeRead(void);
bool YHomeRead(void);

#endif /* HOMESENSORS_H_ */