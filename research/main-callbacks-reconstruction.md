# Emerald main callback cluster reconstruction

The Japanese release `bpe-j-rev0-retail` is the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) were verified from `AgbMain` call targets. `CallCallbacks` is reached as the terminal direct callee of `UpdateLinkAndCallCallbacks`; `SetMainCallback2` is reached from `InitMainCallbacks` and cross-checked against the existing global SetMainCallback2 catalog. Per-release maps retain function ranges, hashes, named direct calls and raw-free CFG summaries. No ROM instruction bytes are published.
