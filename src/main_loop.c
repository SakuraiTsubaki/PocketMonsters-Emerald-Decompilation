#include <stdint.h>
typedef uint8_t bool8; typedef void (*MainCallback)(void);
struct MainLoopState { MainCallback callback1,callback2; uint8_t unknown_008[0x20]; uint16_t heldKeysRaw,newKeysRaw,heldKeys,newKeys; };
extern struct MainLoopState gMain;
extern bool8 gSoftResetDisabled,gLinkTransferringData,gFlashMemoryPresent;
extern uint8_t gHeap[];
extern void RegisterRamReset(uint32_t); extern void InitGpuRegManager(void); extern void InitKeys(void); extern void InitIntrHandlers(void);
extern void m4aSoundInit(void); extern void EnableVCountIntrAtLine150(void); extern void InitRFU(void); extern void RtcInit(void);
extern void CheckForFlashMemory(void); extern void InitMainCallbacks(void); extern void InitMapMusic(void); extern void ClearDma3Requests(void);
extern void ResetBgs(void); extern void SetDefaultFontsPointer(void); extern void InitHeap(void *,uint32_t); extern void SetMainCallback2(MainCallback);
extern void ReadKeys(void); extern void rfu_REQ_stopMode(void); extern void rfu_waitREQComplete(void); extern void DoSoftReset(void);
extern bool8 Overworld_SendKeysToLinkIsRunning(void); extern bool8 Overworld_RecvKeysFromLinkIsRunning(void);
extern void UpdateLinkAndCallCallbacks(void); extern void ClearSpriteCopyRequests(void);
extern void PlayTimeCounter_Update(void); extern void MapMusicMain(void); extern void WaitForVBlank(void);
enum { RESET_ALL=0xff,A_BUTTON=1,B_BUTTON=2,SELECT_BUTTON=4,START_BUTTON=8,B_START_SELECT=14,HEAP_SIZE=0x1c000 };

/* BPEJ rev0: 0x080003a4..0x080004bf; non-returning loop. */
void AgbMain(void)
{
    RegisterRamReset(RESET_ALL);
    *(volatile uint16_t *)0x05000000=0x7fff; InitGpuRegManager();
    *(volatile uint16_t *)0x04000204=0x4014;
    InitKeys(); InitIntrHandlers(); m4aSoundInit(); EnableVCountIntrAtLine150();
    InitRFU(); RtcInit(); CheckForFlashMemory(); InitMainCallbacks(); InitMapMusic();
    ClearDma3Requests(); ResetBgs(); SetDefaultFontsPointer(); InitHeap(gHeap,HEAP_SIZE);
    gSoftResetDisabled=0;
    if (gFlashMemoryPresent!=1) SetMainCallback2(0);
    gLinkTransferringData=0;
    for (;;) {
        ReadKeys();
        if (gSoftResetDisabled==0 && (gMain.heldKeysRaw&A_BUTTON)
         && (gMain.heldKeysRaw&B_START_SELECT)==B_START_SELECT) {
            rfu_REQ_stopMode(); rfu_waitREQComplete(); DoSoftReset();
        }
        if (Overworld_SendKeysToLinkIsRunning()==1) {
            gLinkTransferringData=1; UpdateLinkAndCallCallbacks(); gLinkTransferringData=0;
        } else {
            gLinkTransferringData=0; UpdateLinkAndCallCallbacks();
            if (Overworld_RecvKeysFromLinkIsRunning()==1) {
                gMain.newKeys=0; ClearSpriteCopyRequests(); gLinkTransferringData=1;
                UpdateLinkAndCallCallbacks(); gLinkTransferringData=0;
            }
        }
        PlayTimeCounter_Update(); MapMusicMain(); WaitForVBlank();
    }
}
