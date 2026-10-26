#include <stdint.h>

typedef void (*IntrCallback)(void);
typedef void (*MainCallback)(void);

struct MainInterruptState
{
    MainCallback callback1;
    MainCallback callback2;
    uint8_t unknown_008[4];
    IntrCallback vblankCallback;
    IntrCallback hblankCallback;
    IntrCallback vcountCallback;
    IntrCallback serialCallback;
    uint16_t intrCheck;
};

extern struct MainInterruptState gMain;
extern void m4aSoundVSync(void);
#define INTR_CHECK (*(volatile uint16_t *)0x03007FF8)

enum
{
    INTR_FLAG_HBLANK = 0x0002,
    INTR_FLAG_VCOUNT = 0x0004,
    INTR_FLAG_SERIAL = 0x0080
};

void HBlankIntr(void)
{
    if (gMain.hblankCallback != 0)
        gMain.hblankCallback();
    INTR_CHECK |= INTR_FLAG_HBLANK;
    gMain.intrCheck |= INTR_FLAG_HBLANK;
}

void VCountIntr(void)
{
    if (gMain.vcountCallback != 0)
        gMain.vcountCallback();
    m4aSoundVSync();
    INTR_CHECK |= INTR_FLAG_VCOUNT;
    gMain.intrCheck |= INTR_FLAG_VCOUNT;
}

void SerialIntr(void)
{
    if (gMain.serialCallback != 0)
        gMain.serialCallback();
    INTR_CHECK |= INTR_FLAG_SERIAL;
    gMain.intrCheck |= INTR_FLAG_SERIAL;
}
