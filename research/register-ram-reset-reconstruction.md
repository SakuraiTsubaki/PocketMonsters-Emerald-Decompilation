# Emerald RegisterRamReset reconstruction

`bpe-j-rev0-retail` is the Japanese origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) resolve the AgbMain call to a two-instruction Thumb wrapper: BIOS software interrupt 1 followed by return through LR. The wrapper consumes reset flags in r0. Per-release maps preserve addresses and hashes without ROM bytes or instruction dumps.
