#include <stddef.h>
#include <stdint.h>

#define DMA3_REQUEST_COUNT 128

typedef uint8_t bool8;

struct Dma3Request
{
    const uint8_t *src;
    uint8_t *dest;
    uint16_t size;
    uint16_t mode;
    uint32_t value;
};

static struct Dma3Request sDma3Requests[DMA3_REQUEST_COUNT];
static volatile bool8 sDma3ManagerLocked;
static uint8_t sDma3RequestCursor;

void ClearDma3Requests(void)
{
    unsigned int i;

    sDma3ManagerLocked = 1;
    sDma3RequestCursor = 0;
    for (i = 0; i < DMA3_REQUEST_COUNT; i++)
    {
        struct Dma3Request *request = &sDma3Requests[i];
        request->size = 0;
        request->src = NULL;
        request->dest = NULL;
    }
    sDma3ManagerLocked = 0;
}
