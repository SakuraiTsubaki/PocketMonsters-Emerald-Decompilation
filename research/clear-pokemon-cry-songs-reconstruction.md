# Pokemon Emerald ClearPokemonCrySongs reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain exactly one function with the same 26-byte Thumb structure: a zero halfword is placed on the stack, then `CpuSet` repeats it for 52 halfwords (104 bytes) into the release-specific `gPokemonCrySongs` address.

The reconstructed C source expresses that behavior without embedding ROM instructions. Per-release maps retain function ranges, hashes, call targets, destination addresses, and raw-free control-flow evidence. Naming and semantics are corroborated by `pret/pokeemerald` at `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/main.c`.
