#start:
li a0, 1042
li a1, 666
jal ra, 4

#max:
bge a0, a1, 8
add a2, zero, a1
add a2 , zero , a0



#EXPECTED
# a0 : 1042
# a1 : 666
# a2 : 1042
# ra : 3
# sp : 16384
