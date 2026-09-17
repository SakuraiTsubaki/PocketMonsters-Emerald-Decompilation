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
- Maintain a cross-variant defect registry and remove reproducible bugs, glitches, undefined behavior, crashes, softlocks, corruption paths, data errors, collision mistakes, audiovisual faults, localization-only defects, and exploit chains.
- Define byte, layout, state, and behavior-based verification for each reconstructed or corrected component.

## Defect-eradication baseline

The zero-known-defect campaign is defined in `docs/BUG_ERADICATION.md`.

Initial evidence has been pinned in:

- `manifests/bugs/pret-marked-bug-surface.csv` for current upstream `BUGFIX` and `UBFIX` source surfaces;
- `research/bugs/public-catalog-seed.csv` for public Emerald and shared Generation III glitch/oversight reports;
- `tools/scan_emerald_roms.py` for repeatable local ROM identity verification.

No single public catalog is considered complete. Completion requires source review, binary comparison, static analysis, dynamic emulator testing, fuzz/property testing, and regression coverage across every applicable target identity.

## First milestone

The original target-identification portion of the foundation milestone is complete. The next foundation milestone is complete when:

1. a reproducible source baseline is present or synchronized;
2. the upstream and public seed inventories are merged into one deduplicated defect registry;
3. high-risk memory/UB, save-corruption/cloning, crash/softlock, and battle-state defects have automated regression tests where technically possible;
4. each fix records applicability across BPEJ/BPEE/BPED/BPEF/BPEI/BPES;
5. all commands needed to reproduce the analysis and tests are documented.

## Non-ROM artifact preservation

Follow [ARTIFACT_POLICY.md](ARTIFACT_POLICY.md). Preserve all storable non-ROM research, source, scripts, tools, logs, manifests, tables, structured data, graphics, sprites, palettes, fonts, icons, tiles, converted data, patches, and verification material. Graphics work must include actual PNG output.
