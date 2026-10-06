#include <stdint.h>

#define REG_IME (*(volatile uint16_t *)0x04000208)
#define REG_DMA_CNT_H(channel) (*(volatile uint16_t *)(0x040000BA + (channel) * 12))

extern void m4aSoundVSyncOff(void);
extern void ScanlineEffect_Stop(void);
extern void SiiRtcProtect(void);
extern void SoftReset(uint32_t resetFlags);

static inline void DmaStop(uint8_t channel)
{
    REG_DMA_CNT_H(channel) = 0;
}

enum
{
    RESET_ALL = 0xFF,
    RESET_SIO_REGS = 0x20
};

/* BPEJ-rev0: 0x080008F4..0x08000950. */
void DoSoftReset(void)
{
    REG_IME = 0;
    m4aSoundVSyncOff();
    ScanlineEffect_Stop();
    DmaStop(1);
    DmaStop(2);
    DmaStop(3);
    SiiRtcProtect();
    SoftReset(RESET_ALL);
}

