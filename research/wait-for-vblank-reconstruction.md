# WaitForVBlank reconstruction

Target: BPEJ-rev0 (33f5610b9186b4add09fef68895deb00f552b997b3d133b5a961e5123506343c)

The already verified Japanese `AgbMain` map calls `WaitForVBlank` at 0x080008AC. A fresh conservative Thumb trace terminates at 0x080008D4, observes a return, and is published without instruction halfwords. The code-only ROM range SHA-256 is `a76d461ef38542e453f177d865ed0be60c4cbca398e3ff02657adee9bcbb520a`; no ROM bytes are stored.

The function clears bit 0 of `gMain.intrCheck` at the proven offset `0x1C` before waiting. This build polls the volatile flag until the VBlank interrupt handler sets it. The corresponding `VBlankIntr` reconstruction independently shows that the handler sets the same flag, closing the producer/consumer relationship.

Names were aligned with [pret/pokeemerald](https://github.com/pret/pokeemerald) at commit `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, then checked against this ROM's addresses, control flow, literals, and state accesses. The upstream project is a naming reference, not a substitute for the local ROM evidence.

