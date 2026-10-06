# DoSoftReset reconstruction

Target: BPEJ-rev0 (33f5610b9186b4add09fef68895deb00f552b997b3d133b5a961e5123506343c)

The verified Japanese `AgbMain` map calls `DoSoftReset` at 0x080008F4. A fresh Thumb trace closes at 0x08000950, observes a return, and is published without instruction halfwords. The code-only range SHA-256 is `3ef44d6129b690d136ac017c669c2dbd5c0d5ad0d95f4692b4487c3be2390f9c`; no ROM bytes are stored.

The straight-line routine disables the interrupt master switch, stops sound VSync and the scanline effect, then disables DMA channels 1, 2, and 3 through their control-high registers. This Ruby/Sapphire/Emerald-family build protects the RTC and passes the full `0xFF` reset mask to `SoftReset`.

Names were aligned with [pret/pokeemerald](https://github.com/pret/pokeemerald) at commit `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, then independently checked against this ROM's function boundary, direct-call targets, hardware addresses, and constants.

