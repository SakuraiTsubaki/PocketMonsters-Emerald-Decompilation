# BPEJ revision 0 interrupt initialization

Emerald copies 14 handlers and the 0x800-byte `IntrMain` buffer like the
earlier games, but enables VBlank through `EnableInterrupts` after setting
`REG_IME`. It also provides `RestoreSerialTimer3IntrHandlers`, restoring table
slots 1 and 2 to Emerald's serial and timer3 handlers. The reconstruction and
map preserve these version-specific behaviors and exact Japanese addresses
without publishing ROM instructions.
