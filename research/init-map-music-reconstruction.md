# InitMapMusic reconstruction

The selected Japanese retail target places `InitMapMusic` at `0x080A269C` through `0x080A26AC`. The 16-byte Thumb routine clears `gDisableMusic`, calls `ResetMapMusic`, and returns.

Its publication-safe CFG records one direct call at `0x080A26A4` to `0x080A27A8` and omits raw halfwords. The exact ROM range SHA-256 is `208cc1ca4b9d4d1ab7ff55f003e775a720b1f0e2f8ac1be80107ce41c8a250be`.

Ruby, Sapphire, Emerald, FireRed, and LeafGreen use byte-identical code for this routine even though their ROM addresses differ. The C naming and semantics are corroborated by `pret/pokeemerald` commit `fe1d8e51b265851676b65885818b1f5f62586135`, `src/sound.c`; the local retail ROM and its own SHA-256 remain the authoritative evidence for this repository.

