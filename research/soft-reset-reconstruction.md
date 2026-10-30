# Emerald SoftReset reconstruction

`bpe-j-rev0-retail` is the Japanese origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) resolve DoSoftReset to the same SDK wrapper. It disables REG_IME, moves SP to 0x03007F00, invokes BIOS RegisterRamReset through SWI 1 with flags in r0, then performs the non-returning SWI 0 soft reset. Maps preserve addresses, decoded behavior and hashes without ROM bytes or instruction dumps.
