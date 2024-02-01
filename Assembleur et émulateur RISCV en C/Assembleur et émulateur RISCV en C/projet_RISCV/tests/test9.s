#prog:
li t3, -50
mv s4,t3
addi t4,t3,-10
addi t5,zero,0

#loop:   
beq s4, t5, 24
addi s4,s4,10
mv t3,t4
addi t3,t3,1
add t4,t4,s4
j -20



#EXPECTED
#t3 : -159
#s4 : 0
#t4 : -160
#t5 : 0
# sp : 16384
