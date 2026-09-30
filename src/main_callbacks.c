#include <stddef.h>
#include <stdint.h>

typedef uint8_t bool8;
typedef void (*MainCallback)(void);

/* Only fields proven by the BPEJ rev0 access pattern are named here. */
struct MainCallbackState
{
    MainCallback callback1;       /* +0x000 */
    MainCallback callback2;       /* +0x004 on the 32-bit target */
    uint8_t unknown_008[0x430];
    uint8_t state;                /* +0x438 */
};

extern struct MainCallbackState gMain;
extern bool8 HandleLinkConnection(void);
void CallCallbacks(void);

/* BPEJ rev0: 0x080004c4..0x080004d7 */
void UpdateLinkAndCallCallbacks(void)
{
    if (!HandleLinkConnection())
        CallCallbacks();
}

/* BPEJ rev0: 0x0800051c..0x08000539 */
void CallCallbacks(void)
{
    if (gMain.callback1 != NULL)
        gMain.callback1();
    if (gMain.callback2 != NULL)
        gMain.callback2();
}

/* BPEJ rev0: 0x08000540..0x0800054f */
void SetMainCallback2(MainCallback callback)
{
    gMain.callback2 = callback;
    gMain.state = 0;
}
