# Emerald play-time counter update reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain one verified Update routine in the same `pointer` cluster. It advances 60 VBlanks per second, 60 seconds per minute and 60 minutes per hour, then calls the exact observed SetToMax entry above 999 hours.

Per-release maps retain code hashes, thresholds, state/save addresses and raw-free control-flow summaries. No ROM instruction bytes are published. Naming and behavior are corroborated by `pret/pokeemerald` at `fe1d8e51b265851676b65885818b1f5f62586135`, `src/play_time.c`.
