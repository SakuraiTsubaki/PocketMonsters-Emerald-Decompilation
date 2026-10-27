.syntax unified
.arm
.section .text.rom_entry, "ax", %progbits
.global RomEntry
.type RomEntry, %function
RomEntry:
    b ArmBootstrap
.size RomEntry, . - RomEntry
