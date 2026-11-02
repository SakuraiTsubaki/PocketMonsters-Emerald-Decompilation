    .syntax unified
    .thumb

    .equ SPECIES_PIKACHU, 25

    @ Verified RSE table layouts used by the reconstruction assets.
    .macro CompressedSpriteSheet data, size, tag
    .word \data
    .hword \size, \tag
    .endm

    .macro CompressedSpritePalette data, tag
    .word \data
    .hword \tag, 0
    .endm
