# EnableVCountIntrAtLine150 reconstruction

Target: BPEJ-rev0 (33f5610b9186b4add09fef68895deb00f552b997b3d133b5a961e5123506343c)

The verified Japanese `AgbMain` map calls `EnableVCountIntrAtLine150` at 0x08000594. A fresh Thumb trace closes at 0x080005BC, observes a return, and is published without instruction halfwords. The exact code-range SHA-256 is `95a2d56604eed3cfceb2533a3a5dfcc05af2c009a10368853ae1640110efa633`; no ROM bytes are stored.

The routine preserves the low byte of DISPSTAT, sets the VCount comparison field to scanline 150, enables the DISPSTAT VCount interrupt bit, and enables the VCount interrupt source. FireRed and LeafGreen share identical code; Emerald uses different helper addresses but the same verified behavior.

Names were aligned with [pret/pokeemerald](https://github.com/pret/pokeemerald) at commit `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`, then checked against this ROM's boundary, direct-call targets, constants, and data flow.

