from antlr4 import *
from antlr4.InputStream import InputStream

from .OvernightLexer import OvernightLexer
from .OvernightParser import OvernightParser
from .OvernightListener import OvernightListener
from .IREmitter import IREmitter

from ..utils import ErrorHandler

class Translator():
    def __init__(self):
        self.emitter = IREmitter()
        self.walker = ParseTreeWalker()
        self.error_listener = ErrorHandler() 

    def parser(self, logical_form):
        input_stream = InputStream(logical_form)
        lexer = OvernightLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = OvernightParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        return parser.root()

    def to_ir(self, logical_form):
        tree = self.parser(logical_form)
        self.walker.walk(self.emitter, tree)
        ir = self.emitter.get_ir(tree)
        return ir

    
    