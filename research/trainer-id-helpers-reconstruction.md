# BPEJ-rev0 trainer-ID helper reconstruction

The verified Japanese ROM contains the following four-byte trainer-ID helpers:

- `SetTrainerId`: `0x08083C54..0x08083C64`, SHA-256 `b219139d5a72a06b84b59c718f14ddff68a10a2a3e7c77994251bbc8cd5ca40b`.
- `GetTrainerId`: `0x08083C64..0x08083C7C`, SHA-256 `007d0bda88f16c7dd47124c261ed6846f26451d6862ac00c3cdecc3cc09d07b1`.
- `CopyTrainerId`: `0x08083C7C..0x08083C98`, SHA-256 `e2ede032f2797356414ff7d8a4c5803c4350847c7d86acc47bf4ba92bb5e75e5`.

The setters serialize a 32-bit value in little-endian order. Copy helpers move exactly four bytes; the Emerald-specific getter reconstructs the same little-endian value. Every function has one observed return, and none calls another routine.

Names and behavior are corroborated by `pret/pokeemerald` commit `fe1d8e51b265851676b65885818b1f5f62586135`, `src/new_game.c`. The ROM digests and publication-safe CFGs are authoritative here. No ROM instruction bytes are published.
