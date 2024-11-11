class VMWriter:
    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, "w")
    
    def writePush(self, segment, index):
        self.output_file.write(f"push {segment} {str(index)}\n")
    
    def writePop(self, segment, index):
        self.output_file.write(f"pop {segment} {str(index)}\n")
    
    def writeArithmetic(self, command):
        self.output_file.write(f"{command}\n")
    
    def writeLabel(self, label):
        self.output_file.write(f"label {label}\n")
    
    def writeGoto(self, label):
        self.output_file.write(f"goto {label}\n")
    
    def writeIf(self, label):
        self.output_file.write(f"if-goto {label}\n")
    
    def writeCall(self, name, nArgs):
        self.output_file.write(f"call {name} {str(nArgs)}\n")
    
    def writeFunction(self, name, nVars):
        self.output_file.write(f"function {name} {str(nVars)}\n")
    
    def writeReturn(self):
        self.output_file.write("return\n")
    
    def close(self):
        self.output_file.close()