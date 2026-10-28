# Emerald flash-memory detection reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) preserve the same 38-byte control-flow shape: `IdentifyFlash` returns zero on success, the presence flag is set, and `InitFlashTimer` is called only on that success path. Per-release maps retain addresses, calls and code hashes without ROM bytes or instruction halfwords. `pret/pokeemerald` commit `fe1d8e51b265851676b65885818b1f5f62586135`, `src/load_save.c`, is the naming basis.
