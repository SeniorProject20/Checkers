#ifndef NEOPIXEL_H_
#define NEOPIXEL_H_

#include <stdint.h>

void NeoPixelInit(void);
void NeoPixelSetRgb(uint8_t red, uint8_t green, uint8_t blue);
void NeoPixelClearPattern(void);
void NeoPixelAddColorToPattern(uint8_t red, uint8_t green, uint8_t blue);
void NeoPixelClearSequence(void);
void NeoPixelAddCurrentPatternToSequence(uint32_t fadeTime_ms);
void NeoPixelAddSolidColorPatternToSequence(uint8_t red, uint8_t green, uint8_t blue, uint32_t fadeTime_ms);
void NeoPixelStartSequence(uint8_t loopCount, uint8_t loopBackIndex);

#endif