addi a0, zero, 42
sd a0, -8(sp)
ld a1, -8(sp)
# EXPECTED
# sp: 16384
# a0: 42
# a1: 42
