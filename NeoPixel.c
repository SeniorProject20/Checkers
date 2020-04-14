#include "NeoPixel.h"

#include <asf.h>

#define PIXEL_LATCH_TIME_ms 0.8

#define LED_STRIP_PIXEL_COUNT 10

#define MAX_STEPS         20
#define LED_SERVO_TIME_MS 20

typedef struct {
	uint8_t red;
	uint8_t green;
	uint8_t blue;
} Color;

typedef struct {
	Color colors[LED_STRIP_PIXEL_COUNT];
} Pattern;

typedef struct {
	Pattern  pattern;
	uint32_t fadeTime_ms;
} Step;

typedef struct {
	Step    steps[MAX_STEPS];
	uint8_t stepCount;
	uint8_t loopCount;
	uint8_t loopBackIndex;
} Sequence;

typedef struct {
	Pattern  currentPattern;
	uint8_t  loopCounter;
	uint8_t  previousStepIndex;
	uint8_t  currentStepIndex;
	uint32_t increments;
	uint32_t incrementor;
	float    redIncrements[LED_STRIP_PIXEL_COUNT];
	float    greenIncrements[LED_STRIP_PIXEL_COUNT];
	float    blueIncrements[LED_STRIP_PIXEL_COUNT];
} FadeData;

typedef struct {
	Pattern  stagePattern;
	uint8_t  stagePatternIndex;
	Sequence stageSequence;
	Sequence currentSequence;
	uint8_t  stageStepIndex;
	bool     reset;
	FadeData fadeData;
} NeoPixelData;

NeoPixelData neoPixelData;

SemaphoreHandle_t transferCompleteSemaphore;
struct spi_module led_spi_instance;

uint8_t pixel_data_sercom_format[LED_STRIP_PIXEL_COUNT*3*4]; //3 colors per device, 4 bytes per color due to encoding

static void NeoPixelTask      (void* p);
static void HandleFade        (void);
static void PrepareForNewStep (void);
static void UpdatePixels      (Pattern pattern);

static void set_up_dma_led_transfer(uint8_t *led_color_data_sercom_format, int numbytes);
static void do_dma_led_transfer(void);

void NeoPixelInit(void) {
	memset(&neoPixelData, 0, sizeof(neoPixelData));
	NeoPixelSetRgb(0,0,0);
	xTaskCreate(NeoPixelTask, "NeoPixel Task", 500, NULL, 2, NULL);

	//spi used to clock out the bits to the leds
	struct spi_config config_spi_master;

	spi_get_config_defaults(&config_spi_master);
	config_spi_master.receiver_enable  = false;
	config_spi_master.select_slave_low_detect_enable= false;
	config_spi_master.mux_setting = SPI_SIGNAL_MUX_SETTING_B;  //sets dopo dipo... A=0,0  B=0,1  C=0,2  D=0,3  E=1,0  F=1,1  ...  O=3,2  P=3,3
	config_spi_master.pinmux_pad0 = PINMUX_PA00D_SERCOM1_PAD0;
	config_spi_master.pinmux_pad1 = PINMUX_UNUSED;
	config_spi_master.pinmux_pad2 = PINMUX_UNUSED;
	config_spi_master.pinmux_pad3 = PINMUX_UNUSED;

	config_spi_master.mode_specific.master.baudrate = 3333333;
	spi_init(&led_spi_instance, SERCOM1, &config_spi_master);
	spi_enable(&led_spi_instance);

	transferCompleteSemaphore = xSemaphoreCreateBinary();
	xSemaphoreTake(transferCompleteSemaphore, 0);
}

void NeoPixelSetRgb(uint8_t red, uint8_t green, uint8_t blue) {
	NeoPixelClearSequence();
	NeoPixelAddSolidColorPatternToSequence(red, green, blue, LED_SERVO_TIME_MS);
	NeoPixelStartSequence(0, 0);
}

