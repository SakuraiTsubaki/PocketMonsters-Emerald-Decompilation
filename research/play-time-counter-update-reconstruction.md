# BPEJ rev0 PlayTimeCounter_Update reconstruction

The verified Japanese ROM implements `PlayTimeCounter_Update` across `0x08083BC4..0x08083C1F`. Its 92-byte code range has SHA-256 `4307a398f162c7bc732bb41036bbc531ffd4049ce7cea4a9920d24ef779cb4d8`; the repository retains only this digest and a publication-safe CFG.

The CFG has ten direct branch edges, one return, and one call to `PlayTimeCounter_SetToMax`. The routine runs only in state 1, rolls 60 VBlanks into one second, 60 seconds into one minute, and 60 minutes into one hour, then clamps values when hours exceed 999. Save fields are accessed at offsets `0x0E`, `0x10`, `0x11`, and `0x12` through `gSaveBlock2Ptr`.

Names and behavior are corroborated by `pret/pokeemerald` commit `fe1d8e51b265851676b65885818b1f5f62586135`, `src/play_time.c`. `src/play_time_counter.c` preserves this title family's direct-versus-pointer save access rather than forcing all five games into one binary layout.

No ROM instruction bytes are published.

