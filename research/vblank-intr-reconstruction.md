# BPEJ revision 0 VBlank interrupt

Emerald's handler selects RFU or wired-link VSync, maintains both main VBlank
counters and an optional saturating Trainer Hill counter, dispatches the
callback, flushes buffered GPU and DMA3 work, then services audio and incoming
link-battle data. RNG advances unless an active battle has one of the recorded,
link, or Frontier-related flags represented by mask `0x013F0102`.

The final wireless-indicator update and dual VBlank acknowledgments are also
preserved. The map records exact Japanese calls, globals, range hash, and the
`gMain.inBattle` offset without publishing ROM instruction bytes.
