#ifndef SPICONTROL_H_
#define SPICONTROL_H_

#include "StatusCodes.h"

#include <stdbool.h>
#include <stdint.h>

#define SPI_FPGA_FMW_VER_REG_ADDR 0x00
#define SPI_FPGA_RESET_REG_ADDR   0x7F
#define SPI_FPGA_MOT1_REG_ADDR    0x01
#define SPI_FPGA_MOT2_REG_ADDR    0x02
#define SPI_FPGA_MOT3_REG_ADDR    0x03
#define SPI_FPGA_MOT4_REG_ADDR    0x04
#define SPI_FPGA_MOT5_REG_ADDR    0x05
#define SPI_FPGA_MOT6_REG_ADDR    0x06
#define SPI_FPGA_MOT7_REG_ADDR    0x07
#define SPI_FPGA_MOT8_REG_ADDR    0x08
#define SPI_FPGA_MOT9_REG_ADDR    0x09
#define SPI_FPGA_MOT10_REG_ADDR   0x0A
#define SPI_FPGA_MOT11_REG_ADDR   0x0B
#define SPI_FPGA_MOT12_REG_ADDR   0x0C
#define SPI_FPGA_MOT13_REG_ADDR   0x0D

#define SPI_ADC_LINEAR_SERVO_POT_ANA_FB1_CHANNEL 0x00
#define SPI_ADC_LINEAR_SERVO_POT_ANA_FB2_CHANNEL 0x01
#define SPI_ADC_LINEAR_SERVO_POT_ANA_FB3_CHANNEL 0x02
#define SPI_ADC_LINEAR_SERVO_POT_ANA_FB4_CHANNEL 0x03
#define SPI_ADC_LINEAR_SERVO_POT_ANA_FB5_CHANNEL 0x04
#define SPI_ADC_LINEAR_SERVO_POT_ANA_FB6_CHANNEL 0x05
#define SPI_ADC_LINEAR_SERVO_POT_ANA_FB7_CHANNEL 0x06

void ConfigureSpi                        (void);
bool SpiAdcReadChannel                   (uint8_t adcChannel,      uint16_t* adcReading   );
bool SpiFpgaLinearServoMotorReadRegister (uint8_t registerAddress, uint16_t* registerValue);
bool SpiFpgaLinearServoMotorWriteRegister(uint8_t registerAddress, uint16_t  registerValue);
//bool SpiFpgaMuscleWireReadRegister       (uint8_t registerAddress, uint16_t* registerValue);
//bool SpiFpgaMuscleWireWriteRegister      (uint8_t registerAddress, uint16_t  registerValue);
//bool SpiMwObsIoExpReadRegister           (uint8_t registerAddress, uint8_t*  registerValue);
//bool SpiMwObsIoExpWriteRegister          (uint8_t registerAddress, uint8_t   registerValue);
#endif