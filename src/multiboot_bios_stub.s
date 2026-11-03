.syntax unified
.thumb

.global MultiBoot
.type MultiBoot, %function
MultiBoot:
    movs r1, 1
    swi 0x25
    bx lr
.size MultiBoot, . - MultiBoot
