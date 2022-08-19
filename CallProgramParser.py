from antlr4 import *
from antlr4.InputStream import InputStream

from .kopl.KoplLexer import KoplLexer
from .kopl.KoplParser import KoplParser

def get_program_seq(program):
    seq = []
    for item in program:
        func = item['function']
        inputs = item['inputs']
        seq.append(func + '(' + '<c>'.join(inputs) + ')')
    seq = '<b>'.join(seq)
    return seq

class Parser():
    def __init__(self):
        self.walker = ParseTreeWalker() 
        self.errors = []

    def parse(self, input):
        program = get_program_seq(input)
        input_stream = InputStream(program)
        lexer = KoplLexer(input_stream)       
        token_stream = CommonTokenStream(lexer)
        parser = KoplParser(token_stream)
        
        try:
            tree = parser.query()
            lisp_tree_str = tree.toStringTree(recog=parser)
        except Exception:
            self.errors.append(input)
            return None

        return lisp_tree_str        
    
