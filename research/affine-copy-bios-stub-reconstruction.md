# Emerald affine and fast-copy BIOS stub reconstruction

bpe-j-rev0-retail is the Japanese origin reference. All 6 cataloged builds (Japanese, English, German, French, Italian, Spanish) independently contain exactly one BgAffineSet, CpuFastSet, and ObjAffineSet Thumb wrapper, including the Ruby debug build where cataloged. Unique SWI signatures are cross-checked at family-specific offsets from the verified LZ77 VRAM wrapper. Pinned upstream libagbsyscall sources corroborate symbols and calling conventions. No ROM bytes are published.
