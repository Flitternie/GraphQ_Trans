from antlr4 import *
from antlr4.InputStream import InputStream

from .KoplLexer import KoplLexer
from .KoplParser import KoplParser
from .KoplListener import KoplListener
from .IREmitter import IREmitter

from ..utils import ErrorHandler

def get_program_seq(program):
    seq = []
    for item in program:
        func = item['function']
        inputs = item['inputs']
        seq.append(func + '(' + '<c>'.join(inputs) + ')')
    seq = '<b>'.join(seq)
    return seq

class Translator():
    def __init__(self):
        self.emitter = IREmitter()
        self.walker = ParseTreeWalker() 
        self.error_listener = ErrorHandler()
    
    def parse(self, logical_form):
        input_stream = InputStream(logical_form)
        lexer = KoplLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = KoplParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        return parser.root()

    def to_ir(self, logical_form):
        tree = self.parse(get_program_seq(logical_form))
        self.walker.walk(self.emitter, tree)
        ir = self.emitter.get_ir(tree)
        return ir
