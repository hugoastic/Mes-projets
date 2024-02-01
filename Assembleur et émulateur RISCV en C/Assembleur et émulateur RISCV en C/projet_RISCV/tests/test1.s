addi a1, zero, -20
addi a2, zero, 22
add a0, a1, a2
sub a3, a1, a2

#EXPECTED
# a1 : -20
# a2 : 22
# a0 : 2
# a3 : -42
# sp : 16384
