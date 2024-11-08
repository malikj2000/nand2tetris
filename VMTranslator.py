import sys
import os

class Parser():

    def __init__(self, file):
        self.file = open(file, "r")
        self.current_command = ""

    def hasMoreLines(self):
        cur_pos = self.file.tell()
        does_it = bool(self.file.readline())
        self.file.seek(cur_pos)
        return does_it
    
    def advance(self):
        while self.hasMoreLines():
            self.current_command = self.file.readline().strip()
            if not self.current_command or self.current_command[0] == '/':
                continue
            break
    
    def commandType(self):
        if self.current_command[:4] == "push":
            return "C_PUSH"
        if self.current_command[:3] == "pop":
            return "C_POP"
        if self.current_command[:5] == "label":
            return "C_LABEL"
        if self.current_command[:4] == "goto":
            return "C_GOTO"
        if self.current_command[:2] == "if":
            return "C_IF"
        if self.current_command[:8] == "function":
            return "C_FUNCTION"
        if self.current_command[:6] == "return":
            return "C_RETURN"
        if self.current_command[:4] == "call":
            return "C_CALL"
        else:
            return "C_ARITHMETIC"
    
    def arg1(self):
        if self.commandType() == "C_ARITHMETIC":
            return self.current_command
        elif self.commandType() == "C_RETURN":
            return
        else:
            current_command_split = self.current_command.split(" ")
            return current_command_split[1]
    
    def arg2(self):
        if self.commandType() == "C_PUSH" or self.commandType() == "C_POP" or self.commandType() == "C_FUNCTION" or self.commandType() == "C_CALL":
            current_command_split = self.current_command.split(" ")
            return current_command_split[2]
    

