.syntax unified
.thumb

.global RegisterRamReset
.type RegisterRamReset, %function
RegisterRamReset:
    swi 1
    bx lr
.size RegisterRamReset, . - RegisterRamReset
