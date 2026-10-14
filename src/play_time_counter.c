#include <stdint.h>

typedef uint8_t u8;
typedef uint16_t u16;

struct SaveBlock2 {
    u8 unknown_000[0x0E];
    u16 playTimeHours;
    u8 playTimeMinutes;
    u8 playTimeSeconds;
    u8 playTimeVBlanks;
};

extern struct SaveBlock2 *gSaveBlock2Ptr;
extern u8 sPlayTimeCounterState;

enum {
    PLAY_TIME_STOPPED,
    PLAY_TIME_RUNNING,
    PLAY_TIME_MAXED_OUT
};

void PlayTimeCounter_Reset(void)
{
    sPlayTimeCounterState = PLAY_TIME_STOPPED;
    gSaveBlock2Ptr->playTimeHours = 0;
    gSaveBlock2Ptr->playTimeMinutes = 0;
    gSaveBlock2Ptr->playTimeSeconds = 0;
    gSaveBlock2Ptr->playTimeVBlanks = 0;
}

void PlayTimeCounter_SetToMax(void);

void PlayTimeCounter_Start(void)
{
    sPlayTimeCounterState = PLAY_TIME_RUNNING;
    if (gSaveBlock2Ptr->playTimeHours > 999)
        PlayTimeCounter_SetToMax();
}

void PlayTimeCounter_Stop(void)
{
    sPlayTimeCounterState = PLAY_TIME_STOPPED;
}

void PlayTimeCounter_Update(void)
{
    if (sPlayTimeCounterState != PLAY_TIME_RUNNING)
        return;

    gSaveBlock2Ptr->playTimeVBlanks++;
    if (gSaveBlock2Ptr->playTimeVBlanks < 60)
        return;

    gSaveBlock2Ptr->playTimeVBlanks = 0;
    gSaveBlock2Ptr->playTimeSeconds++;
    if (gSaveBlock2Ptr->playTimeSeconds < 60)
        return;

    gSaveBlock2Ptr->playTimeSeconds = 0;
    gSaveBlock2Ptr->playTimeMinutes++;
    if (gSaveBlock2Ptr->playTimeMinutes < 60)
        return;

    gSaveBlock2Ptr->playTimeMinutes = 0;
    gSaveBlock2Ptr->playTimeHours++;
    if (gSaveBlock2Ptr->playTimeHours > 999)
        PlayTimeCounter_SetToMax();
}

void PlayTimeCounter_SetToMax(void)
{
    sPlayTimeCounterState = PLAY_TIME_MAXED_OUT;
    gSaveBlock2Ptr->playTimeHours = 999;
    gSaveBlock2Ptr->playTimeMinutes = 59;
    gSaveBlock2Ptr->playTimeSeconds = 59;
    gSaveBlock2Ptr->playTimeVBlanks = 59;
}
