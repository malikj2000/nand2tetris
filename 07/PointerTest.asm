// C_PUSHconstant3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPpointer0
@SP
M=M-1
A=M
D=M
@THIS
M=D
// C_PUSHconstant3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPpointer1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// C_PUSHconstant32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPthis2
@2
D=A
@THIS
A=M
D=D+A
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
// C_PUSHconstant46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPthat6
@6
D=A
@THAT
A=M
D=D+A
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
// C_PUSHpointer0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHpointer1
@THAT
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
// C_PUSHthis2
@2
D=A
@THIS
A=M
A=D+A
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
// C_PUSHthat6
@6
D=A
@THAT
A=M
A=D+A
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
