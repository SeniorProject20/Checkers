#ifndef TARGETEEPROM_H_
#define TARGETEEPROM_H_

#include "EepromInterface.h"

//Use this file to define items that are stored in the emulated EEPROM
//Each section should have some room to grow for future use.  At the moment, we have allowed 100bytes per section
//In this file we define the overall data stored in the EEPROM - typedef struct{ ...}TargetEEPROM;
//TargetEEPROM defines the memory layout of the data stored in the emulated EEPROM.  It is a collection of other data structures
//which are specific to different items controlled by the target.  These specific data structures may be defined in this header
//or they may be in a separate header file which my be included in this header.  It is recommended to have a signature/version member
//of each individual structure in order to support compatibility as the controller code gets updated in the future.
//To access one of these structures, use the following macro: GET_NV_PARAMS(struct_to_access, where_to_put_the_data_accessed)
//for example: to get the PCR2NvParams use the following:
//#include "TargetEEPROM.h"
//  tPCR2NvParams tempData;
//  memset(&tempData, 0xff, sizeof(tempData));
//  GET_NV_PARAMS(PCR2NvParams, tempData);

//typedef struct {
//    uint32_t signature; //only needs to be a char but due to alignment may as well use all that the compiler would alocate to it
//    uint32_t closedLoopMaxCurrent;
//    uint32_t openLoopCurrent;
//    double Kp;
//    double Ki;
//    double Kd;
//    int sensor_offset;
//    int top_position;
//    int bottom_position;
//}tSquisherNvParams;
//  
// 
// typedef struct {
//    uint32_t signature; //only needs to be a char but due to alignment may as well use all that the compiler would alocate to it
//    double Kp;
//    double Ki;
//    double Kd;
//    char valid;
//}tPCR2NvParams;

#define _NVPARAMS_SPACING_ 60  //amount of room allocated for each individual structure
#define LAST_PAGE_SYSTEM_INFO_SIZE 16
#define LAST_PAGE_SPACING  (_NVPARAMS_SPACING_ - LAST_PAGE_SYSTEM_INFO_SIZE)  //

typedef struct 
{
    int version;
    char targetId;
} SystemInfoNonvolParameters;

 
 typedef struct{
     char pad1[_NVPARAMS_SPACING_]; //note: sizeof(struct) will be padded to a multiple of 4 bytes
     char pad2[_NVPARAMS_SPACING_];
     char pad3[_NVPARAMS_SPACING_]; //note: sizeof(struct) will be padded to a multiple of 4 bytes
     char pad4[_NVPARAMS_SPACING_];
     char pad5[_NVPARAMS_SPACING_]; //note: sizeof(struct) will be padded to a multiple of 4 bytes
     char pad6[_NVPARAMS_SPACING_];
     char pad7[_NVPARAMS_SPACING_]; //note: sizeof(struct) will be padded to a multiple of 4 bytes
     char pad8[_NVPARAMS_SPACING_];
     char pad9[_NVPARAMS_SPACING_]; //note: sizeof(struct) will be padded to a multiple of 4 bytes
     char pad10[_NVPARAMS_SPACING_];
     char pad11[_NVPARAMS_SPACING_]; //note: sizeof(struct) will be padded to a multiple of 4 bytes
     char pad12[LAST_PAGE_SPACING];
     SystemInfoNonvolParameters systemInfoNonvolParameters;
     char padSysInfo[LAST_PAGE_SYSTEM_INFO_SIZE-sizeof(SystemInfoNonvolParameters)];
}TargetEEPROM;

#define GET_NV_PARAMS(struct_to_access, where_to_put_the_data_accessed)   ThreadSafeEepromEmulatorReadBuffer(offsetof(TargetEEPROM,struct_to_access), (uint8_t * const)&where_to_put_the_data_accessed, sizeof(where_to_put_the_data_accessed))
#define SET_NV_PARAMS(struct_to_access, where_to_put_the_data_accessed)   ThreadSafeEepromEmulatorWriteBuffer(offsetof(TargetEEPROM,struct_to_access), (uint8_t * const)&where_to_put_the_data_accessed, sizeof(where_to_put_the_data_accessed)); eeprom_emulator_commit_page_buffer();

#endif