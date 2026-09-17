# Generation III defect research

This directory is the research intake layer for the zero-known-defect campaign.

## Current catalogs

### `public-catalog-seed.csv`

Emerald-focused working seed. It includes shared RSE / GBA defects that can affect Emerald and explicitly marks cross-title items that are **not** applicable to Emerald so they are not accidentally patched into the wrong game.

### `generation-iii-public-catalog.csv`

Cross-title Generation III public-source intake. The initial snapshot contains 72 candidate records spanning:

- Ruby / Sapphire;
- Emerald;
- FireRed / LeafGreen;
- Pokémon Colosseum;
- Pokémon XD: Gale of Darkness;
- Pokémon Box Ruby & Sapphire;
- Pokémon Channel distribution behavior where it directly affects Generation III game data.

The initial records cover the headings in the public Generation III general, battle, and overworld glitch catalogs plus directly relevant revision/distribution defects found during the same audit.

**This file is not a completeness claim.** The public battle-glitch catalog itself is explicitly marked incomplete, and public lists cannot reveal undiscovered defects or every region/revision-specific implementation fault.

## Independent source-code surface

`../../manifests/bugs/pret-marked-bug-surface.csv` is a separate source-code evidence stream pinned to `pret/pokeemerald@5eff78649e7170a877b961ef0b3da13b81a16038`.

It contains 94 marker/path records:

- 56 `BUGFIX` records;
- 38 `UBFIX` records.

These markers must be audited even if no public glitch page describes the behavior.

Use `../../tools/audit_bug_surface.py` against the exact pinned source tree to detect missing expected paths, removed expected markers, and newly discovered marker sites that are absent from the manifest.

## Required expansion streams

The Generation III project-wide registry must continue beyond these seeds with independent sweeps of:

1. upstream source history, bug-fix commits, open/closed issues and pull requests;
2. Ruby/Sapphire and FireRed/LeafGreen decompilation/disassembly bug annotations;
3. regional and revision binary diffs, especially fixes introduced in later cartridge revisions;
4. save/RTC/Berry update behavior and official patch delivery paths;
5. Battle Frontier, Contest, AI, breeding, roamer and storage edge cases;
6. link cable, Wireless Adapter/RFU, Mystery Event/Gift, e-Reader/e-Card and GameCube-GBA communication;
7. Colosseum/XD battle, Shadow Pokémon, Snag/Purification and trade connectivity;
8. Pokémon Box storage, Adventure mode, memory-card and ribbon behavior;
9. Pokémon Channel and game-based distribution transfer behavior;
10. script/flag/warp/collision/map/event sweeps;
11. static-analysis findings and compiler undefined behavior;
12. fuzzing, deterministic emulator replay, save-state transition tests and long-run soak tests;
13. exploit chains including cloning, corruption, Pomeg-derived state manipulation and arbitrary-code-execution enablers;
14. graphics, audio, localization, text and data-table inconsistencies;
15. unused/dummy data only when it can affect execution or represents an intended-but-broken path.

## Disposition rule

Every candidate remains `unverified` until it is independently checked against the exact game/region/revision. A record must not be promoted directly from a wiki heading or upstream patch to `fixed`.

Final closure requires: reproduction/applicability evidence, root cause, fix, regression coverage, region/revision disposition, and compatibility review as defined in `../../docs/BUG_ERADICATION.md` and `../../config/bugfix-policy.json`.
