// C_PUSHargument1
@1
D=A
@ARG
A=M
D=D+A
A=D
D=M
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
// C_PUSHconstant0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPthat0
@0
D=A
@THAT
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
// C_PUSHconstant1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POPthat1
@1
D=A
@THAT
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
// C_PUSHargument0
@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHconstant2
@2
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
@0
D=A
@ARG
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
//label LOOP
(OS$LOOP)
// C_PUSHargument0
@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT
@SP
AM=M-1
D=M
@OS$COMPUTE_ELEMENT
D;JNE
//goto END
@OS$END
0;JMP
//label COMPUTE_ELEMENT
(OS$COMPUTE_ELEMENT)
// C_PUSHthat0
@0
D=A
@THAT
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSHthat1
@1
D=A
@THAT
A=M
D=D+A
A=D
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
// C_POPthat2
@2
D=A
@THAT
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
// C_PUSHpointer1
@THAT
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
// C_POPpointer1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// C_PUSHargument0
@0
D=A
@ARG
A=M
D=D+A
A=D
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
@0
D=A
@ARG
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
//goto LOOP
@OS$LOOP
0;JMP
//label END
(OS$END)
