# BPEJ rev0 RNG reconstruction

The verified Japanese ROM reaches `Random` at `0x0806F050` from `VBlankIntr`; `SeedRng` begins at `0x0806F07C`. Publication-safe CFGs close both straight-line Thumb functions at one return with no calls.

Literal and instruction-shape validation proves the same 32-bit recurrence `state = 1103515245 * state + 24691`, returning bits 31..16. Emerald additionally increments `sRandCount` at `0x02024664` on every call and clears `sUnknown` at `0x02024660` when seeding; the RNG state is `0x03005AE0`.

Names and semantics are corroborated by pinned primary source `pret/pokeemerald@731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/random.c`. No ROM instruction bytes are published.
