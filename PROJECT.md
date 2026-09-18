# Target Profile: Pokémon Emerald / Pocket Monsters Emerald

## Known repository scope

- Repository: `SakuraiTsubaki/PocketMonsters-Emerald-Decompilation`
- Working target: Pokémon Emerald / Pocket Monsters Emerald
- Platform family: Game Boy Advance
- Series generation: Generation III
- Exact target set: six unique verified retail ROM identities
  - BPEJ — Japan / Japanese
  - BPEE — USA/Europe / English
  - BPED — Germany / German
  - BPEF — France / French
  - BPEI — Italy / Italian
  - BPES — Spain / Spanish
- Software version byte: 0 for all six selected identities
- ROM size: 16 MiB for all six selected identities

The exact hashes, header checksums, observed input names, and duplicate English aliases are recorded in `config/target.json`. Original ROM binaries remain local and are never committed.

## Identity findings

Seven ROM files were observed locally, but the two English files named `Pokemon - Emerald Version (U).gba` and `Pokemon - Emerald Version (USA, Europe).gba` are byte-identical and share SHA-256 `a9dec84dfe7f62ab2220bafaef7479da0929d066ece16a6885f6226db19085af`. The working matrix therefore contains six unique binary identities.

All six unique inputs have a 16 MiB size, `POKEMON EMER` header title, maker code `01`, software version `0`, the expected GBA fixed header byte, and a valid calculated header complement checksum.

## Research priorities

- Reconstruct shared and localization-specific code/data boundaries across the six selected identities.
- Identify ARM and Thumb code boundaries, calling conventions, compiler fingerprints, and data/code references.
- Map pointer tables, compression, graphics, text, audio, scripts, and other target-specific resource formats.
- Build deterministic extraction and comparison tools around hash-verified local inputs.
- Define byte, layout, state, and behavior-based verification for each reconstructed component.
- Preserve reproducible evidence and every lawful non-ROM work product.

## First milestone

The original target-identification portion of the foundation milestone is complete. The next foundation milestone is complete when:

1. a reproducible source baseline is present or synchronized;
2. high-confidence code and data boundaries are recorded for every selected identity;
3. shared and localization-specific structures can be compared deterministically;
4. reconstructed components record applicability across BPEJ/BPEE/BPED/BPEF/BPEI/BPES;
5. all commands needed to reproduce the analysis and tests are documented.

## Non-ROM artifact preservation

Follow [ARTIFACT_POLICY.md](ARTIFACT_POLICY.md). Preserve all storable non-ROM research, source, scripts, tools, logs, manifests, tables, structured data, graphics, sprites, palettes, fonts, icons, tiles, converted data, patches, and verification material. Graphics work must include actual PNG output.