class CodeWriter():

    def __init__(self, file):
        self.file = open(file, "w")
        self.label_counter = 0
        self.label_counter2 = 0
        self.label_counter3 = 0
        self.function_name = "OS"
    
    def generate_unique_label(self, base):
        label = f"{base}{self.label_counter}"
        self.label_counter += 1
        return label
    
    def write_init(self):
        # SP = 256
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")

        # call Sys.init
        self.writeFunction("Sys.init", 0)

    def writeArithmetic(self, command):
        # pop, command, push
        # pop:
        # SP--
        # D = RAM[SP]
        # SP--
        # command:
        # D=M command D
        # push:
        # M=D
        # SP++

        self.file.write("// " + command + "\n")
        if command in ["add", "sub", "and", "or", "eq", "gt", "lt"]:
            # Pop top of the stack into D
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
            self.file.write("D=M\n")
            # Pop next element of the stack into M
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
        if command == "add":
            self.file.write("D=D+M\n")
        elif command == "sub":
            self.file.write("D=M-D\n")
        elif command == "neg":
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
            self.file.write("M=-M\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")
            return
        elif command == "eq":
            equal_label = self.generate_unique_label("EQUAL")
            end_label = self.generate_unique_label("END")
            self.file.write("D=M-D\n")
            self.file.write(f"@{equal_label}\n")
            self.file.write("D;JEQ\n")
            self.file.write("D=0\n")
            self.file.write(f"@{end_label}\n")
            self.file.write("0;JMP\n")
            self.file.write(f"({equal_label})\n")
            self.file.write("D=-1\n")
            self.file.write(f"({end_label})\n")
        elif command == "gt":
            gt_label = self.generate_unique_label("GREATER")
            end_label = self.generate_unique_label("END")
            self.file.write("D=M-D\n")
            self.file.write(f"@{gt_label}\n")
            self.file.write("D;JGT\n")
            self.file.write("D=0\n")
            self.file.write(f"@{end_label}\n")
            self.file.write("0;JMP\n")
            self.file.write(f"({gt_label})\n")
            self.file.write("D=-1\n")
            self.file.write(f"({end_label})\n")
        elif command == "lt":
            lt_label = self.generate_unique_label("LESS")
            end_label = self.generate_unique_label("END")
            self.file.write("D=M-D\n")
            self.file.write(f"@{lt_label}\n")
            self.file.write("D;JLT\n")
            self.file.write("D=0\n")
            self.file.write(f"@{end_label}\n")
            self.file.write("0;JMP\n")
            self.file.write(f"({lt_label})\n")
            self.file.write("D=-1\n")
            self.file.write(f"({end_label})\n")
        elif command == "and":
            self.file.write("D=D&M\n")
        elif command == "or":
            self.file.write("D=D|M\n")
        elif command == "not":
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
            self.file.write("M=!M\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")
            return
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
    
    def writePushPop(self, command, segment, index):
        self.file.write("// " + command + segment + index + "\n")
        if command == "C_PUSH":
            if segment == "constant":
                self.file.write("@" + index + "\n")
                self.file.write("D=A\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
                ptr = ""
                if segment == "local":
                    ptr = "LCL"
                elif segment == "argument":
                    ptr = "ARG"
                elif segment == "this":
                    ptr = "THIS"
                elif segment == "that":
                    ptr = "THAT"
                if index != "0":
                    self.file.write("@" + index + "\n")
                    self.file.write("D=A\n")
                elif index == "0":
                    self.file.write("D=0\n")
                self.file.write("@" + ptr + "\n")
                self.file.write("A=M\n")
                self.file.write("A=D+A\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "static":
                symbol = self.file.name[:self.file.name.index(".")] + "." + index
                self.file.write("@" + symbol + "\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "temp":
                self.file.write("@" + index + "\n")
                self.file.write("D=A\n")
                self.file.write("@5\n")
                self.file.write("A=D+A\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "pointer":
                if index == "0":
                    self.file.write("@THIS\n")
                    self.file.write("D=M\n")
                    self.file.write("@SP\n")
                    self.file.write("A=M\n")
                    self.file.write("M=D\n")
                    self.file.write("@SP\n")
                    self.file.write("M=M+1\n")
                elif index == "1":
                    self.file.write("@THAT\n")
                    self.file.write("D=M\n")
                    self.file.write("@SP\n")
                    self.file.write("A=M\n")
                    self.file.write("M=D\n")
                    self.file.write("@SP\n")
                    self.file.write("M=M+1\n")
        elif command == "C_POP":
            if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
                ptr = ""
                if segment == "local":
                    ptr = "LCL"
                elif segment == "argument":
                    ptr = "ARG"
                elif segment == "this":
                    ptr = "THIS"
                elif segment == "that":
                    ptr = "THAT"
                if index != "0":
                    self.file.write("@" + index + "\n")
                    self.file.write("D=A\n")
                elif index == "0":
                    self.file.write("D=0\n")
                self.file.write("@" + ptr + "\n")
                self.file.write("A=M\n")
                self.file.write("D=D+A\n")
                self.file.write("@addr\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write("@addr\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
            elif segment == "static":
                symbol = self.file.name[:self.file.name.index(".")] + "." + index
                self.file.write("@SP\nM=M-1\nA=M\nD=M\n@" + symbol + "\nM=D\n")
            elif segment == "temp":
                self.file.write("@" + index + "\n")
                self.file.write("D=A\n")
                self.file.write("@5\n")
                self.file.write("D=D+A\n")
                self.file.write("@addr\nM=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write("@addr\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
            elif segment == "pointer":
                if index == "0":
                    self.file.write("@SP\n")
                    self.file.write("M=M-1\n")
                    self.file.write("A=M\n")
                    self.file.write("D=M\n")
                    self.file.write("@THIS\n")
                    self.file.write("M=D\n")
                elif index == "1":
                    self.file.write("@SP\n")
                    self.file.write("M=M-1\n")
                    self.file.write("A=M\n")
                    self.file.write("D=M\n")
                    self.file.write("@THAT\n")
                    self.file.write("M=D\n")
    
    def writeLabel(self, label):
        self.file.write("//label " + label + "\n")
        self.file.write(f"({self.function_name}${label})\n")

    def writeGoto(self, label):
        self.file.write("//goto " + label + "\n")
        self.file.write(f"@{self.function_name}${label}\n0;JMP\n")
    
    def writeIf(self, label):
        true_label = self.generate_unique_label("TRUE")
        end_label = self.generate_unique_label("END")
        self.file.write("//if-goto " + label + "\n")
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        self.file.write(f"@{true_label}\n")
        self.file.write("D;JGT\n")
        self.file.write(f"@{end_label}\n")
        self.file.write("0;JMP\n")
        self.file.write(f"({true_label})\n")
        self.file.write(f"@{self.function_name}${label}\n")
        self.file.write("0;JMP\n")
        self.file.write(f"({end_label})\n")

    def writeFunction(self, functionName, nVars):
        self.function_name = self.file.name[:self.file.name.index(".")] + "." + functionName

        # (functionName)
        self.file.write(f"({self.function_name})\n")

        # push nVars 0 values
        for i in range(int(nVars)):
            self.file.write("@0\n")
            self.file.write("D=A\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")

    
    def writeCall(self, functionName, nArgs):
        self.file.write("//call " + functionName + nArgs + "\n")
        return_label = self.function_name + "$ret." + str(self.label_counter2)
        self.label_counter2 += 1

        # push return_label
        self.file.write("@" + return_label + "\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")

        # push LCL, ARG, THIS, THAT
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.file.write("@" + segment + "\n")
            self.file.write("D=A\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")
        
        # ARG = SP - 5 - nArgs
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n")
        self.file.write("@" + str(nArgs) + "\n")
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")

        # LCL = SP
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")

        # goto functionName
        self.file.write("@" + functionName + "\n")
        self.file.write("0;JMP\n")

        # (return_label)
        self.file.write(f"({return_label})\n")
        
    def writeReturn(self):
        endFrame_label = "endFrame" + str(self.label_counter3)
        retAddr_label = "retAddr" + str(self.label_counter3)
        self.label_counter3 += 1
        # endFrame = LCL
        self.file.write("@LCL\n")
        self.file.write("D=M\n")
        self.file.write("@" + endFrame_label + "\n")
        self.file.write("M=D\n")
        
        # retAddr = *(endFrame - 5)
        self.file.write("@" + endFrame_label + "\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n")
        self.file.write("A=D\n")
        self.file.write("D=M\n")
        self.file.write("@" + retAddr_label + "\n")
        self.file.write("M=D\n")

        # *ARG = pop()
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")

        # SP = ARG + 1
        self.file.write("@ARG\n")
        self.file.write("D=M+1\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")

        # Restore that, this, arg, and lcl segments.
        for segment in ["THAT", "THIS", "ARG", "LCL"]:
            self.file.write("@" + endFrame_label + "\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("@" + segment + "\n")
            self.file.write("M=D\n")
        
        # goto retAddr
        self.file.write("@" + retAddr_label + "\n")
        self.file.write("A=M\n")
        self.file.write("0;JMP\n")

    def close(self):
        self.file.close()

if __name__ == "__main__":
    input_files = []
    input_path = sys.argv[1]
    if os.path.isfile(input_path) and input_path[-3:] == ".vm":
        input_files.append(input_path)
        output_file_name = input_path[:-3] + ".asm"
    elif os.path.isdir(input_path):
        if input_path[-1:] == "/":
            input_path = input_path[:-1]
        for file_name in os.listdir(input_path):
            if file_name[-3:] == ".vm":
                input_files.append(input_path + "/" + file_name)
        output_file_name = input_path + ".asm"
    code_writer = CodeWriter(output_file_name)
    code_writer.write_init()

    for input_file_name in input_files:
        parser = Parser(input_file_name)
        while parser.hasMoreLines():
            parser.advance()
            if parser.commandType() == "C_POP" or parser.commandType() == "C_PUSH":
                code_writer.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())
            elif parser.commandType() == "C_ARITHMETIC":
                code_writer.writeArithmetic(parser.arg1())
            elif parser.commandType() == "C_LABEL":
                code_writer.writeLabel(parser.arg1())
            elif parser.commandType() == "C_GOTO":
                code_writer.writeGoto(parser.arg1())
            elif parser.commandType() == "C_IF":
                code_writer.writeIf(parser.arg1())
            elif parser.commandType() == "C_FUNCTION":
                code_writer.writeFunction(parser.arg1(), parser.arg2())
            elif parser.commandType() == "C_CALL":
                code_writer.writeCall(parser.arg1(), parser.arg2())
            elif parser.commandType() == "C_RETURN":
                code_writer.writeReturn()
    code_writer.close()