#include <stdint.h>

typedef uint8_t bool8;
typedef void (*MainCallback)(void);

struct MainInputState {
    MainCallback callback1;
    MainCallback callback2;
    uint8_t unknown_008[0x20];
    uint16_t heldKeysRaw;
    uint16_t newKeysRaw;
    uint16_t heldKeys;
    uint16_t newKeys;
    uint16_t newAndRepeatedKeys;
    uint16_t keyRepeatCounter;
    bool8 watchedKeysPressed;
    uint8_t unknown_035;
    uint16_t watchedKeysMask;
};

struct SaveBlock2InputOptions {
    uint8_t unknown_000[0x13];
    uint8_t optionsButtonMode;
};

extern struct MainInputState gMain;
extern struct SaveBlock2InputOptions *gSaveBlock2Ptr;
extern uint16_t gKeyRepeatContinueDelay;
extern uint16_t gKeyRepeatStartDelay;

#define REG_KEYINPUT (*(volatile uint16_t *)0x04000130)

enum {
    A_BUTTON = 1,
    L_BUTTON = 1 << 9,
    KEYS_MASK = 0x03FF,
    OPTIONS_BUTTON_MODE_L_EQUALS_A = 2
};

/* BPEJ rev0: 0x080005bc..0x080005d7. */
void InitKeys(void)
{
    gKeyRepeatContinueDelay = 5;
    gKeyRepeatStartDelay = 40;
    gMain.heldKeys = 0;
    gMain.newKeys = 0;
    gMain.newAndRepeatedKeys = 0;
    gMain.heldKeysRaw = 0;
    gMain.newKeysRaw = 0;
}

/* BPEJ rev0: 0x080005e4..0x08000679. */
void ReadKeys(void)
{
    uint16_t keyInput = REG_KEYINPUT ^ KEYS_MASK;
    gMain.newKeysRaw = keyInput & ~gMain.heldKeysRaw;
    gMain.newKeys = gMain.newKeysRaw;
    gMain.newAndRepeatedKeys = gMain.newKeysRaw;

    if (keyInput != 0 && gMain.heldKeys == keyInput) {
        gMain.keyRepeatCounter--;
        if (gMain.keyRepeatCounter == 0) {
            gMain.newAndRepeatedKeys = keyInput;
            gMain.keyRepeatCounter = gKeyRepeatContinueDelay;
        }
    } else {
        gMain.keyRepeatCounter = gKeyRepeatStartDelay;
    }

    gMain.heldKeysRaw = keyInput;
    gMain.heldKeys = gMain.heldKeysRaw;

    if (gSaveBlock2Ptr->optionsButtonMode == OPTIONS_BUTTON_MODE_L_EQUALS_A) {
        if (gMain.newKeys & L_BUTTON)
            gMain.newKeys |= A_BUTTON;
        if (gMain.heldKeys & L_BUTTON)
            gMain.heldKeys |= A_BUTTON;
    }

    if (gMain.newKeys & gMain.watchedKeysMask)
        gMain.watchedKeysPressed = 1;
}

