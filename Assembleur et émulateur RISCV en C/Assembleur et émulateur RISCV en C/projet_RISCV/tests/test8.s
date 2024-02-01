li t0, -1000
li t1, 15
li t2, 1
addi a6, zero, 13
add a7, zero,a7
beq t1,t2,8
sub t2,t2,t2
sd t2, 0(sp)

#EXPECTED
#t0 : -1000
#t1 : 15
#t2 : 0
#a6 : 13
#a7 :  0
#sp : 16384
