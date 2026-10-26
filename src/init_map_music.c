#include <stdint.h>

typedef uint8_t bool8;

enum
{
    FALSE = 0
};

extern bool8 gDisableMusic;
extern void ResetMapMusic(void);

void InitMapMusic(void)
{
    gDisableMusic = FALSE;
    ResetMapMusic();
}
