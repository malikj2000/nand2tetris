from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.symbol_table = SymbolTable()
        self.vmwriter = VMWriter(output_file)
        self.indentation = 0
        self.ops = {'+': "add", '-': "sub", '*': "Math.multiply", '/': "Math.divide", '&': "and", '|': "or", '>': "gt", '<': "lt", '=': "eq"}
        self.class_name = ""
        self.subroutineName = ""
        self.label_counter = 0
    
    def compileClass(self):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            # class
            self.tokenizer.advance()

            # className
            self.class_name = self.tokenizer.identifier()
            self.tokenizer.advance()

            # '{'
            self.tokenizer.advance()

            # classVarDec
            while self.tokenizer.keyword() == "static" or self.tokenizer.keyword() == "field":
                self.compileClassVarDec()

            # subroutineDec
            while self.tokenizer.keyword() == "constructor" or self.tokenizer.keyword() == "function" or self.tokenizer.keyword() == "method":
                self.compileSubroutine()

            # '}'
            self.tokenizer.advance()
            

    def compileClassVarDec(self):
        kind = type = name = ""

        # ('static' | 'field')
        if self.tokenizer.keyword() == "field":
            kind = "this"
        else:
            kind = "static"
        self.tokenizer.advance()

        # type
        if self.tokenizer.tokenType() == "KEYWORD":
            type = self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            type = self.tokenizer.identifier()
        self.tokenizer.advance()

        # varName
        name = self.tokenizer.identifier()
        self.symbol_table.define(name, type, kind)
        self.tokenizer.advance()

        # (',' varName)*
        while self.tokenizer.symbol() == ",":
            self.tokenizer.advance()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, type, kind)
            self.tokenizer.advance()
        
        # ';'
        self.tokenizer.advance()

    def compileSubroutine(self):
        self.symbol_table.reset()

        # ('constructor' | 'function' | 'method')
        subroutine_type = self.tokenizer.keyword()
        is_constructor = subroutine_type == "constructor"
        is_method = subroutine_type == "method"

        if is_method:
            self.symbol_table.define("this", self.class_name, "argument")
        self.tokenizer.advance()

        # ('void' | type)
        self.tokenizer.advance()

        # subroutineName
        self.subroutineName = self.tokenizer.identifier()
        self.tokenizer.advance()

        # '('
        self.tokenizer.advance()

        # parameterList
        self.compileParameterList()

        # ')'
        self.tokenizer.advance()

        # subroutineBody
        self.compileSubroutineBody(is_constructor, is_method)
    
    def compileParameterList(self):
        if self.tokenizer.tokenType() == "KEYWORD" or self.tokenizer.tokenType() == "IDENTIFIER":
            type = name = ""
            # type
            if self.tokenizer.tokenType() == "KEYWORD":
                type = self.tokenizer.keyword()
            elif self.tokenizer.tokenType() == "IDENTIFIER":
                type = self.tokenizer.identifier()
            self.tokenizer.advance()

            # varName
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, type, "argument")
            self.tokenizer.advance()

            # (',' type varName)*
            while self.tokenizer.symbol() == ",":
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == "KEYWORD":
                    type = self.tokenizer.keyword()
                elif self.tokenizer.tokenType() == "IDENTIFIER":
                    type = self.tokenizer.identifier()
                self.tokenizer.advance()
                name = self.tokenizer.identifier()
                self.symbol_table.define(name, type, "argument")
                self.tokenizer.advance()
    
    def compileSubroutineBody(self, is_constructor, is_method):
        # '{'
        self.tokenizer.advance()

        # varDec*
        while self.tokenizer.keyword() == "var":
            self.compileVarDec()
        
        self.vmwriter.writeFunction(f"{self.class_name}.{self.subroutineName}", self.symbol_table.varCount("local"))
        if is_constructor:
            field_count = self.symbol_table.varCount("this")
            self.vmwriter.writePush("constant", field_count)
            self.vmwriter.writeCall("Memory.alloc", 1)
            self.vmwriter.writePop("pointer", 0)
        elif is_method:
            self.vmwriter.writePush("argument", 0)
            self.vmwriter.writePop("pointer", 0)
        
        # statements
        self.compileStatements()

        # '}'
        self.tokenizer.advance()

    def compileVarDec(self):
        type = name = ""

        # 'var'
        self.tokenizer.advance()

        # type
        if self.tokenizer.tokenType() == "KEYWORD":
            type = self.tokenizer.keyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            type = self.tokenizer.identifier()
        self.tokenizer.advance()

        # varName
        name = self.tokenizer.identifier()
        self.symbol_table.define(name, type, "local")
        self.tokenizer.advance()

        # (',' varName)*
        while self.tokenizer.symbol() == ",":
            self.tokenizer.advance()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, type, "local")
            self.tokenizer.advance()
        
        # ';'
        self.tokenizer.advance()
    
    def compileStatements(self):
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

    def compileLet(self):
        # 'let'
        self.tokenizer.advance()
        array = False

        # varName
        name = self.tokenizer.identifier()
        kind = self.symbol_table.kindOf(name)
        index = self.symbol_table.indexOf(name)
        self.tokenizer.advance()

        # ('[' expression ']')
        if self.tokenizer.symbol() == "[":
            array = True
            self.tokenizer.advance()
            self.vmwriter.writePush(kind, index)
            self.compileExpression()
            self.vmwriter.writeArithmetic("add")
            self.tokenizer.advance()
        
        # '='
        self.tokenizer.advance()

        # expression
        self.compileExpression()

        if array:
            self.vmwriter.writePop("temp", 0)
            self.vmwriter.writePop("pointer", 1)
            self.vmwriter.writePush("temp", 0)
            self.vmwriter.writePop("that", 0)
        else:
            self.vmwriter.writePop(kind, index)

        # ';'
        self.tokenizer.advance()

    def compileIf(self):
        if_label = f"L{str(self.label_counter)}"
        self.label_counter += 1
        go_label = f"L{str(self.label_counter)}"
        self.label_counter += 1
        # 'if'
        self.tokenizer.advance()

        # '('
        self.tokenizer.advance()

        # expression
        self.compileExpression()

        self.vmwriter.writeArithmetic("not")

        self.vmwriter.writeIf(if_label)

        # ')'
        self.tokenizer.advance()

        # '{'
        self.tokenizer.advance()

        # statements
        self.compileStatements()

        self.vmwriter.writeGoto(go_label)
        self.vmwriter.writeLabel(if_label)

        # '}'
        self.tokenizer.advance()

        # ('else' '{' statements '}')?
        if self.tokenizer.keyword() == "else":
            self.tokenizer.advance()
            self.tokenizer.advance()
            self.compileStatements()
            self.tokenizer.advance()
        
        self.vmwriter.writeLabel(go_label)
    
    def compileWhile(self):
        go_label = f"L{self.label_counter}"
        self.label_counter += 1
        if_label = f"L{self.label_counter}"
        self.label_counter += 1

        # 'while'
        self.tokenizer.advance()

        # '('
        self.tokenizer.advance()

        self.vmwriter.writeLabel(go_label)

        # expression
        self.compileExpression()

        self.vmwriter.writeArithmetic("not")

        # ')'
        self.tokenizer.advance()

        # '{'
        self.tokenizer.advance()

        self.vmwriter.writeIf(if_label)

        # statements
        self.compileStatements()

        self.vmwriter.writeGoto(go_label)
        # '}'
        self.tokenizer.advance()

        self.vmwriter.writeLabel(if_label)
    
    def compileDo(self):
        # 'do'
        self.tokenizer.advance()

        # subroutineCall (can be treated as an expression)
        self.compileExpression()

        self.vmwriter.writePop("temp", 0)

        # ';'
        self.tokenizer.advance()

    def compileReturn(self):
        # 'return'
        self.tokenizer.advance()

        # expression?
        if self.tokenizer.tokenType() != "SYMBOL":
            self.compileExpression()
        else:
            self.vmwriter.writePush("constant", 0)
        
        self.vmwriter.writeReturn()

        # ';'
        self.tokenizer.advance()
    
    def compileExpression(self):
        # term
        self.compileTerm()

        # (op term)*
        while self.tokenizer.symbol() in self.ops:
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compileTerm()
            if op == '*':
                self.vmwriter.writeCall("Math.multiply", 2)
            elif op == "/":
                self.vmwriter.writeCall("Math.divide", 2)
            else:
                self.vmwriter.writeArithmetic(self.ops[op])
    
    def compileTerm(self):
        if self.tokenizer.tokenType() == "INT_CONST":
            self.vmwriter.writePush("constant", self.tokenizer.intVal())
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "STRING_CONST":
            string = self.tokenizer.stringVal()
            length = len(string)
            self.vmwriter.writePush("constant", length)
            self.vmwriter.writeCall("String.new", 1)
            for char in string:
                self.vmwriter.writePush("constant", ord(char))
                self.vmwriter.writeCall("String.appendChar", 2)
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "KEYWORD":
            if self.tokenizer.keyword() in ['true', 'false', 'null', 'this']:
                if self.tokenizer.keyword() == 'true':
                    self.vmwriter.writePush("constant", 1)
                    self.vmwriter.writeArithmetic("neg")
                elif self.tokenizer.keyword() == "false":
                    self.vmwriter.writePush("constant", 0)
                elif self.tokenizer.keyword() == "null":
                    self.vmwriter.writePush("constant", 0)
                elif self.tokenizer.keyword() == "this":
                    self.vmwriter.writePush("pointer", 0)
                self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "SYMBOL":
            # (expression)
            if self.tokenizer.symbol() == '(':
                # '('
                self.tokenizer.advance()

                # expression
                self.compileExpression()
                
                # ')'
                self.tokenizer.advance()
            
            # unaryOp term
            elif self.tokenizer.symbol() in ['-', '~']:
                symbol = self.tokenizer.symbol()
                # unaryOp
                self.tokenizer.advance()

                # term
                self.compileTerm()
                
                if symbol == '-':
                    self.vmwriter.writeArithmetic("neg")
                else:
                    self.vmwriter.writeArithmetic("not")
                
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            cur_token = self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "SYMBOL":
                # subroutineCall
                if self.tokenizer.symbol() == '(':
                    # subroutineName
                    # '('
                    self.tokenizer.advance()

                    # expressionList
                    count = self.compileExpressionList()

                    # ')'
                    self.tokenizer.advance()

                    self.vmwriter.writePush("pointer", 0)

                    self.vmwriter.writeCall(f"{self.class_name}.{cur_token}", count + 1)

                # (className | varName) '.' subroutineName (expressionList)
                elif self.tokenizer.symbol() == '.':
                    subroutine = ""
                    push = True
                    # className | varName
                    if self.symbol_table.kindOf(cur_token) == "NONE":
                        subroutine += cur_token
                        subroutine += "."
                        push = False
                    else:
                        subroutine += self.symbol_table.typeOf(cur_token)
                        subroutine += "."
                    
                    # '.'
                    self.tokenizer.advance()

                    # subroutineName
                    subroutine += self.tokenizer.identifier()
                    self.tokenizer.advance()

                    if push:
                        self.vmwriter.writePush(self.symbol_table.kindOf(cur_token), self.symbol_table.indexOf(cur_token))

                    # '('
                    self.tokenizer.advance()

                    # expressionList
                    count = self.compileExpressionList()

                    # ')'
                    self.tokenizer.advance()

                    if push:
                        self.vmwriter.writeCall(subroutine, count + 1)
                    else:
                        self.vmwriter.writeCall(subroutine, count)
                
                # varName '[' expression ']'
                elif self.tokenizer.symbol() == '[':
                    # varName
                    self.vmwriter.writePush(self.symbol_table.kindOf(cur_token), self.symbol_table.indexOf(cur_token))

                    # '['
                    self.tokenizer.advance()

                    # expression
                    self.compileExpression()

                    self.vmwriter.writeArithmetic("add")
                    self.vmwriter.writePop("pointer", 1)
                    self.vmwriter.writePush("that", 0)
                    # ']'
                    self.tokenizer.advance()
                
                # varName (with another symbol)
                else:
                    self.vmwriter.writePush(self.symbol_table.kindOf(cur_token), self.symbol_table.indexOf(cur_token))

            else:
                # varName
                self.vmwriter.writePush(self.symbol_table.kindOf(cur_token), self.symbol_table.indexOf(cur_token))
    
    def compileExpressionList(self):
        count = 0
        if self.tokenizer.tokenType() != "SYMBOL" or (self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.symbol() != ')'):
            self.compileExpression()
            count += 1
            while self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.symbol() == ',':
                self.tokenizer.advance()
                self.compileExpression()
                count += 1
        
        return count
    
