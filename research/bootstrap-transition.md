# BPEJ bootstrap ARM-to-Thumb transition

Without repeating Emerald's established identity work, the BPEJ entry path is extended from `0x08000204` through twelve ARM words to `bx r1` at `0x08000230`. Literal `0x080003a5` at `0x08000244` proves transition into Thumb code at `0x080003a4`.
