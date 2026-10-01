# BPEJ revision 0 `AgbMain` reconstruction

The verified Japanese Emerald CFG covers `0x080003A4..0x080004BF`, contains 29
direct calls, and loops from `0x080004BE` to the frame body at `0x0800042A`.
All call sites are mapped against `pret/pokeemerald` `src/main.c` at commit
`fe1d8e51b265851676b65885818b1f5f62586135`.

Emerald shares RFU-aware link processing with FRLG but retains `RtcInit`, lacks
the FireRed/LeafGreen help-system initialization, and gates its initial callback
when flash memory is unavailable. BPEJ rev0 does not call debug printing or the
optional bugfix-only RTC seed routine. The reconstruction preserves those
observed build differences instead of treating all third-generation loops as
interchangeable. No ROM instruction bytes are published.
