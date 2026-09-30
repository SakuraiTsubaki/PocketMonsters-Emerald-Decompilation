# Main callback reconstruction

The first repeated bootstrap target at `0x080004c4` is no longer left as an
anonymous address. Its control flow, the two adjacent routines it reaches, and
the matching public reference source jointly establish three functions:

| BPEJ rev0 range | Reconstructed function | Key evidence |
| --- | --- | --- |
| `0x080004c4..0x080004d7` | `UpdateLinkAndCallCallbacks` | Predicate call; skip-or-dispatch branch |
| `0x0800051c..0x08000539` | `CallCallbacks` | Two nullable callback slots; two indirect dispatches |
| `0x08000540..0x0800054f` | `SetMainCallback2` | Callback store at `+0x4`; state-byte clear at `+0x438` |

The names are adopted only after the BPEJ rev0 access pattern matches
`pret/pokeemerald` `src/main.c`; they are not inferred from addresses alone.
The local source intentionally defines only the `gMain` layout portion proven
by these accesses. Unknown bytes remain opaque instead of receiving speculative
field names.

`analysis/emerald-jp-main-callbacks-map.json` records the address mapping and
the reference basis. The publication-safe CFG retains addresses and edge kinds
but omits instruction halfwords, so no ROM fragment is committed.
