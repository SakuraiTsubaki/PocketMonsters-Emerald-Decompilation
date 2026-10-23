#include <stdint.h>

#define CPU_SET_SOURCE_FIXED (1u << 24)
#define POKEMON_CRY_SONG_BYTES 104u

extern uint8_t gPokemonCrySongs[POKEMON_CRY_SONG_BYTES];
extern void CpuSet(const void *source, void *destination, uint32_t mode);

void ClearPokemonCrySongs(void)
{
    const uint16_t zero = 0;
    CpuSet(&zero, gPokemonCrySongs,
           CPU_SET_SOURCE_FIXED | (POKEMON_CRY_SONG_BYTES / sizeof(uint16_t)));
}
