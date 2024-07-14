class JackTokenizer:

    def __init__(self, input_file):
        self.input_file = open(input_file, "r")
        self.current_token = ""
        self.keywords = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
        self.symbols = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}

    def hasMoreTokens(self):
        cur_pos = self.input_file.tell()
        does_it = bool(self.input_file.read(1))
        self.input_file.seek(cur_pos)
        return does_it
    
    def advance(self):
        while self.hasMoreTokens():
            char = self.input_file.read(1)
            
            # Skip whitespace
            if char.isspace():
                continue
            
            # Handle single-line comments
            if char == '/':
                next_char = self.input_file.read(1)
                if next_char == '/':
                    self.input_file.readline()
                    continue
                elif next_char == '*':
                    # Handle multi-line comments
                    while True:
                        next_char = self.input_file.read(1)
                        if next_char == '*' and self.input_file.read(1) == '/':
                            break
                    continue
                else:
                    self.input_file.seek(self.input_file.tell() - 1)
            
            if char in self.symbols:
                self.current_token = char
                return
            
            running_token = ""
            if char == '\"':
                running_token += char
                while True:
                    char = self.input_file.read(1)
                    running_token += char
                    if char == '\"':
                        break
                self.current_token = running_token
                return

            while char and not char.isspace() and char not in self.symbols:
                running_token += char
                char = self.input_file.read(1)

            if char in self.symbols:
                self.input_file.seek(self.input_file.tell() - 1)

            self.current_token = running_token.strip()
            return
    
    def tokenType(self):
        if self.current_token in self.keywords:
            return "KEYWORD"
        elif self.current_token in self.symbols:
            return "SYMBOL"
        elif self.current_token.isdecimal():
            return "INT_CONST"
        elif self.current_token[0] == "\"":
            return "STRING_CONST"
        else:
            return "IDENTIFIER"
    
    def keyword(self):
        if self.tokenType() == "KEYWORD":
            return self.current_token
    
    def symbol(self):
        if self.tokenType() == "SYMBOL":
            return self.current_token
    
    def identifier(self):
        if self.tokenType() == "IDENTIFIER":
            return self.current_token
    
    def intVal(self):
        if self.tokenType() == "INT_CONST":
            return int(self.current_token)
    
    def stringVal(self):
        if self.tokenType() == "STRING_CONST":
            return self.current_token[1:-1]
