# Emerald display and serial interrupt reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain exactly one HBlank, VCount and Serial handler matching the `emerald` structural profile. VCount invokes the optional callback and then m4aSoundVSync.

Each handler sets both the shared IWRAM interrupt check and gMain.intrCheck with HBlank 0x0002, VCount 0x0004 or Serial 0x0080. Per-release maps retain ranges, code hashes, validated literals and call targets without publishing ROM instruction bytes. Naming and behavior are corroborated by `pret/pokeemerald` at `731ad5e7e7a8031b79629077efbc8409c1363a70`, `src/main.c`.
