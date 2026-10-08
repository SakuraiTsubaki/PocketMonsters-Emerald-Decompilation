#include <stdint.h>

typedef uint8_t bool8;

enum {
    FALSE = 0
};

extern bool8 gDisableMusic;
extern void ResetMapMusic(void);

/* Verified independently in the selected Japanese retail ROM. */
void InitMapMusic(void)
{
    gDisableMusic = FALSE;
    ResetMapMusic();
}

