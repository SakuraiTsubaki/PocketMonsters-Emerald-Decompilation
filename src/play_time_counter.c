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
extern void PlayTimeCounter_SetToMax(void);

enum {
    PLAY_TIME_STOPPED,
    PLAY_TIME_RUNNING,
    PLAY_TIME_MAXED_OUT
};

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

