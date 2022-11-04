from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.cypher.CypherLexer import CypherLexer
from graphq_trans.cypher.CypherParser import CypherParser

from graphq_trans.utils import ErrorHandler


class Parser():
    def __init__(self):
        self.walker = ParseTreeWalker() 
        self.error_listener = ErrorHandler()

    def parse(self, input):
        input_stream = InputStream(input)
        lexer = CypherLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = CypherParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        tree = parser.root()
        lisp_tree_str = tree.toStringTree(recog=parser)

        return lisp_tree_str        
    
