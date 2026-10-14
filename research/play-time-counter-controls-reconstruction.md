# BPEJ-rev0 play-time counter control reconstruction

The verified Japanese ROM contains four control routines surrounding the previously reconstructed update routine:

- `PlayTimeCounter_Reset`: `0x08083B6C..0x08083B88`, 28 bytes, SHA-256 `6dee17d890810e71b59343bb41a46213bf2e2b6d4b795b06442fe99e9b90419a`.
- `PlayTimeCounter_Start`: `0x08083B90..0x08083BAC`, 28 bytes, SHA-256 `245be510a80dba9e5609035282e375dc8797d647a0f0d99ea5b1fea1832fc3c1`.
- `PlayTimeCounter_Stop`: `0x08083BB8..0x08083BC0`, 8 bytes, SHA-256 `af63598031ab14af781d7cf7af24c648b7677228730b316da86ab311a3171699`.
- `PlayTimeCounter_SetToMax`: `0x08083C2C..0x08083C48`, 28 bytes, SHA-256 `3692df09faf1ac9b5829de52fdb5d912456f627f60d484b3f5e9d636b86a1e33`.

The publication-safe CFGs prove one return for every routine. Only `PlayTimeCounter_Start` has a call: when the saved hour count exceeds 999, it calls the observed `PlayTimeCounter_SetToMax` entry. Reset clears the state and all four saved counters, Stop clears only the state, and SetToMax stores state 2 with 999:59:59 plus 59 VBlanks.

Save access is recorded as `gSaveBlock2Ptr`. Names and behavior are corroborated by `pret/pokeemerald` commit `fe1d8e51b265851676b65885818b1f5f62586135`, `src/play_time.c`.

No ROM instruction bytes are published.
