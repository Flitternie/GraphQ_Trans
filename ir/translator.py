from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.ir.UnifiedIRLexer import UnifiedIRLexer
from graphq_trans.ir.UnifiedIRParser import UnifiedIRParser
from graphq_trans.ir.UnifiedIRParserListener import UnifiedIRParserListener

from graphq_trans.ir.SparqlEmitter import SparqlEmitter
from graphq_trans.ir.OvernightEmitter import OvernightEmitter, overnight_domains
from graphq_trans.ir.CypherEmitter import CypherEmitter
from graphq_trans.ir.KoplEmitter import KoplEmitter

from graphq_trans.utils import ErrorHandler


def post_process_ir(ir):
    for token in ["<E>","</E>","<ES>","</ES>","<A>","</A>","<R>","</R>","<V>","</V>","<Q>","</Q>","<C>","</C>"]:
        ir = ir.replace(" {}".format(token), token)
        ir = ir.replace("{} ".format(token), token)
    return ir        


class Translator():
    def __init__(self, ungrounded=False):
        self.sparql_emitter = SparqlEmitter()
        self.kopl_emitter = KoplEmitter()
        self.overnight_emitter = OvernightEmitter(ungrounded)
        self.cypher_emitter = CypherEmitter()
        self.walker = ParseTreeWalker() 
        self.error_listener = ErrorHandler()
    
    def set_domain(self, domain_idx):
        assert domain_idx < len(overnight_domains)
        self.overnight_emitter.set_domain(overnight_domains[domain_idx])
    
    def parse(self, input):
        input_stream = InputStream(input)
        lexer = UnifiedIRLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = UnifiedIRParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        return parser.root()

    def to_sparql(self, input):
        input = post_process_ir(input)
        tree = self.parse(input)
        self.walker.walk(self.sparql_emitter, tree)
        logical_form = self.sparql_emitter.emit(tree)
        return logical_form

    def to_kopl(self, input):
        input = post_process_ir(input)
        tree = self.parse(input)
        self.walker.walk(self.kopl_emitter, tree)
        logical_form = self.kopl_emitter.emit(tree)
        return logical_form
    
    def to_overnight(self, input, domain_idx=None):
        if domain_idx != None and self.overnight_emitter.domain != overnight_domains[domain_idx]:
            self.set_domain(domain_idx)
        tree = self.parse(input)
        self.walker.walk(self.overnight_emitter, tree)
        logical_form = self.overnight_emitter.emit(tree)
        return logical_form
    
    def to_cypher(self, input):
        tree = self.parse(input)
        self.walker.walk(self.cypher_emitter, tree)
        logical_form = self.cypher_emitter.emit(tree)
        return logical_form

    