# Emerald play-time counter controls reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain one verified Reset/Start/Stop/SetToMax control family using the `pointer` save-storage profile. Start calls the observed SetToMax entry when hours exceed 999.

Per-release maps preserve ranges, hashes, state/save addresses and raw-free control-flow summaries. No ROM instruction bytes are published. Naming and behavior are corroborated by `pret/pokeemerald` at `fe1d8e51b265851676b65885818b1f5f62586135`, `src/play_time.c`.
