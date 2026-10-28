#include <stdint.h>

typedef int32_t bool32;

extern bool32 gFlashMemoryPresent;
extern int IdentifyFlash(void);
extern void InitFlashTimer(void);

void CheckForFlashMemory(void)
{
    if (IdentifyFlash() == 0)
    {
        gFlashMemoryPresent = 1;
        InitFlashTimer();
    }
    else
    {
        gFlashMemoryPresent = 0;
    }
}

