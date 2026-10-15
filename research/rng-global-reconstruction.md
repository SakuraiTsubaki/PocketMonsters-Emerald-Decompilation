# Pokémon Emerald global RNG reconstruction

The established six retail identities were reused directly; no release identity was re-investigated. The existing Japanese reconstruction remains the origin reference. The English, German, French, Italian, and Spanish ROMs were independently SHA-256 gated, searched for the complete Emerald `Random` and `SeedRng` Thumb instruction shapes, and closed with publication-safe control-flow graphs.

All six builds implement the same 32-bit recurrence `state = 1103515245 * state + 24691`, return bits 31..16, increment a call counter from `Random`, and clear the auxiliary byte from `SeedRng`. Japanese uses `Random=0x0806f050`, `SeedRng=0x0806f07c`, `gRngValue=0x03005ae0`, `sRandCount=0x02024664`, and `sUnknown=0x02024660`. English, German, and Italian use `0x0806f5cc`/`0x0806f5f8`; French and Spanish use `0x0806f5c8`/`0x0806f5f4`. All international builds use `gRngValue=0x03005d80`, `sRandCount=0x020249c0`, and `sUnknown=0x020249bc`.

The C implementation in `src/random.c` is shared because the verified semantics are identical; address differences remain in the per-release evidence rather than being encoded as source differences. Naming and behavior are corroborated by `pret/pokeemerald@731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/random.c`. Reports and CFGs omit ROM instruction bytes.
