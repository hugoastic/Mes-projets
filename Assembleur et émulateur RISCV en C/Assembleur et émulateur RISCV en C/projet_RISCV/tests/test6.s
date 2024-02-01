li x5,20
li x6,20
li x20,40

addi sp,sp,-24
sd x5,16(sp)
sd x6,8(sp)
sd x20,0(sp)

add x15,x6,x5


ld t1,0(sp)
ld t2,8(sp)
ld t3,16(sp)
addi sp,sp,24

#EXPECTED
#x5 : 20
#x6 : 20
#x20 : 40
#x15 : 40
#t1 : 40
#t2 : 20
#t3 : 20
#sp : 16384
