#include <stdint.h>

extern uint16_t GetGpuReg(uint16_t regOffset);
extern void SetGpuReg(uint16_t regOffset, uint16_t value);
extern void EnableInterrupts(uint16_t flags);

enum
{
    REG_OFFSET_DISPSTAT = 0x04,
    DISPSTAT_VCOUNT_INTR = 1 << 5,
    INTR_FLAG_VCOUNT = 1 << 2,
    VCOUNT_COMPARE_LINE = 150
};

void EnableVCountIntrAtLine150(void)
{
    uint16_t gpuReg = (GetGpuReg(REG_OFFSET_DISPSTAT) & 0xFF)
                    | (VCOUNT_COMPARE_LINE << 8);
    SetGpuReg(REG_OFFSET_DISPSTAT, gpuReg | DISPSTAT_VCOUNT_INTR);
    EnableInterrupts(INTR_FLAG_VCOUNT);
}
