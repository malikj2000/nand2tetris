// C_PUSHconstant17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQUAL0
D;JEQ
D=0
@END1
0;JMP
(EQUAL0)
D=-1
(END1)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQUAL2
D;JEQ
D=0
@END3
0;JMP
(EQUAL2)
D=-1
(END3)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@EQUAL4
D;JEQ
D=0
@END5
0;JMP
(EQUAL4)
D=-1
(END5)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LESS6
D;JLT
D=0
@END7
0;JMP
(LESS6)
D=-1
(END7)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LESS8
D;JLT
D=0
@END9
0;JMP
(LESS8)
D=-1
(END9)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LESS10
D;JLT
D=0
@END11
0;JMP
(LESS10)
D=-1
(END11)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@GREATER12
D;JGT
D=0
@END13
0;JMP
(GREATER12)
D=-1
(END13)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@GREATER14
D;JGT
D=0
@END15
0;JMP
(GREATER14)
D=-1
(END15)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@GREATER16
D;JGT
D=0
@END17
0;JMP
(GREATER16)
D=-1
(END17)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
// neg
@SP
M=M-1
A=M
M=-M
@SP
M=M+1
// and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D&M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D|M
@SP
A=M
M=D
@SP
M=M+1
// not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1