void NeoPixelClearPattern(void) {
	memset(&neoPixelData.stagePattern, 0, sizeof(neoPixelData.stagePattern));
	neoPixelData.stagePatternIndex = 0;
}

void NeoPixelAddColorToPattern(uint8_t red, uint8_t green, uint8_t blue) {
	if(neoPixelData.stagePatternIndex >= LED_STRIP_PIXEL_COUNT) {
		return;
	}
	Color* color = &neoPixelData.stagePattern.colors[neoPixelData.stagePatternIndex];
	color->red   = red;
	color->green = green;
	color->blue  = blue;
	neoPixelData.stagePatternIndex++;
}

void NeoPixelClearSequence(void) {
	memset(&neoPixelData.stageSequence, 0, sizeof(neoPixelData.stageSequence));
	neoPixelData.stageStepIndex = 0;
}

void NeoPixelAddCurrentPatternToSequence(uint32_t fadeTime_ms) {
	Step* step = &neoPixelData.stageSequence.steps[neoPixelData.stageStepIndex];
	neoPixelData.stageSequence.stepCount++;

	for(int i = 0; i < LED_STRIP_PIXEL_COUNT; i++) {
		step->pattern.colors[i].red   = neoPixelData.stagePattern.colors[i].red;
		step->pattern.colors[i].green = neoPixelData.stagePattern.colors[i].green;
		step->pattern.colors[i].blue  = neoPixelData.stagePattern.colors[i].blue;
	}

	step->fadeTime_ms = fadeTime_ms;
	neoPixelData.stageStepIndex++;
}

void NeoPixelAddSolidColorPatternToSequence(uint8_t red, uint8_t green, uint8_t blue, uint32_t fadeTime_ms) {
	Step* step = &neoPixelData.stageSequence.steps[neoPixelData.stageStepIndex];
	neoPixelData.stageSequence.stepCount++;

	for(int i = 0; i < LED_STRIP_PIXEL_COUNT; i++) {
		step->pattern.colors[i].red   = red;
		step->pattern.colors[i].green = green;
		step->pattern.colors[i].blue  = blue;
	}
	step->fadeTime_ms = fadeTime_ms;
	neoPixelData.stageStepIndex++;
}

void NeoPixelStartSequence(uint8_t loopCount, uint8_t loopBackIndex) {
	memset(&neoPixelData.fadeData, 0, sizeof(neoPixelData.fadeData));
	neoPixelData.stageSequence.loopBackIndex = loopBackIndex;
	neoPixelData.stageSequence.loopCount = loopCount;
	neoPixelData.currentSequence = neoPixelData.stageSequence;
	neoPixelData.reset = true;
}

void HandleFade(void) {
	if(neoPixelData.fadeData.incrementor == neoPixelData.fadeData.increments) {
		PrepareForNewStep();
	}

	Step* previousStep = &neoPixelData.currentSequence.steps[neoPixelData.fadeData.previousStepIndex];

	for(int i = 0; i < LED_STRIP_PIXEL_COUNT; i++) {
		neoPixelData.fadeData.currentPattern.colors[i].red   = previousStep->pattern.colors[i].red   + (neoPixelData.fadeData.redIncrements[i]   * neoPixelData.fadeData.incrementor);
		neoPixelData.fadeData.currentPattern.colors[i].green = previousStep->pattern.colors[i].green + (neoPixelData.fadeData.greenIncrements[i] * neoPixelData.fadeData.incrementor);
		neoPixelData.fadeData.currentPattern.colors[i].blue  = previousStep->pattern.colors[i].blue  + (neoPixelData.fadeData.blueIncrements[i]  * neoPixelData.fadeData.incrementor);
	}

	neoPixelData.fadeData.incrementor++;

	UpdatePixels(neoPixelData.fadeData.currentPattern);
}

