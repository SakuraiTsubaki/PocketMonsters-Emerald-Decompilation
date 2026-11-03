# Emerald Div BIOS stub reconstruction

bpe-j-rev0-retail is the Japanese origin reference. All 6 cataloged builds (Japanese, English, German, French, Italian, Spanish) independently verify the Div wrapper at -4 from LZ77UnCompVram. It invokes BIOS SWI 0x06 and exposes quotient, remainder, and absolute quotient results in r0, r1, and r3. Pinned libagbsyscall source corroborates the symbol and calling convention. No ROM bytes are published.
