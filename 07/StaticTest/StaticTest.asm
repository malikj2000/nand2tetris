@256
D=A
@SP
M=D
(StaticTest.Sys.init)
// C_PUSHconstant111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPstatic8
@SP
M=M-1
A=M
D=M
@StaticTest.8
M=D
// C_POPstatic3
@SP
M=M-1
A=M
D=M
@StaticTest.3
M=D
// C_POPstatic1
@SP
M=M-1
A=M
D=M
@StaticTest.1
M=D
// C_PUSHstatic3
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHstatic1
@StaticTest.1
D=M
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
// C_PUSHstatic8
@StaticTest.8
D=M
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
