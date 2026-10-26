# Emerald VBlankIntr reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) have a VBlank handler immediately after the verified serial callback setter and match the `emerald` control-flow profile. Wireless sync, Trainer Hill counting and battle-dependent RNG suppression are retained.

Per-release maps preserve code hashes, call targets, validated state addresses and the dependency hash for interrupt initialization. CFG evidence omits raw halfwords and no ROM instruction bytes are published. Naming and behavior are corroborated by `pret/pokeemerald` at `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/main.c`.
