#prog:
li a0, 20
mv s1,a0
addi t2,a0,10
addi t1,t1,0

#loop:   
beq s1, t1, 24
addi s1,s1,-5
mv a0,t2
addi a0,a0,1
add t2,t2,s1
j -20

#EXPECTED
#s1 : 0
#t2 : 60
#a0 : 61
#t1 : 0
# sp : 16384
