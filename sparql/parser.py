from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.sparql.SparqlLexer import SparqlLexer
from graphq_trans.sparql.SparqlParser import SparqlParser

from graphq_trans.utils import ErrorHandler


class Parser():
    def __init__(self):
        self.walker = ParseTreeWalker() 
        self.error_listener = ErrorHandler()

    def parse(self, input):
        input_stream = InputStream(input)
        lexer = SparqlLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = SparqlParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        tree = parser.root()
        lisp_tree_str = tree.toStringTree(recog=parser)

        return lisp_tree_str
        

