from antlr4.error.ErrorListener import ErrorListener

class ErrorHandler(ErrorListener):

    __slots__ = [ 'file_name' ]
    
    def __init__(self, file_name="<stdin>"):
        self.file_name = file_name

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"{self.file_name} {line}:{column} {msg}")

class strictDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            raise KeyError("{} is not a legal key of this strictDict".format(repr(key)))
        dict.__setitem__(self, key, value)

class entitySet(str):
    def __new__(cls, value="", is_atom=False, is_pop=False, concept=None):
        return str.__new__(cls, value)
    
    def __init__(self, value="", is_atom=False, is_pop=False, concept=None):
        self.is_atom = is_atom
        self.is_pop = is_pop
        self.concept = concept
    
    def reassign(self, value: str):
        return entitySet(value, is_atom=self.is_atom, is_pop=self.is_pop)

def insert(ctx, value, is_atom=False, is_pop=False, concept=None):
    if isinstance(ctx.slots["entitySet"], list):
        ctx.slots["entitySet"].append(entitySet(value, is_atom=is_atom, is_pop=is_pop, concept=concept))
    else:
        ctx.slots["entitySet"] = entitySet(value, is_atom=is_atom, is_pop=is_pop, concept=concept)