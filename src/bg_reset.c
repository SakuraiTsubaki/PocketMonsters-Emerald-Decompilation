#include <stdint.h>

#define NUM_BACKGROUNDS 4
#define DISPCNT_ALL_BG_AND_MODE_BITS 0x0F07

struct BgConfig
{
    uint8_t visible:1;
    uint8_t unknown_1:1;
    uint8_t screenSize:2;
    uint8_t priority:2;
    uint8_t mosaic:1;
    uint8_t wraparound:1;
    uint8_t charBaseIndex:2;
    uint8_t mapBaseIndex:5;
    uint8_t paletteMode:1;
    uint8_t unknown_2;
    uint8_t unknown_3;
};

struct BgControl
{
    struct BgConfig configs[NUM_BACKGROUNDS];
    uint16_t bgVisibilityAndMode;
};

static struct BgControl sGpuBgConfigs;
static const struct BgConfig sZeroedBgControlStruct = {0};

extern uint16_t GetGpuReg(uint16_t offset);
extern void SetGpuReg(uint16_t offset, uint16_t value);

void ResetBgControlStructs(void)
{
    unsigned int i;
    for (i = 0; i < NUM_BACKGROUNDS; i++)
        sGpuBgConfigs.configs[i] = sZeroedBgControlStruct;
}

void SetTextModeAndHideBgs(void)
{
    SetGpuReg(0, GetGpuReg(0) & ~DISPCNT_ALL_BG_AND_MODE_BITS);
}

void ResetBgs(void)
{
    ResetBgControlStructs();
    sGpuBgConfigs.bgVisibilityAndMode = 0;
    SetTextModeAndHideBgs();
}
