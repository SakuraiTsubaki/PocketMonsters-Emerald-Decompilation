#include <stdint.h>

typedef int32_t s32;
typedef uint8_t u8;
typedef uint32_t u32;

void SetTrainerId(u32 trainerId, u8 *dst)
{
    dst[0] = trainerId;
    dst[1] = trainerId >> 8;
    dst[2] = trainerId >> 16;
    dst[3] = trainerId >> 24;
}

u32 GetTrainerId(const u8 *trainerId)
{
    return (trainerId[3] << 24)
         | (trainerId[2] << 16)
         | (trainerId[1] << 8)
         | trainerId[0];
}

void CopyTrainerId(u8 *dst, const u8 *src)
{
    s32 i;

    for (i = 0; i < 4; i++)
        dst[i] = src[i];
}
