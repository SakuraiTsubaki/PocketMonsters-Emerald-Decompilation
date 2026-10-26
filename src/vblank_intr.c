#include <stdint.h>

typedef uint8_t bool8;
typedef void (*IntrCallback)(void);
typedef void (*MainCallback)(void);

struct MainVBlankState
{
    MainCallback callback1;
    MainCallback callback2;
    uint8_t unknown_008[4];
    IntrCallback vblankCallback;
    IntrCallback hblankCallback;
    IntrCallback vcountCallback;
    IntrCallback serialCallback;
    uint16_t intrCheck;
    uint16_t unknown_01e;
    uint32_t vblankCounter1;
    uint32_t vblankCounter2;
    uint8_t unknown_028[0x411];
    bool8 inBattle;
};

struct SoundInfoVBlank
{
    uint8_t unknown_000[4];
    uint8_t pcmDmaCounter;
};

extern struct MainVBlankState gMain;
extern uint8_t gWirelessCommType;
extern uint8_t gLinkVSyncDisabled;
extern uint8_t gPcmDmaCounter;
extern struct SoundInfoVBlank gSoundInfo;
extern uint32_t *gTrainerHillVBlankCounter;
extern uint32_t gBattleTypeFlags;
extern void RfuVSync(void);
extern void LinkVSync(void);
extern void CopyBufferedValuesToGpuRegs(void);
extern void ProcessDma3Requests(void);
extern void m4aSoundMain(void);
extern void TryReceiveLinkBattleData(void);
extern void UpdateWirelessStatusIndicatorSprite(void);
extern uint16_t Random(void);

#define INTR_CHECK (*(volatile uint16_t *)0x03007FF8)
#define INTR_FLAG_VBLANK 1
#define BATTLE_RNG_SUPPRESS_MASK 0x013F0102u

void VBlankIntr(void)
{
    if (gWirelessCommType != 0)
        RfuVSync();
    else if (!gLinkVSyncDisabled)
        LinkVSync();
    gMain.vblankCounter1++;
    if (gTrainerHillVBlankCounter != 0 && *gTrainerHillVBlankCounter < 0xFFFFFFFFu)
        (*gTrainerHillVBlankCounter)++;
    if (gMain.vblankCallback != 0)
        gMain.vblankCallback();
    gMain.vblankCounter2++;
    CopyBufferedValuesToGpuRegs();
    ProcessDma3Requests();
    gPcmDmaCounter = gSoundInfo.pcmDmaCounter;
    m4aSoundMain();
    TryReceiveLinkBattleData();
    if (!gMain.inBattle || !(gBattleTypeFlags & BATTLE_RNG_SUPPRESS_MASK))
        Random();
    UpdateWirelessStatusIndicatorSprite();
    INTR_CHECK |= INTR_FLAG_VBLANK;
    gMain.intrCheck |= INTR_FLAG_VBLANK;
}
