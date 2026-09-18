# PocketMonsters-Emerald-Decompilation

A complete, target-specific workspace for reproducible research, analysis, tooling, source reconstruction, and retained non-ROM work products related to **Pokémon Emerald / Pocket Monsters Emerald**.

| Field | Value |
| --- | --- |
| Working target | Pokémon Emerald / Pocket Monsters Emerald |
| Platform family | Game Boy Advance |
| Series generation | Generation III |
| Exact build identity | Six unique verified retail ROM identities: BPEJ, BPEE, BPED, BPEF, BPEI, BPES |
| Foundation status | ROM identities selected; ready for evidence-backed reconstruction work |

Machine-readable hashes and header identities are stored in [`config/target.json`](config/target.json). Original ROM binaries remain local inputs and are never committed.

## Repository areas

| Area | Responsibility |
| --- | --- |
| [`research/`](research/) | References, collected material, experiments, questions, and methodology. |
| [`analysis/`](analysis/) | Symbols, structures, formats, comparisons, and verified findings. |
| [`tools/`](tools/) | Target adapters and extraction, inspection, conversion, build, and verification utilities. |
| [`src/`](src/) | Reviewed reconstruction and source-linked data. |
| [`config/`](config/) | Target identity, symbols, mappings, and reproducible configuration. |
| [`artifacts/`](artifacts/) | Generated or collected non-ROM outputs, including graphics and converted data. |
| [`manifests/`](manifests/) | Hashes, inventories, file maps, and build records. |
| [`logs/`](logs/) | Research, extraction, conversion, build, comparison, and verification logs. |
| [`patches/`](patches/) | Patch files, generation scripts, manifests, and verification results. |
| [`tests/`](tests/) | Unit, regression, comparison, and build-verification checks. |
| [`progress/`](progress/) | Evidence-backed milestones and blockers. |
| [`docs/`](docs/) | Target workflow and architecture documentation. |

Target-independent work belongs in [`SakuraiTsubaki/Decompilation`](https://github.com/SakuraiTsubaki/Decompilation).

## Start here

1. Verify local inputs with `python tools/scan_emerald_roms.py <roms...>` and compare them with [`config/target.json`](config/target.json).
2. Begin a focused record from [`research/template.md`](research/template.md).
3. Promote reproducible conclusions through [`analysis/template.md`](analysis/template.md).
4. Commit every storable non-ROM result produced or collected during the work.
5. Run `python scripts/check_repository.py .` and the unit tests.

## Storage rule

Only original, modified, or rebuilt ROM binaries—and equivalent complete game-image/package binaries—are excluded from GitHub. Commit all other storable work products: analysis, research, reports, documents, scripts, source, tools, settings, logs, manifests, checklists, tables, CSV/JSON/YAML, graphics, sprites, images, palettes, fonts, icons, tiles, converted data, patches, and validation material.

Graphics and sprite work must include actual viewable PNG output in addition to data and metadata. See [ARTIFACT_POLICY.md](ARTIFACT_POLICY.md).

Secrets, credentials, and private keys are not work products and must not be committed.
