@256
D=A
@SP
M=D
//call Sys.init0
@OS$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(OS$ret.0)
// C_PUSHargument1
@1
D=A
@ARG
A=M
A=D+A
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
D=0
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
// C_PUSHconstant2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub                     // since 2 elements were already computed.
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
//label LOOP
(OS$LOOP)
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
//if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@TRUE0
D;JLT
@END1
0;JMP
(TRUE0)
@OS$COMPUTE_ELEMENT
0;JMP
(END1)
//goto END
@OS$END
0;JMP
//label COMPUTE_ELEMENT
(OS$COMPUTE_ELEMENT)
// C_PUSHthat0
D=0
@THAT
A=M
A=D+A
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
// C_POPthat2
@2
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
//goto LOOP
@OS$LOOP
0;JMP
//label END
(OS$END)
