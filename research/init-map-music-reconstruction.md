# Emerald InitMapMusic reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain exactly one verified InitMapMusic routine. It clears the release-specific IWRAM gDisableMusic byte and calls ResetMapMusic. Per-release maps preserve ranges, hashes, call targets and raw-free control flow. No ROM instruction bytes are published. Naming is corroborated by `pret/pokeemerald` at `fe1d8e51b265851676b65885818b1f5f62586135`, `src/sound.c`.
