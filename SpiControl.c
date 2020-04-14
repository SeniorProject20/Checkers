#include "SpiControl.h"
#include "ProjectDefines.h"

#include <asf.h>

#define SPI_TRANSCEIVE_TIMEOUT_MS       2
#define DUMMY_BYTE                      0x00
#define SPI_FPGA_TRANSMISSION_LENGTH    3
#define SPI_ADC_TRANSMISSION_LENGTH     2
#define SPI_ADC_CHANNEL_SELECT_SHIFT    3
#define SPI_IO_EXP_TRANSMISSION_LENGTH  3
#define SPI_IO_EXP_ADDRESS              0x20

struct spi_module spi1_master_instance;
struct spi_slave_inst fpgaMotorSlave;
struct spi_slave_inst adcSlave;

SemaphoreHandle_t transceiveCompleteSemaphore;
SemaphoreHandle_t spiBusInUseSemaphore;

bool spiMasterTransferComplete = false;

static bool SpiFpgaMotorReadRegister (struct spi_slave_inst* slave, uint8_t registerAddress, uint16_t *registerValue);
static bool SpiFpgaMotorWriteRegister(struct spi_slave_inst* slave, uint8_t registerAddress, uint16_t registerValue);
static void SpiMasterCallback(struct spi_module *const module);
static void ConfigureSpi1(void);

bool SpiFpgaLinearServoMotorReadRegister (uint8_t registerAddress, uint16_t* registerValue) { return SpiFpgaMotorReadRegister (&fpgaMotorSlave,  registerAddress, registerValue); }
bool SpiFpgaLinearServoMotorWriteRegister(uint8_t registerAddress, uint16_t  registerValue) { return SpiFpgaMotorWriteRegister(&fpgaMotorSlave,  registerAddress, registerValue); }

void ConfigureSpi(void)
{
    ConfigureSpi1();
}

bool SpiAdcReadChannel(uint8_t adcChannel, uint16_t* adcReading)
{
    xSemaphoreTake(spiBusInUseSemaphore, portMAX_DELAY);
    uint8_t tx_buffer[SPI_ADC_TRANSMISSION_LENGTH];
    uint8_t rx_buffer[SPI_ADC_TRANSMISSION_LENGTH];

    tx_buffer[0] = adcChannel << SPI_ADC_CHANNEL_SELECT_SHIFT;
    tx_buffer[1] = DUMMY_BYTE;

    struct spi_slave_inst *slave = &adcSlave;

    spi_select_slave(&spi1_master_instance, slave, true);
    spi_transceive_buffer_job(&spi1_master_instance, tx_buffer, rx_buffer, SPI_ADC_TRANSMISSION_LENGTH);
    bool transceiveWasSuccessful = false;
    if (xSemaphoreTake(transceiveCompleteSemaphore, SPI_TRANSCEIVE_TIMEOUT_MS) == pdFALSE)
    {
        transceiveWasSuccessful = false;
        goto errout;
    }
    else
    {
        transceiveWasSuccessful = true;
    }

    spi_transceive_buffer_job(&spi1_master_instance, tx_buffer, rx_buffer, SPI_ADC_TRANSMISSION_LENGTH);
    if (xSemaphoreTake(transceiveCompleteSemaphore, SPI_TRANSCEIVE_TIMEOUT_MS) == pdFALSE)
    {
        transceiveWasSuccessful = false;
        goto errout;
    }
    else
    {
        transceiveWasSuccessful = true;
    }

    *adcReading = (rx_buffer[0] << 8) | rx_buffer[1];

    errout: //error has occurred, don't leave with chip enable asserted... don't leave still holding the semaphore
    spi_select_slave(&spi1_master_instance, slave, false);
    xSemaphoreGive(spiBusInUseSemaphore);
    return transceiveWasSuccessful;
}

static bool SpiFpgaMotorReadRegister(struct spi_slave_inst* slave, uint8_t registerAddress, uint16_t *registerValue)
{
    xSemaphoreTake(spiBusInUseSemaphore, portMAX_DELAY);
    uint8_t tx_buffer[SPI_FPGA_TRANSMISSION_LENGTH];
    uint8_t rx_buffer[SPI_FPGA_TRANSMISSION_LENGTH];

    tx_buffer[0] = registerAddress << 1;
    tx_buffer[1] = DUMMY_BYTE;
    tx_buffer[2] = DUMMY_BYTE;

    spi_select_slave(&spi1_master_instance, slave, true);
    spi_transceive_buffer_job(&spi1_master_instance, tx_buffer, rx_buffer, SPI_FPGA_TRANSMISSION_LENGTH);
    bool transceiveWasSuccessful = false;
    if (xSemaphoreTake(transceiveCompleteSemaphore, SPI_TRANSCEIVE_TIMEOUT_MS) == pdFALSE)
    {
        transceiveWasSuccessful = false;
    }
    else
    {
        transceiveWasSuccessful = true;
    }
    spi_select_slave(&spi1_master_instance, slave, false);
    xSemaphoreGive(spiBusInUseSemaphore);
    if(transceiveWasSuccessful)
    {
        *registerValue = (rx_buffer[1] << 8) | rx_buffer[2];
    }

    return transceiveWasSuccessful;
}

