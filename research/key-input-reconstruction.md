# BPEJ revision 0 key-input reconstruction

The Japanese Emerald `InitKeys` is at `0x080005BC` and `ReadKeys` at
`0x080005E4`. The reconstruction preserves the repeat timing, active-low key
mask, L-to-A remapping, and watched-key latch.

Unlike Japanese Ruby/Sapphire, Emerald loads the save-options object through
`gSaveBlock2Ptr` at `0x03005AF0` before reading byte `+0x13`. The code and map
retain this real version difference rather than copying the earlier games'
fixed-object declaration. The ROM code range is hash-locked, while raw ROM
instructions are omitted from publication.
