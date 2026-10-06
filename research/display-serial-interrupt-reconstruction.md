# BPEJ revision 0 display and serial interrupts

Japanese Emerald conditionally dispatches the HBlank, VCount, and serial
callbacks stored in `gMain`, then acknowledges each interrupt in the BIOS
check word and `gMain.intrCheck`. Its VCount handler additionally calls the
game-specific `m4aSoundVSync` target after the callback. The map records all
boundaries, call targets, offsets, flags, and a publication-safe range hash.

