# Pokemon Emerald DoSoftReset global reconstruction

The existing Japanese reconstruction remains the origin reference. All 6 cataloged releases (Japanese, English, German, French, Italian, Spanish) disable IME, stop sound VSync and the scanline effect, disable DMA channels 1 through 3, and invoke SoftReset. Observed variants: rtc-full-reset.

RTC-family builds call `SiiRtcProtect` and reset with mask `0xFF`; FireRed/LeafGreen builds omit RTC protection and preserve SIO registers with mask `0xDF`. Per-release maps retain ranges, hashes, ordered call targets, hardware writes, and raw-free CFGs. No ROM instructions or binaries are published.

Naming and behavior are corroborated by `pret/pokeemerald` at `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, `src/main.c`.
