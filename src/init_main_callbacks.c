#include <stddef.h>
#include <stdint.h>

typedef void (*MainCallback)(void);

struct MainInitState
{
    MainCallback callback1;
    MainCallback callback2;
    uint8_t unknown_008[0x18];
    void *vblankCounter1;
    void *vblankCounter2;
};

extern struct MainInitState gMain;
extern void *gTrainerHillVBlankCounter;
extern void *gSaveBlock2Ptr;
extern void *gPokemonStoragePtr;
extern uint8_t gSaveblock2[];
extern uint8_t gPokemonStorage[];
extern void CB2_InitCopyrightScreenAfterBootup(void);
extern void SetMainCallback2(MainCallback callback);

void InitMainCallbacks(void)
{
    gMain.vblankCounter1 = NULL;
    gTrainerHillVBlankCounter = NULL;
    gMain.vblankCounter2 = NULL;
    gMain.callback1 = NULL;
    SetMainCallback2(CB2_InitCopyrightScreenAfterBootup);
    gSaveBlock2Ptr = gSaveblock2;
    gPokemonStoragePtr = gPokemonStorage;
}
