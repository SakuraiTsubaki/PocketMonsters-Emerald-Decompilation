# BPEJ rev0 MapMusicMain reconstruction

The verified Japanese ROM implements `MapMusicMain` across `0x080A26B0..0x080A2797`. The contiguous 232-byte function range has SHA-256 `2028900fc8662f31cf6e4bccc0027e79ea374777bd688159bb6e4f8b06d7e752`; only its hash and publication-safe CFG are retained.

The function uses an agbcc-style absolute-word jump table with eight entries. `SakuraiTsubaki/Decompilation` commit `4f687a912ecc40823a17a67fa885768cdca12e98` extends the shared Thumb tracer to resolve this exact compiler pattern without treating the literal pool and table as instructions. The resulting CFG reaches every case and records eight direct calls.

Behavior and names are corroborated by `pret/pokeemerald` commit `fe1d8e51b265851676b65885818b1f5f62586135`, `src/sound.c`: state 1 starts the current BGM, state 5 waits for BGM completion, state 6 waits for both BGM and fanfare completion before starting the queued track, and state 7 performs the corresponding fade-in transition. Emerald explicitly treats states 2, 3, and 4 as idle and uses its own sound-engine targets.

`src/map_music_main.c` is a behavioral reconstruction bound to the ROM CFG, jump-table targets, call order, and code-range hash. No ROM instruction bytes or table words are published.

