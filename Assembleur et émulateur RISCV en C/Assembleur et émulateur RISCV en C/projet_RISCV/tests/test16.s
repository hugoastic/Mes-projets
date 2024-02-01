jal ra, 12
addi a0, zero, 42
jal ra, 8
jal ra, -8

#EXPECTED
# a0 : 42
# ra : 3
#sp : 16384
