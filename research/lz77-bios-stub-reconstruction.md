# Emerald LZ77 BIOS stub reconstruction

`bpe-j-rev0-retail` is the Japanese origin reference. All 6 cataloged builds (Japanese, English, German, French, Italian, Spanish) independently contain exactly one adjacent `LZ77UnCompVram`/`LZ77UnCompWram` suite, including the Ruby debug build where cataloged. The wrappers pass source and destination in r0/r1, invoke BIOS SWI 0x12 and 0x11, and return through lr. Pinned upstream libagbsyscall sources corroborate the symbols and order. Maps preserve addresses, semantics, and hashes without publishing ROM bytes.
