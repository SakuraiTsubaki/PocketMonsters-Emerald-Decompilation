#include <stddef.h>
#include <stdint.h>
typedef void (*IntrCallback)(void);
typedef void (*MainCallback)(void);
struct MainInterruptState { MainCallback callback1,callback2; uint8_t unknown_008[4]; IntrCallback vblankCallback,hblankCallback,vcountCallback,serialCallback; };
struct DmaChannelRegisters { const void *source; void *destination; uint32_t control; };
extern struct MainInterruptState gMain;
extern IntrCallback gIntrTable[14];
extern const IntrCallback gIntrTableTemplate[14];
extern const uint8_t IntrMain[];
extern uint8_t IntrMain_Buffer[0x800];
extern void SerialIntr(void);
extern void Timer3Intr(void);
extern void EnableInterrupts(uint16_t flags);
#define DMA3 (*(volatile struct DmaChannelRegisters *)0x040000D4)
#define INTR_VECTOR (*(void (**)(void))0x03007FFC)
#define REG_IME (*(volatile uint16_t *)0x04000208)
#define DMA_ENABLE (1u << 31)
#define DMA_32BIT (1u << 26)
#define INTR_FLAG_VBLANK 1
void SetVBlankCallback(IntrCallback callback);void SetHBlankCallback(IntrCallback callback);void SetVCountCallback(IntrCallback callback);void SetSerialCallback(IntrCallback callback);

/* BPEJ rev0: 0x08000684..0x080006cd. */
void InitIntrHandlers(void)
{
    unsigned i;
    for (i=0;i<14;i++) gIntrTable[i]=gIntrTableTemplate[i];
    DMA3.source=IntrMain;DMA3.destination=IntrMain_Buffer;DMA3.control=DMA_ENABLE|DMA_32BIT|(sizeof(IntrMain_Buffer)/4);
    INTR_VECTOR=(void (*)(void))IntrMain_Buffer;
    SetVBlankCallback(NULL);SetHBlankCallback(NULL);SetSerialCallback(NULL);
    REG_IME=1;EnableInterrupts(INTR_FLAG_VBLANK);
}
void SetVBlankCallback(IntrCallback callback){gMain.vblankCallback=callback;}
void SetHBlankCallback(IntrCallback callback){gMain.hblankCallback=callback;}
void SetVCountCallback(IntrCallback callback){gMain.vcountCallback=callback;}
/* BPEJ rev0: 0x08000714..0x0800072b. */
void RestoreSerialTimer3IntrHandlers(void){gIntrTable[1]=SerialIntr;gIntrTable[2]=Timer3Intr;}
void SetSerialCallback(IntrCallback callback){gMain.serialCallback=callback;}
