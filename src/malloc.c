#include <stdint.h>

#define MALLOC_SYSTEM_ID 0xA3A3

typedef uint16_t bool16;

struct MemBlock
{
    bool16 flag;
    uint16_t magic;
    uint32_t size;
    struct MemBlock *prev;
    struct MemBlock *next;
    uint8_t data[];
};

static void *sHeapStart;
static uint32_t sHeapSize;

void PutMemBlockHeader(void *block, struct MemBlock *prev,
                       struct MemBlock *next, uint32_t size)
{
    struct MemBlock *header = block;
    header->flag = 0;
    header->magic = MALLOC_SYSTEM_ID;
    header->size = size;
    header->prev = prev;
    header->next = next;
}

void PutFirstMemBlockHeader(void *block, uint32_t size)
{
    PutMemBlockHeader(block, block, block, size - sizeof(struct MemBlock));
}

void InitHeap(void *heapStart, uint32_t heapSize)
{
    sHeapStart = heapStart;
    sHeapSize = heapSize;
    PutFirstMemBlockHeader(heapStart, heapSize);
}
