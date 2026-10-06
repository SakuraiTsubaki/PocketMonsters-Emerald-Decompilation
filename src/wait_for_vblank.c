#include <stdint.h>

struct MainVBlankState
{
    uint8_t unknown_000[0x1C];
    volatile uint16_t intrCheck;
};

extern struct MainVBlankState gMain;

enum { INTR_FLAG_VBLANK = 1 };

/* BPEJ-rev0: 0x080008AC..0x080008d4. */
void WaitForVBlank(void)
{
    gMain.intrCheck &= (uint16_t)~INTR_FLAG_VBLANK;
    while (!(gMain.intrCheck & INTR_FLAG_VBLANK))
    {
    }
}

