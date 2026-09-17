# Emerald zero-known-defect campaign

## Goal

Remove reproducible bugs, glitches, crashes, softlocks, corruption paths, undefined behavior, incorrect mechanics, event/script mistakes, collision errors, graphical/audio defects, localization-specific faults, exploitable duplication paths, and other unintended behavior from the maintained Emerald implementation.

"All fixed" is not defined as "all items from one public glitch list are fixed." Completion requires convergence of independent evidence sources and a clean regression matrix across every selected ROM variant.

## Verified input baselines

The selected local ROM identities are recorded in `config/target.json`. There are seven observed files but six unique SHA-256 identities because the two observed English inputs are byte-identical. ROM binaries stay outside Git.

Every defect record must state which of the six unique targets were tested:

- BPEJ — Japan / Japanese
- BPEE — USA/Europe / English
- BPED — Germany / German
- BPEF — France / French
- BPEI — Italy / Italian
- BPES — Spain / Spanish

## Evidence sources

The campaign merges, deduplicates, and verifies findings from all of the following:

1. Current `pret/pokeemerald` source annotations and fixes, including `BUGFIX` and `UBFIX` paths pinned in `manifests/bugs/pret-marked-bug-surface.csv`.
2. Public glitch and oversight catalogs, initially seeded in `research/bugs/public-catalog-seed.csv`.
3. Direct binary comparison of the six unique retail ROM identities.
4. Static analysis of reconstructed/decompiled source: compiler warnings, sanitizable host-side logic, range checks, integer width/sign issues, array bounds, uninitialized state, dead/fallthrough script paths, invalid pointers, unsafe division, and state-machine invariants.
5. Dynamic emulator testing: deterministic input playback, save/load cycles, RTC transitions, battle facilities, link/wireless paths where testable, graphics/audio stress, and long-run soak tests.
6. Differential tests between retail behavior, reconstructed behavior, and explicitly corrected expected behavior.
7. Fuzz/property tests for parsers, scripts, tables, battle commands, save data handling, compression/decompression, and UI state transitions.

No single source is treated as complete.

## Defect classes

Every finding receives one or more classes:

- `crash` — freeze, invalid opcode, emulator-dependent failure, hard lock
- `softlock` — game remains running but normal progress/input recovery fails
- `memory` — out-of-bounds, uninitialized use, corruption, unsafe aliasing, undefined behavior
- `save` — save corruption, rollback, cloning/duplication, invalid persistence
- `battle` — incorrect move/ability/item/status/AI/facility mechanics
- `overworld` — movement, map transition, NPC, event, current, dive, field-state fault
- `script` — wrong command, missing terminator, stale variable/flag, bad state transition
- `collision` — incorrect metatile or movement permission
- `data` — wrong table entry, text property, move details, encounter/item/species metadata
- `graphics` — sprite, palette, tile, window, animation or display corruption
- `audio` — stuck/missing/wrong sound or music state
- `rtc-rng` — RTC state, seed, timing, random-selection or persistence error
- `link` — cable/wireless synchronization, serialization or remote-state error
- `localization` — language/region-only behavior or asset/data error
- `exploit` — cloning, arbitrary-code-enabling chain, unintended state manipulation

## Required lifecycle for every defect

A defect is not closed by code inspection alone.

1. `reported` — external report, source annotation, static-analysis hit, differential mismatch, or test failure exists.
2. `reproduced` — exact steps, preconditions, expected result, actual result, target hashes and evidence are recorded.
3. `localized` — responsible function/script/data region and root cause are identified.
4. `fixed` — minimal corrective change is implemented without intentionally changing unrelated behavior.
5. `regression-test` — an automated test fails before the fix and passes after it whenever automation is technically possible.
6. `cross-variant` — all six unique retail target identities are checked for applicability or explicitly marked not applicable with evidence.
7. `verified` — rebuild/runtime/static checks are clean and no adjacent regression is observed.
8. `closed` — source, test, report, logs, patch/commit identity and verification artifact are all retained in Git.

## Immediate source policy

When a `pret/pokeemerald` source base is imported or synchronized, both the ordinary bug-fix paths and genuine undefined-behavior fixes are baseline requirements, not optional compatibility toggles for the corrected build. Retail-matching builds may retain switches for comparison, but the maintained corrected build must use the fixed behavior.

Source-marked fixes are only the first layer. Public Emerald-specific defects such as Battle Tower cloning, Pomeg-based invalid party/state manipulation, Battle Pike poison knockout, Hidden Power disobedience behavior, collision/event oversights, and language-specific field errors require independent reproduction and regression coverage even when they are not represented by one `BUGFIX` marker.

## Test matrix

For each applicable fix, record at minimum:

| Dimension | Required coverage |
| --- | --- |
| ROM identity | BPEJ, BPEE, BPED, BPEF, BPEI, BPES |
| Build | retail-match reference + corrected build |
| Emulator | mGBA baseline; second independent emulator for hardware-sensitive cases when available |
| Save state | fresh save and representative progressed save when state-dependent |
| RTC | normal time plus boundary cases for RTC-dependent code |
| Battle | singles/doubles/facility/link context as applicable |
| Language | verify text/window/tile differences do not reintroduce behavior faults |

## Zero-known-defect release gate

A release may be described as `zero-known-defect` only when all of these are true at the pinned source revision:

- no open reproduced defect remains in the project registry;
- every `BUGFIX` and `UBFIX` item from the pinned upstream audit has been reviewed and either integrated or rejected with evidence;
- every item in the maintained public catalog has a verified disposition;
- compiler/static-analysis gates have no unexplained high-confidence findings;
- automated regression tests are green across the corrected build matrix;
- deterministic emulator suites complete without crash, softlock, corruption, assertion or unexplained behavioral divergence;
- save round-trip, RTC boundary, battle facility, overworld transition and long-run soak suites pass;
- six-variant differential checks have no unexplained executable/data differences relevant to shared behavior;
- the remaining limitations list contains only explicitly out-of-scope hardware/environment issues, not known game defects.

The phrase means "no defects known after the documented search and test campaign," not a claim that undiscovered defects are mathematically impossible.

## Current starting artifacts

- `config/target.json` — six unique verified Emerald ROM identities.
- `tools/scan_emerald_roms.py` — read-only local ROM fingerprint and deduplication utility.
- `manifests/bugs/pret-marked-bug-surface.csv` — pinned upstream source files containing `BUGFIX` or `UBFIX` markers.
- `research/bugs/public-catalog-seed.csv` — first public Emerald/Gen III bug and oversight seed list.

Next implementation work should populate the source tree, convert the two seed inventories into one deduplicated defect registry, and begin with memory/UB, save-corruption/cloning, crash/softlock and battle-state defects before cosmetic-only issues.
