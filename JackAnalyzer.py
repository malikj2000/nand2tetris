import sys
import os

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

        
class CompilationEngine:

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = open(output_file, "w")
        self.indentation = 0
    
    def writeKeyword(self):
        self.output_file.write(" " * self.indentation + "<keyword> " + self.tokenizer.keyword() + " </keyword>\n")
    
    def writeIdentifier(self):
        self.output_file.write(" " * self.indentation + "<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
    
    def writeSymbol(self):
        self.output_file.write(" " * self.indentation + "<symbol> " + self.tokenizer.symbol() + " </symbol>\n")
    
    def compileType(self):
        if self.tokenizer.tokenType() == "KEYWORD":
            self.writeKeyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            self.writeIdentifier()

    def compileVarName(self):
        self.writeIdentifier()
    
    def compileClass(self):
        if self.tokenizer.hasMoreTokens():
            self.output_file.write("<class>\n")
            self.tokenizer.advance()

            # class
            self.indentation += 1
            self.writeKeyword()
            self.tokenizer.advance()

            # className
            self.writeIdentifier()
            self.tokenizer.advance()

            # '{'
            self.writeSymbol()
            self.tokenizer.advance()

            # classVarDec
            while self.tokenizer.keyword() == "static" or self.tokenizer.keyword() == "field":
                self.compileClassVarDec()

            # subroutineDec
            while self.tokenizer.keyword() == "constructor" or self.tokenizer.keyword() == "function" or self.tokenizer.keyword == "method":
                self.compileSubroutine()

            # '}'
            self.writeSymbol()
            self.tokenizer.advance()

            self.indentation -= 1
            self.output_file.write("</class>\n")
            

    def compileClassVarDec(self):
        self.output_file.write(" " * self.indentation + "<classVarDec>\n")
        self.indentation += 1

        # ('static' | 'field')
        self.writeKeyword()
        self.tokenizer.advance()

        # type
        self.compileType()
        self.tokenizer.advance()

        # varName
        self.compileVarName()
        self.tokenizer.advance()

        # (',' varName)*
        while self.tokenizer.symbol() == ",":
            self.writeSymbol()
            self.tokenizer.advance()
            self.writeIdentifier()
            self.tokenizer.advance()
        
        # ';'
        self.writeSymbol()
        self.tokenizer.advance()

        self.indentation -= 1
        self.output_file.write(" " * self.indentation + "</classVarDec>\n")

    def compileSubroutine(self):
        self.output_file.write(" " * self.indentation + "<subroutineDec>\n")
        self.indentation += 1

        # ('constructor' | 'function' | 'method')
        self.writeKeyword()
        self.tokenizer.advance()

        # ('void' | type)
        self.compileType()
        self.tokenizer.advance()

        # subroutineName
        self.writeIdentifier()
        self.tokenizer.advance()

        # '('
        self.writeSymbol()
        self.tokenizer.advance()

        # parameterList
        self.compileParameterList()

        # ')'
        self.writeSymbol()
        self.tokenizer.advance()

        # subroutineBody
        self.compileSubroutineBody()

        self.indentation -= 1
        self.output_file.write(" " * self.indentation + "</subroutineDec>\n")
    
    def compileParameterList(self):
        self.output_file.write(" " * self.indentation + "<parameterList>\n")
        self.indentation += 1

        if self.tokenizer.tokenType() == "KEYWORD" or self.tokenizer.tokenType() == "IDENTIFIER":
            # type
            self.compileType()
            self.tokenizer.advance()

            # varName
            self.compileVarName()
            self.tokenizer.advance()

            # (',' varName)*
            while self.tokenizer.symbol() == ",":
                self.writeSymbol()
                self.tokenizer.advance()
                self.writeIdentifier()
                self.tokenizer.advance()
        
        self.indentation -= 1
        self.output_file.write(" " * self.indentation + "</parameterList>\n")
    
    def compileSubroutineBody(self):
        self.output_file.write(" " * self.indentation + "<subroutineBody>\n")
        self.indentation += 1

        # '{'
        self.writeSymbol()
        self.tokenizer.advance()

        # varDec*
        while self.tokenizer.keyword() == "var":
            self.compileVarDec()
        
        # statements
        self.compileStatements()

        # '}'
        self.writeSymbol()
        self.tokenizer.advance()

        self.indentation -= 1
        self.output_file.write(" " * self.indentation + "</subroutineBody>\n")

    def compileVarDec(self):
        self.output_file.write(" " * self.indentation + "<varDec>\n")
        self.indentation += 1

        # 'var'
        self.writeKeyword()
        self.tokenizer.advance()

        # type
        self.compileType()
        self.tokenizer.advance()

        # varName
        self.compileVarName()
        self.tokenizer.advance()

        # (',' varName)*
        while self.tokenizer.symbol() == ",":
            self.writeSymbol()
            self.tokenizer.advance()
            self.writeIdentifier()
            self.tokenizer.advance()
        
        # ';'
        self.writeSymbol()
        self.tokenizer.advance()

        self.output_file.write(" " + self.indentation + "</varDec>\n")
    
    def compileStatements(self):
        self.output_file.write(" " + self.indentation + "<statements>\n")
        self.indentation += 1

        while self.tokenizer.tokenType() == "KEYWORD":
            if self.tokenizer.keyword() == "if":
                self.compileIf()
            elif self.tokenizer.keyword() == "let":
                self.compileLet()
            elif self.tokenizer.keyword() == "while":
                self.compileWhile()
            elif self.tokenizer.keyword() == "do":
                self.compileDo()
            elif self.tokenizer.keyword() == "return":
                self.compileReturn()
        
        self.indentation -= 1
        self.output_file.write(" " * self.indentation + "</statements>\n")
    
    
                

        

