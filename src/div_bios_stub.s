.syntax unified
.thumb

.global Div
.type Div, %function
Div:
    swi 0x06
    bx lr
.size Div, . - Div
