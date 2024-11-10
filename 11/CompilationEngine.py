from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable

class CompilationEngine:

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.symbol_table = SymbolTable()
        self.output_file = open(output_file, "w")
        self.indentation = 0
        self.ops = ['+', '-', '*', '/', '&', '|', '>', '<', '=']
        self.class_name = ""
    
    def writeKeyword(self):
        self.output_file.write("  " * self.indentation + "<keyword> " + self.tokenizer.keyword() + " </keyword>\n")
    
    def writeIdentifier(self, category, index, defined_or_used):
        self.output_file.write("  " * self.indentation + f"<identifier> <{category} {str(index)} {defined_or_used}> " + self.tokenizer.identifier() + f" </{category} {index} {defined_or_used}> </identifier>\n")
    
    def writeSymbol(self):
        symbol = self.tokenizer.symbol()
        if self.tokenizer.symbol() == "<":
            symbol = "&lt;"
        elif self.tokenizer.symbol() == ">":
            symbol = "&gt;"
        elif self.tokenizer.symbol() == "&":
            symbol == "&amp;"
        self.output_file.write("  " * self.indentation + "<symbol> " + symbol + " </symbol>\n")
    
    def compileType(self):
        if self.tokenizer.tokenType() == "KEYWORD":
            self.writeKeyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            self.writeIdentifier("class", -1, "used")
    
    def compileClass(self):
        if self.tokenizer.hasMoreTokens():
            self.output_file.write("<class>\n")
            self.tokenizer.advance()

            # class
            self.indentation += 1
            self.writeKeyword()
            self.tokenizer.advance()

            # className
            self.writeIdentifier("class", -1, "defined")
            self.class_name = self.tokenizer.identifier()
            self.tokenizer.advance()

            # '{'
            self.writeSymbol()
            self.tokenizer.advance()

            # classVarDec
            while self.tokenizer.keyword() == "static" or self.tokenizer.keyword() == "field":
                self.compileClassVarDec()

            # subroutineDec
            while self.tokenizer.keyword() == "constructor" or self.tokenizer.keyword() == "function" or self.tokenizer.keyword() == "method":
                self.compileSubroutine()

            # '}'
            self.writeSymbol()
            self.tokenizer.advance()

            self.indentation -= 1
            self.output_file.write("</class>\n")
            

    def compileClassVarDec(self):
        self.output_file.write("  " * self.indentation + "<classVarDec>\n")
        self.indentation += 1
        kind = type = name = ""

        # ('static' | 'field')
        self.writeKeyword()
        kind = self.tokenizer.keyword().upper()
        self.tokenizer.advance()

        # type
        self.compileType()
        if self.tokenizer.tokenType() == "KEYWORD":
            type = self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            type = self.tokenizer.identifier()
        self.tokenizer.advance()

        # varName
        name = self.tokenizer.identifier()
        self.symbol_table.define(name, type, kind)
        self.writeIdentifier(kind, self.symbol_table.varCount(kind) - 1, "defined")
        self.tokenizer.advance()

        # (',' varName)*
        while self.tokenizer.symbol() == ",":
            self.writeSymbol()
            self.tokenizer.advance()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, type, kind)
            self.writeIdentifier(kind, self.symbol_table.varCount(kind) - 1, "defined")
            self.tokenizer.advance()
        
        # ';'
        self.writeSymbol()
        self.tokenizer.advance()

        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</classVarDec>\n")

    def compileSubroutine(self):
        self.symbol_table.reset()
        self.output_file.write("  " * self.indentation + "<subroutineDec>\n")
        self.indentation += 1

        # ('constructor' | 'function' | 'method')
        self.writeKeyword()
        if self.tokenizer.keyword() == "method":
            self.symbol_table.define("this", self.class_name, "ARG")
        self.tokenizer.advance()

        # ('void' | type)
        self.compileType()
        self.tokenizer.advance()

        # subroutineName
        self.writeIdentifier("subroutine", -1, "defined")
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
        self.output_file.write("  " * self.indentation + "</subroutineDec>\n")
    
    def compileParameterList(self):
        self.output_file.write("  " * self.indentation + "<parameterList>\n")
        self.indentation += 1

        if self.tokenizer.tokenType() == "KEYWORD" or self.tokenizer.tokenType() == "IDENTIFIER":
            type = name = ""
            # type
            if self.tokenizer.tokenType() == "KEYWORD":
                type = self.tokenizer.keyword()
            elif self.tokenizer.tokenType() == "IDENTIFIER":
                type = self.tokenizer.identifier()
            self.compileType()
            self.tokenizer.advance()

            # varName
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, type, "ARG")
            self.writeIdentifier("argument", self.symbol_table.varCount("ARG") - 1, "defined")
            self.tokenizer.advance()

            # (',' type varName)*
            while self.tokenizer.symbol() == ",":
                self.writeSymbol()
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == "KEYWORD":
                    type = self.tokenizer.keyword()
                elif self.tokenizer.tokenType() == "IDENTIFIER":
                    type = self.tokenizer.identifier()
                self.compileType()
                self.tokenizer.advance()
                name = self.tokenizer.identifier()
                self.symbol_table.define(name, type, "ARG")
                self.writeIdentifier("argument", self.symbol_table.varCount("ARG") - 1, "defined")
                self.tokenizer.advance()
        
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</parameterList>\n")
    
    def compileSubroutineBody(self):
        self.output_file.write("  " * self.indentation + "<subroutineBody>\n")
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
        self.output_file.write("  " * self.indentation + "</subroutineBody>\n")

    def compileVarDec(self):
        self.output_file.write("  " * self.indentation + "<varDec>\n")
        self.indentation += 1
        type = name = ""

        # 'var'
        self.writeKeyword()
        self.tokenizer.advance()

        # type
        self.compileType()
        if self.tokenizer.tokenType() == "KEYWORD":
            type = self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            type = self.tokenizer.identifier()
        self.tokenizer.advance()

        # varName
        name = self.tokenizer.identifier()
        self.symbol_table.define(name, type, "LOCAL")
        self.writeIdentifier("local", self.symbol_table.varCount("LOCAL") - 1, "defined")
        self.tokenizer.advance()

        # (',' varName)*
        while self.tokenizer.symbol() == ",":
            self.writeSymbol()
            self.tokenizer.advance()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, type, "LOCAL")
            self.writeIdentifier("local", self.symbol_table.varCount("LOCAL") - 1, "defined")
            self.tokenizer.advance()
        
        # ';'
        self.writeSymbol()
        self.tokenizer.advance()

        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</varDec>\n")
    
    def compileStatements(self):
        self.output_file.write("  " * self.indentation + "<statements>\n")
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
        self.output_file.write("  " * self.indentation + "</statements>\n")

    def compileLet(self):
        self.output_file.write("  " * self.indentation + "<letStatement>\n")
        self.indentation += 1

        # 'let'
        self.writeKeyword()
        self.tokenizer.advance()

        # varName
        name = self.tokenizer.identifier()
        self.writeIdentifier(self.symbol_table.kindOf(name), self.symbol_table.indexOf(name), "used")
        self.tokenizer.advance()

        # ('[' expression ']')
        if self.tokenizer.symbol() == "[":
            self.writeSymbol()
            self.tokenizer.advance()
            self.compileExpression()
            self.writeSymbol()
            self.tokenizer.advance()
        
        # '='
        self.writeSymbol()
        self.tokenizer.advance()

        # expression
        self.compileExpression()

        # ';'
        self.writeSymbol()
        self.tokenizer.advance()

        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</letStatement>\n")

    def compileIf(self):
        self.output_file.write("  " * self.indentation + "<ifStatement>\n")
        self.indentation += 1

        # 'if'
        self.writeKeyword()
        self.tokenizer.advance()

        # '('
        self.writeSymbol()
        self.tokenizer.advance()

        # expression
        self.compileExpression()

        # ')'
        self.writeSymbol()
        self.tokenizer.advance()

        # '{'
        self.writeSymbol()
        self.tokenizer.advance()

        # statements
        self.compileStatements()

        # '}'
        self.writeSymbol()
        self.tokenizer.advance()

        # ('else' '{' statements '}')?
        if self.tokenizer.keyword() == "else":
            self.writeKeyword()
            self.tokenizer.advance()
            self.writeSymbol()
            self.tokenizer.advance()
            self.compileStatements()
            self.writeSymbol()
            self.tokenizer.advance()
        
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</ifStatement>\n")
    
    def compileWhile(self):
        self.output_file.write("  " * self.indentation + "<whileStatement>\n")
        self.indentation += 1

        # 'while'
        self.writeKeyword()
        self.tokenizer.advance()

        # '('
        self.writeSymbol()
        self.tokenizer.advance()

        # expression
        self.compileExpression()

        # ')'
        self.writeSymbol()
        self.tokenizer.advance()

        # '{'
        self.writeSymbol()
        self.tokenizer.advance()

        # statements
        self.compileStatements()

        # '}'
        self.writeSymbol()
        self.tokenizer.advance()
    
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</whileStatement>\n")
    
    def compileDo(self):
        self.output_file.write("  " * self.indentation + "<doStatement>\n")
        self.indentation += 1

        # 'do'
        self.writeKeyword()
        self.tokenizer.advance()

        # subroutineCall (can be treated as an expression)
        cur_token = self.tokenizer.identifier()
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == "SYMBOL":
            # subroutineCall
            if self.tokenizer.symbol() == '(':
                # subroutineName
                self.output_file.write("  " * self.indentation + f"<identifier> <subroutine -1 used> " + cur_token + " </subroutine -1 used> </identifier>\n")

                # '('
                self.writeSymbol()
                self.tokenizer.advance()

                # expressionList
                self.compileExpressionList()

                # ')'
                self.writeSymbol()
                self.tokenizer.advance()

            # (className | varName) '.' subroutineName (expressionList)
            elif self.tokenizer.symbol() == '.':
                # className | varName
                if self.symbol_table.kindOf(cur_token) == "NONE":
                    self.output_file.write("  " * self.indentation + "<identifier> <class -1 used>" + cur_token + " </class -1 used> </identifier>\n")
                else:
                    kind = self.symbol_table.kindOf(cur_token)
                    index = self.symbol_table.indexOf(cur_token)
                    self.output_file.write("  " * self.indentation + f"<identifier> <{kind} {index} used>" + cur_token + f" </{kind} {index} used> </identifier>\n")
                
                # '.'
                self.writeSymbol()
                self.tokenizer.advance()

                # subroutineName
                self.writeIdentifier("subroutine", -1, "used")
                self.tokenizer.advance()

                # '('
                self.writeSymbol()
                self.tokenizer.advance()

                # expressionList
                self.compileExpressionList()

                # ')'
                self.writeSymbol()
                self.tokenizer.advance()

        # ';'
        self.writeSymbol()
        self.tokenizer.advance()

        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</doStatement>\n")

    def compileReturn(self):
        self.output_file.write("  " * self.indentation + "<returnStatement>\n")
        self.indentation += 1

        # 'return'
        self.writeKeyword()
        self.tokenizer.advance()

        # expression?
        if self.tokenizer.tokenType() != "SYMBOL":
            self.compileExpression()
        
        # ';'
        self.writeSymbol()
        self.tokenizer.advance()

        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</returnStatement>\n")
    
    def compileExpression(self):
        self.output_file.write("  " * self.indentation + "<expression>\n")
        self.indentation += 1

        # term
        self.compileTerm()

        # (op term)*
        while self.tokenizer.symbol() in self.ops:
            self.writeSymbol()
            self.tokenizer.advance()
            self.compileTerm()
        
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</expression>\n")
    
    def compileTerm(self):
        self.output_file.write("  " * self.indentation + "<term>\n")
        self.indentation += 1

        if self.tokenizer.tokenType() == "INT_CONST":
            self.output_file.write("  " * self.indentation + "<integerConstant> " + str(self.tokenizer.intVal()) + " </integerConstant>\n")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "STRING_CONST":
            self.output_file.write("  " * self.indentation + "<stringConstant> " + self.tokenizer.stringVal() + " </stringConstant>\n")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "KEYWORD":
            if self.tokenizer.keyword() in ['true', 'false', 'null', 'this']:
                self.writeKeyword()
                self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "SYMBOL":
            # (expression)
            if self.tokenizer.symbol() == '(':
                # '('
                self.writeSymbol()
                self.tokenizer.advance()

                # expression
                self.compileExpression()
                
                # ')'
                self.writeSymbol()
                self.tokenizer.advance()
            
            # unaryOp term
            elif self.tokenizer.symbol() in ['-', '~']:
                # unaryOp
                self.writeSymbol()
                self.tokenizer.advance()

                # term
                self.compileTerm()
                
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            cur_token = self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "SYMBOL":
                # subroutineCall
                if self.tokenizer.symbol() == '(':
                    # subroutineName
                    self.output_file.write("  " * self.indentation + "<identifier> <subroutine -1 used> " + cur_token + " </subroutine -1 used> </identifier>\n")

                    # '('
                    self.writeSymbol()
                    self.tokenizer.advance()

                    # expressionList
                    self.compileExpressionList()

                    # ')'
                    self.writeSymbol()
                    self.tokenizer.advance()

                # (className | varName) '.' subroutineName (expressionList)
                elif self.tokenizer.symbol() == '.':
                    # className | varName
                    if self.symbol_table.kindOf(cur_token) == "NONE":
                        self.output_file.write("  " * self.indentation + "<identifier> <class -1 used>" + cur_token + " </class -1 used> </identifier>\n")
                    else:
                        kind = self.symbol_table.kindOf(cur_token)
                        index = self.symbol_table.indexOf(cur_token)
                        self.output_file.write("  " * self.indentation + f"<identifier> <{kind} {index} used>" + cur_token + f" </{kind} {index} used> </identifier>\n")
                    
                    # '.'
                    self.writeSymbol()
                    self.tokenizer.advance()

                    # subroutineName
                    self.writeIdentifier("subroutine", -1, "used")
                    self.tokenizer.advance()

                    # '('
                    self.writeSymbol()
                    self.tokenizer.advance()

                    # expressionList
                    self.compileExpressionList()

                    # ')'
                    self.writeSymbol()
                    self.tokenizer.advance()
                
                # varName '[' expression ']'
                elif self.tokenizer.symbol() == '[':
                    # varName
                    kind = self.symbol_table.kindOf(cur_token)
                    index = self.symbol_table.indexOf(cur_token)
                    self.output_file.write("  " * self.indentation + f"<identifier> <{kind} {index} used>" + cur_token + f" </{kind} {index} used> </identifier>\n")

                    # '['
                    self.writeSymbol()
                    self.tokenizer.advance()

                    # expression
                    self.compileExpression()

                    # ']'
                    self.writeSymbol()
                    self.tokenizer.advance()
                
                # varName (with another symbol)
                else:
                    kind = self.symbol_table.kindOf(cur_token)
                    index = self.symbol_table.indexOf(cur_token)
                    self.output_file.write("  " * self.indentation + f"<identifier> <{kind} {index} used>" + cur_token + f" </{kind} {index} used> </identifier>\n")

            else:
                # varName
                kind = self.symbol_table.kindOf(cur_token)
                index = self.symbol_table.indexOf(cur_token)
                self.output_file.write("  " * self.indentation + f"<identifier> <{kind} {index} used>" + cur_token + f" </{kind} {index} used> </identifier>\n")
        
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</term>\n")
    
    def compileExpressionList(self):
        self.output_file.write("  " * self.indentation + "<expressionList>\n")
        self.indentation += 1

        count = 0
        if self.tokenizer.tokenType() != "SYMBOL" or (self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.symbol() != ')'):
            self.compileExpression()
            count += 1
            while self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.symbol() == ',':
                self.writeSymbol()
                self.tokenizer.advance()
                self.compileExpression()
                count += 1
        
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</expressionList>\n")
        return count
    
