.syntax unified
.arm
.section .text.rom_entry, "ax", %progbits
.global rom_entry
rom_entry:
    .word 0xea00007f @ b 0x08000204 when linked at 0x08000000
