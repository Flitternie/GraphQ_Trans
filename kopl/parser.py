from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.kopl.KoplLexer import KoplLexer
from graphq_trans.kopl.KoplParser import KoplParser

from graphq_trans.utils import ErrorHandler
from graphq_trans.kopl.utils import get_program_seq

class Parser():
    def __init__(self):
        self.walker = ParseTreeWalker() 
        self.error_listener = ErrorHandler()

    def parse(self, input):
        input = get_program_seq(input)
        input_stream = InputStream(input)
        lexer = KoplLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = KoplParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        tree = parser.root()
        lisp_tree_str = tree.toStringTree(recog=parser)

        return lisp_tree_str       
    
