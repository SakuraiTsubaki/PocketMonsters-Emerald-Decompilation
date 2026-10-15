# Pokémon Emerald secondary RNG reconstruction

Emerald's six established retail identities were used without repeating release identification. Each ROM contains one structurally linked `SeedRng2`/`Random2` pair: `Random2` follows the seed function and its literal pool, and both address the same independent `gRng2Value`. This adjacency and shared-state condition disambiguates the pair from other code that happens to use the same short compiler instruction shapes.

All builds use `state = 1103515245 * state + 24691` and return bits 31..16, but the state is independent from the primary RNG. Japanese places `SeedRng2` at `0x0806f094`, `Random2` at `0x0806f0a4`, and `gRng2Value` at `0x03005ae4`. English, German, and Italian use `0x0806f610`, `0x0806f620`, and `0x03005d84`; French and Spanish use `0x0806f60c`, `0x0806f61c`, and the same international state address.

The reconstructed C implementation adds `gRng2Value`, `SeedRng2`, and `Random2` to `src/random.c`. Names and semantics are corroborated by `pret/pokeemerald@731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/random.c`. Per-release reports and CFGs omit ROM instruction bytes.
