#ifndef PROJECTDEFINES_H_
#define PROJECTDEFINES_H_

#include "CommonDefines.h"

#define DEFAULT_TARGET_ID "A"
#define TARGET_VERSION_STRING "0.0.0"
#define xstr(s) str(s)
#define str(s) #s
#define BUILD_INFO " " xstr(COMPUTER_NAME) " \"" __DATE__ " " __TIME__ "\""
#define FW_VER_STRING TARGET_VERSION_STRING COMMON_VERSION_STRING BUILD_INFO
#define REVISION_VALUE "1"
#define RTU_NAME "Template"
//#define ASSERT_CLK_GPIO   PIN_PB00 //-- for xplained board replace with pin for fru
//#define ASSERT_DATA_GPIO  PIN_PB06 //-- for xplained board replace with pin for fru
//#define GP_LED_PIN        PIN_PB30 //-- for xplained board replace with pin for fru

///// HEART BEAT //////
#define HB_LED_PIN -1
///////////////////////

#define LINEAR_SERVO_TASK_STACK    300
#define LINEAR_SERVO_TASK_PRIORITY 2

//////////////////////////////////////////
#define SPI1_MISO       PIN_PA04
#define SPI1_MOSI       PIN_PA06
#define SPI1_SCK        PIN_PA07
#define SPI1_FPGA_nCS   PIN_PA05
#define SPI1_ADC_nCS    PIN_PB11

/////////////////////////////////////////
// COMMON INTERFACES
////////////////////////////////////////

///// SPI //////
#define SPI1_SERCOM       SERCOM0
#define SPI1_SERCOM_PAD0  PINMUX_PA04D_SERCOM0_PAD0
#define SPI1_SERCOM_PAD1  PINMUX_UNUSED
#define SPI1_SERCOM_PAD2  PINMUX_PA06D_SERCOM0_PAD2
#define SPI1_SERCOM_PAD3  PINMUX_PA07D_SERCOM0_PAD3
#define SPI1_MUX_SETTING  SPI_SIGNAL_MUX_SETTING_E
///////////////


#endif
