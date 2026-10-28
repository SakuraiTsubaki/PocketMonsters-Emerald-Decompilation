#include <stdint.h>

typedef void (*IntrFunc)(void);

extern IntrFunc gIntrTable[];
extern void SetFlashTimerIntr(uint8_t timer, IntrFunc *handlerSlot);

void InitFlashTimer(void)
{
    SetFlashTimerIntr(2, gIntrTable + 7);
}

