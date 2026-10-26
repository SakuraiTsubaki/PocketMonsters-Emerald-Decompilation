# Pokemon Emerald EnableVCountIntrAtLine150 reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain exactly one 40-byte Thumb function with the same constant and call-order structure. It preserves the low DISPSTAT byte, selects VCount line 150, enables the DISPSTAT VCount bit, and enables interrupt flag 0x0004.

The reconstructed C source contains no ROM instructions. Per-release maps preserve function ranges, hashes and call targets, while CFG evidence omits raw halfwords. Naming and semantics are corroborated by `pret/pokeemerald` at `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/main.c`.
