#loop_start:
li t1,5

addi s5, s5, 1 
bge s5, t1, 60

addi s6, s6,1
bge s6,t1, 48

addi s7, s7,1
bge s7,t1, 36

addi s8,s8, 1
bge s8, t1, 24

addi s9,s9, 1
bge s9,t1, 12

j -40

#EXPECTED
#s5 : 5 
#s6 : 4
#s7 : 4
#s8 : 4
#s9 : 4
#t1 : 5
# sp : 16384
