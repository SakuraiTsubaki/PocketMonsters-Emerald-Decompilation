# Emerald key input reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain exactly one InitKeys and ReadKeys pair matching the `pointer` profile. Options are read through the gSaveBlock2Ptr indirection.

The pair establishes repeat delays 5 and 40, derives active-high keys from REG_KEYINPUT with mask 0x03FF, implements repeat behavior, applies L-equals-A mode, and records watched-key presses. Per-release maps retain ranges, hashes, validated literals and control-flow counts without ROM instruction bytes. Naming and behavior are corroborated by `pret/pokeemerald` at `fe1d8e51b265851676b65885818b1f5f62586135`, `src/main.c`.