static bool SpiFpgaMotorWriteRegister(struct spi_slave_inst* slave, uint8_t registerAddress, uint16_t registerValue)
{
    xSemaphoreTake(spiBusInUseSemaphore, portMAX_DELAY);
    uint8_t tx_buffer[SPI_FPGA_TRANSMISSION_LENGTH];
    uint8_t rx_buffer[SPI_FPGA_TRANSMISSION_LENGTH];

    tx_buffer[0] = registerAddress << 1 | 0x01;
    tx_buffer[1] = registerValue >> 8;
    tx_buffer[2] = registerValue & 0xFF;

    spi_select_slave(&spi1_master_instance, slave, true);
    spi_transceive_buffer_job(&spi1_master_instance, tx_buffer, rx_buffer, SPI_FPGA_TRANSMISSION_LENGTH);
    bool transceiveWasSuccessful = false;
    if (xSemaphoreTake(transceiveCompleteSemaphore, SPI_TRANSCEIVE_TIMEOUT_MS) == pdFALSE)
    {
        transceiveWasSuccessful = false;
    }
    else
    {
        transceiveWasSuccessful = true;
    }
    spi_select_slave(&spi1_master_instance, slave, false);
    xSemaphoreGive(spiBusInUseSemaphore);
    return transceiveWasSuccessful;
}


static void ConfigureSpi1(void)
{
    struct port_config pin_conf;
    port_get_config_defaults(&pin_conf);
    pin_conf.direction  = PORT_PIN_DIR_OUTPUT;

    struct spi_config config_spi_master;
    struct spi_slave_inst_config slave_dev_config;

    spi_slave_inst_get_config_defaults(&slave_dev_config);

    slave_dev_config.ss_pin = SPI1_ADC_nCS;
    spi_attach_slave(&adcSlave, &slave_dev_config);

    slave_dev_config.ss_pin = SPI1_FPGA_nCS;
    spi_attach_slave(&fpgaMotorSlave, &slave_dev_config);

    spi_get_config_defaults(&config_spi_master);
    config_spi_master.mode_specific.master.baudrate = 4000000;
    config_spi_master.mux_setting = SPI1_MUX_SETTING;
    config_spi_master.pinmux_pad0 = SPI1_SERCOM_PAD0;
    config_spi_master.pinmux_pad1 = SPI1_SERCOM_PAD1;
    config_spi_master.pinmux_pad2 = SPI1_SERCOM_PAD2;
    config_spi_master.pinmux_pad3 = SPI1_SERCOM_PAD3;
    spi_init(&spi1_master_instance, SPI1_SERCOM, &config_spi_master);
    spi_enable(&spi1_master_instance);

    spi_select_slave(&spi1_master_instance, &fpgaMotorSlave, false);
    spi_select_slave(&spi1_master_instance, &adcSlave, false);

    spi_register_callback(&spi1_master_instance, SpiMasterCallback, SPI_CALLBACK_BUFFER_TRANSCEIVED);
    spi_enable_callback(&spi1_master_instance, SPI_CALLBACK_BUFFER_TRANSCEIVED);

    system_pinmux_pin_set_output_strength(SPI1_MOSI, SYSTEM_PINMUX_PIN_STRENGTH_HIGH);
    system_pinmux_pin_set_output_strength(SPI1_MISO, SYSTEM_PINMUX_PIN_STRENGTH_HIGH);
    system_pinmux_pin_set_output_strength(SPI1_SCK, SYSTEM_PINMUX_PIN_STRENGTH_HIGH);

    transceiveCompleteSemaphore = xSemaphoreCreateBinary();
    xSemaphoreTake(transceiveCompleteSemaphore, 0);
    spiBusInUseSemaphore = xSemaphoreCreateBinary();
    xSemaphoreGive(spiBusInUseSemaphore);
}

static void SpiMasterCallback(struct spi_module *const module)
{
    portBASE_TYPE  higherPriorityTaskWoken = pdFALSE;
    xSemaphoreGiveFromISR(transceiveCompleteSemaphore, &higherPriorityTaskWoken);
    portEND_SWITCHING_ISR(higherPriorityTaskWoken);
}
