addi a1,zero,-20
addi a2, zero, 457

add a0, x0, a2
sub a3, a1, a2

beq a1, a2, 12
bne x1, a6, 24
blt t1, x12, 48
bge s10, x0, 12
jal ra, 20
j 400
li a5, 30
li x30,42
mv a6,x30
#test suite
addi x0,a1,-95
jal x10,12
ld a4, 0(a1)
sd a1, 8(a2)
add a4,x18,a5
