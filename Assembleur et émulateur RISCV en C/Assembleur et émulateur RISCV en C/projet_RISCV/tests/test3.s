li a0, 20
li a1, 22 
li a2, 22
addi a3, zero, 1
beq a2, a1, 8
sub a2, a2, a2 
sd a2, 0(sp)


#EXPECTED
#a0 : 20
#a1 : 22
#a2 : 22
#a3 : 1
# sp : 16384