static void PrepareForNewStep(void) {
	neoPixelData.fadeData.previousStepIndex = neoPixelData.fadeData.currentStepIndex;
	Step* previousStep = &neoPixelData.currentSequence.steps[neoPixelData.fadeData.previousStepIndex];

	neoPixelData.fadeData.currentStepIndex++;
	if(neoPixelData.fadeData.currentStepIndex >= neoPixelData.currentSequence.stepCount) {

		neoPixelData.fadeData.currentStepIndex = neoPixelData.currentSequence.loopBackIndex;

		if(neoPixelData.currentSequence.loopCount > 0) {
			neoPixelData.fadeData.loopCounter++;
			if(neoPixelData.fadeData.loopCounter >= neoPixelData.currentSequence.loopCount) {
				Step* currentStep = &neoPixelData.currentSequence.steps[neoPixelData.fadeData.previousStepIndex];
				UpdatePixels(currentStep->pattern);
			}
		}
	}

	Step* currentStep = &neoPixelData.currentSequence.steps[neoPixelData.fadeData.currentStepIndex];

	neoPixelData.fadeData.incrementor    = 0;
	neoPixelData.fadeData.increments     = currentStep->fadeTime_ms / LED_SERVO_TIME_MS;
	for(int i = 0; i < LED_STRIP_PIXEL_COUNT; i++) {
		neoPixelData.fadeData.redIncrements[i]   = ((float)currentStep->pattern.colors[i].red   - (float)previousStep->pattern.colors[i].red)   / (float)neoPixelData.fadeData.increments;
		neoPixelData.fadeData.greenIncrements[i] = ((float)currentStep->pattern.colors[i].green - (float)previousStep->pattern.colors[i].green) / (float)neoPixelData.fadeData.increments;
		neoPixelData.fadeData.blueIncrements[i]  = ((float)currentStep->pattern.colors[i].blue  - (float)previousStep->pattern.colors[i].blue)  / (float)neoPixelData.fadeData.increments;
	}
}

static void NeoPixelTask(void* p) {
	set_up_dma_led_transfer(pixel_data_sercom_format, sizeof(pixel_data_sercom_format));

	while(1) {
		TickType_t lastUpdate;
		neoPixelData.reset = false;
		memset(&neoPixelData.fadeData, 0, sizeof(neoPixelData.fadeData));
		neoPixelData.fadeData.currentPattern = neoPixelData.currentSequence.steps[0].pattern;

		do {
			lastUpdate = xTaskGetTickCount();

			HandleFade();

			vTaskDelayUntil(&lastUpdate, LED_SERVO_TIME_MS * portTICK_PERIOD_MS);
		} while (!neoPixelData.reset);
	}
}


static uint8_t EncodeColorNibble(uint8_t color_byte, int nibbleIndex)
{
	uint8_t value = 0x88;
	if( color_byte & 1 << (nibbleIndex * 2 + 1)) { value |= 0x40; }
	if( color_byte & 1 << (nibbleIndex * 2 + 0)) { value |= 0x04; }
	return ~value;
}

static void UpdatePixels(Pattern pattern)
{
	//taskENTER_CRITICAL();
	uint8_t *p = (uint8_t *)pixel_data_sercom_format;

	for(int j = 0; j < LED_STRIP_PIXEL_COUNT; j++)
	{
		for(int i = 3; i >= 0; i--)
		{
			*p++ = EncodeColorNibble(pattern.colors[j].green, i);
		}
		for(int i = 3; i >= 0; i--)
		{
			*p++ = EncodeColorNibble(pattern.colors[j].red, i);
		}
		for(int i = 3; i >= 0; i--)
		{
			*p++ = EncodeColorNibble(pattern.colors[j].blue, i);
		}
	} // ~200us
	do_dma_led_transfer();

	//vTaskDelay(PIXEL_LATCH_TIME_ms * portTICK_PERIOD_MS);
	vTaskDelay(1 * portTICK_PERIOD_MS); //need at least 80uS according to the data sheet... 2mS is at least that long

	//taskEXIT_CRITICAL();
}

