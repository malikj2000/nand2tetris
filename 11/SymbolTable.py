class SymbolTable:

    def __init__(self):
        # name -> (type, kind, index)
        self.class_level_symbol_table = {}
        self.subroutine_level_symbol_table = {}
        self.field_index = 0
        self.static_index = 0
        self.argument_index = 0
        self.local_index = 0
    
    def reset(self):
        self.subroutine_level_symbol_table = {}
        self.argument_index = 0
        self.local_index = 0
    
    def define(self, name, type, kind):
        if kind == "STATIC":
            self.static_index += 1
            self.class_level_symbol_table[name] = (type, kind, self.static_index)
        elif kind == "FIELD":
            self.field_index += 1
            self.class_level_symbol_table[name] = (type, kind, self.field_index)
        elif kind == "ARG":
            self.argument_index += 1
            self.class_level_symbol_table[name] = (type, kind, self.argument_index)
        elif kind == "LOCAL":
            self.local_index += 1
            self.class_level_symbol_table[name] = (type, kind, self.local_index)
    
    def varCount(self, kind):
        if kind == "STATIC":
            return self.static_index
        elif kind == "FIELD":
            return self.field_index
        elif kind == "ARG":
            return self.argument_index
        elif kind == "LOCAL":
            return self.local_index
    
    def kindOf(self, name):
        if name not in self.class_level_symbol_table and name not in self.subroutine_level_symbol_table:
            return "NONE"
        if name in self.class_level_symbol_table:
            return self.class_level_symbol_table[name][1]
        elif name in self.subroutine_level_symbol_table:
            return self.subroutine_level_symbol_table[name][1]
    
    def typeOf(self, name):
        if name in self.class_level_symbol_table:
            return self.class_level_symbol_table[name][0]
        elif name in self.subroutine_level_symbol_table:
            return self.subroutine_level_symbol_table[name][0]
    
    def indexOf(self, name):
        if name in self.class_level_symbol_table:
            return self.class_level_symbol_table[name][2]
        elif name in self.subroutine_level_symbol_table:
            return self.subroutine_level_symbol_table[name][2]
    