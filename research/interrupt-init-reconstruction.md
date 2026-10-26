# Emerald interrupt initialization reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain exactly one InitIntrHandlers structure and its callback setters matching the `emerald` profile. VBlank is enabled through EnableInterrupts and a separate function restores Serial and Timer3 handlers.

The implementation copies 14 table entries, DMA-copies the 0x800-byte interrupt dispatcher with DMA3 control 0x84000200, installs the IWRAM vector, clears callbacks and enables VBlank. Per-release maps retain code ranges, hashes, validated literals and call targets without ROM instruction bytes. Naming and behavior are corroborated by `pret/pokeemerald` at `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/main.c`.