//##################################################################################################################
//##################################################################################################################
//#########
//#########  Use DMA to send all the bytes to the LEDs thru the serial interface (sercom0)
//#########
//##################################################################################################################
//##################################################################################################################
#include "component/dmac.h"
#include "dma.h"

static volatile bool led_transfer_is_done = false;
COMPILER_ALIGNED(16)
static DmacDescriptor led_dma_descriptors[2]; SECTION_DMAC_DESCRIPTOR;   //only one descriptor required
static struct dma_resource led_dma_resource;

#define DMA_TRANSFER_TIMEOUT_ms 1000


static void transfer_done(struct dma_resource* const resource )
{
	portBASE_TYPE  higherPriorityTaskWoken = pdFALSE;
	xSemaphoreGiveFromISR(transferCompleteSemaphore, &higherPriorityTaskWoken);
	portEND_SWITCHING_ISR(higherPriorityTaskWoken);
}

static void configure_dma_resource(struct dma_resource *resource)
{
	struct dma_resource_config config;
	dma_get_config_defaults(&config);
	config.event_config.event_output_enable=false;
	config.event_config.input_action = DMA_EVENT_INPUT_NOACT;
	config.peripheral_trigger = SERCOM1_DMAC_ID_TX; //see manual, page 322 (table 19-8)
	config.trigger_action = DMA_TRIGGER_ACTION_BEAT;
	dma_allocate(resource, &config);
}

static void setup_transfer_descriptor1(DmacDescriptor *descriptor, DmacDescriptor* nextDescriptor, uint8_t *source_memory, int numbytes )
{
	struct dma_descriptor_config descriptor_config;
	dma_descriptor_get_config_defaults(&descriptor_config);
	descriptor_config.dst_increment_enable = false;
	descriptor_config.block_transfer_count = numbytes;//sizeof(source_memory);
	descriptor_config.source_address = (uint32_t)source_memory + numbytes;//sizeof(source_memory);
	descriptor_config.destination_address = (uint32_t)&SERCOM1->SPI.DATA.reg;
	//descriptor_config.next_descriptor_address = (uint32_t)nextDescriptor;
	dma_descriptor_create(descriptor, &descriptor_config);
}

//static void setup_transfer_descriptor2(DmacDescriptor *descriptor, uint8_t *source_memory, int numbytes )
//{
//struct dma_descriptor_config descriptor_config;
//dma_descriptor_get_config_defaults(&descriptor_config);
//descriptor_config.dst_increment_enable = false;
//descriptor_config.src_increment_enable = false;
//descriptor_config.block_transfer_count = numbytes;//sizeof(source_memory);
//descriptor_config.source_address = (uint32_t)source_memory;//sizeof(source_memory);
//descriptor_config.destination_address = (uint32_t)&SERCOM0->SPI.DATA.reg;
//dma_descriptor_create(descriptor, &descriptor_config);
//}

static void set_up_dma_led_transfer(uint8_t *led_color_data_sercom_format, int numbytes)
{
	//uint8_t bufferByte = 0xFF;
	configure_dma_resource(&led_dma_resource);
	setup_transfer_descriptor1(&led_dma_descriptors[0], &led_dma_descriptors[1], led_color_data_sercom_format, numbytes);
	//setup_transfer_descriptor2(&led_dma_descriptors[1], &bufferByte, 34);
	dma_add_descriptor(&led_dma_resource, &led_dma_descriptors[0]);
	//dma_add_descriptor(&led_dma_resource, &led_dma_descriptors[1]);
	dma_register_callback(&led_dma_resource, transfer_done,   DMA_CALLBACK_TRANSFER_DONE);
	dma_enable_callback(&led_dma_resource, DMA_CALLBACK_TRANSFER_DONE);
}

static void do_dma_led_transfer(void)
{
	dma_start_transfer_job(&led_dma_resource);
	//dma_trigger_transfer(&led_dma_resource);
	xSemaphoreTake(transferCompleteSemaphore, DMA_TRANSFER_TIMEOUT_ms * portTICK_PERIOD_MS);
}