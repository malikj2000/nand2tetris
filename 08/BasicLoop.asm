@256
D=A
@SP
M=D
(BasicLoop.Sys.init)
// C_PUSHconstant0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPlocal0
D=0
@LCL
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
//label LOOP
(BasicLoop.Sys.init$LOOP)
// C_PUSHargument0
D=0
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHlocal0
D=0
@LCL
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
// C_POPlocal0	
@0	
D=A
@LCL
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
// C_PUSHargument0
D=0
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant1
@1
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
// C_POPargument0
D=0
@ARG
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
// C_PUSHargument0
D=0
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//if-goto LOOP
@SP
M=M-1
A=M
D=M
@TRUE0
D;JGT
@END1
0;JMP
(TRUE0)
@BasicLoop.Sys.init$LOOP
0;JMP
(END1)
// C_PUSHlocal0
D=0
@LCL
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
