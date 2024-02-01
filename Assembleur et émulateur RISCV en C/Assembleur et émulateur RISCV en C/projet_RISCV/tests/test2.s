addi a1, zero, 20
addi a2, zero, 20
add a0, a1, a2


beq a1, a2,4
addi a1, a1, 1

bne a1, a2, 8
blt a1, a0, 8
addi a2,a2,10

sub a1,a1,a2


#EXPECTED
# a0 : 40
#a2 : 30
#a1:-9
# sp : 16384
