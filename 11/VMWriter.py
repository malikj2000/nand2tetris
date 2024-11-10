class VMWriter:
    def __init__(self, output_file):
        self.output_file = open(output_file, "w")
    
    def writePush(self, segment, index):
        self.output_file.write(f"push {segment} {index}\n")
    
    def writePop(self, segment, index):
        self.output_file.write(f"pop {segment} {index}\n")
    
    def writeArithmetic(self, command):
        self.output_file.write(f"{command}\n")
    
    def writeLabel(self, label):
        self.output_file.write(f"label {label}\n")
    
    def writeGoto(self, label):
        self.output_file.write(f"goto {label}\n")
    
    def writeIf(self, label):
        self.output_file.write(f"if-goto {label}\n")
    
    def writeCall(self, name, nArgs):
        self.output_file.write(f"call {name} {nArgs}\n")
    
    def writeFunction(self, name, nVars):
        self.output_file.write(f"function {name} {nVars}\n")
    
    def writeReturn(self):
        self.output_file.write("return\n")
    
    def close(self):
        self.output_file.close()