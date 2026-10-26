#include <stdint.h>

typedef uint8_t bool8;
typedef uint8_t u8;
typedef uint16_t u16;

extern u16 sCurrentMapMusic;
extern u16 sNextMapMusic;
extern u8 sMapMusicState;
extern u8 sMapMusicFadeInSpeed;

extern void PlayBGM(u16 songNum);
extern bool8 IsBGMStopped(void);
extern bool8 IsFanfareTaskInactive(void);
extern void FadeInNewBGM(u16 songNum, u8 speed);

void MapMusicMain(void)
{
    switch (sMapMusicState)
    {
    case 0:
        break;
    case 1:
        sMapMusicState = 2;
        PlayBGM(sCurrentMapMusic);
        break;
    case 2:
    case 3:
    case 4:
        break;
    case 5:
        if (IsBGMStopped())
        {
            sNextMapMusic = 0;
            sMapMusicState = 0;
        }
        break;
    case 6:
        if (IsBGMStopped() && IsFanfareTaskInactive())
        {
            sCurrentMapMusic = sNextMapMusic;
            sNextMapMusic = 0;
            sMapMusicState = 2;
            PlayBGM(sCurrentMapMusic);
        }
        break;
    case 7:
        if (IsBGMStopped() && IsFanfareTaskInactive())
        {
            FadeInNewBGM(sNextMapMusic, sMapMusicFadeInSpeed);
            sCurrentMapMusic = sNextMapMusic;
            sNextMapMusic = 0;
            sMapMusicState = 2;
            sMapMusicFadeInSpeed = 0;
        }
        break;
    }
}
