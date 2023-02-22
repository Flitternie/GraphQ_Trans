from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.kopl.KoplLexer import KoplLexer
from graphq_trans.kopl.KoplParser import KoplParser
from graphq_trans.kopl.KoplListener import KoplListener
from graphq_trans.kopl.IREmitter import IREmitter

from graphq_trans.utils import ErrorHandler
from graphq_trans.kopl.utils import get_program_seq

class Translator():
    def __init__(self):
        self.emitter = IREmitter()
        self.walker = ParseTreeWalker() 
        self.error_listener = ErrorHandler()
    
    def parse(self, input):
        input_stream = InputStream(input)
        lexer = KoplLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = KoplParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        return parser.root()

    def to_ir(self, input):
        input = get_program_seq(input) if isinstance(input, list) else input
        tree = self.parse(input)
        self.walker.walk(self.emitter, tree)
        ir = self.emitter.emit(tree)
        return ir
