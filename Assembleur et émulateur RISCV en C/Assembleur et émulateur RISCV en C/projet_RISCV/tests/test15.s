addi a0, zero, -40
addi a1, zero, -30
addi a2, zero , 20

addi sp, sp, -24
sd a2,16(sp)
sd a1, 8(sp)
sd a0, 0(sp)

ld a5, 0(sp)
ld a4, 8(sp)
ld a3, 16(sp)
ld zero, 16(sp)



#EXPECTED
#a0 : -40
#a1 : -30
#a2 : 20
#a3: 20
#a4 : -30
#a5 : -40
#sp : 16360
