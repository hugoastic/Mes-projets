addi s0,zero, -12
addi s1,zero, 2000
add s2, s1,s0

addi a3, zero, 20
addi a4, zero, 20
add a5, a3, a4


beq a3, a4,4
addi a5, a5, 1

bne a3, a5, 8
blt a1, a0, 8
addi a4,a4,10

sub a3,a4,a5


#EXPECTED
#s0 : -12 
#s1 : 2000
#s2 : 1988
#a3 : -11
#a4 : 30
#a5 : 41
#sp : 16384
