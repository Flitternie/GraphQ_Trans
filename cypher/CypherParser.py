# Generated from CypherParser.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\34")
        buf.write("\u00a0\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\6\2\32")
        buf.write("\n\2\r\2\16\2\33\3\2\3\2\5\2 \n\2\3\2\3\2\5\2$\n\2\3\2")
        buf.write("\5\2\'\n\2\3\2\3\2\3\3\3\3\3\3\3\3\5\3/\n\3\3\4\3\4\3")
        buf.write("\4\3\5\3\5\3\5\3\6\3\6\3\6\5\6:\n\6\3\6\3\6\3\6\5\6?\n")
        buf.write("\6\3\6\3\6\3\6\5\6D\n\6\3\6\5\6G\n\6\3\6\7\6J\n\6\f\6")
        buf.write("\16\6M\13\6\3\7\3\7\5\7Q\n\7\3\7\3\7\3\7\3\7\3\7\3\7\5")
        buf.write("\7Y\n\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7a\n\7\3\7\3\7\3\7\3")
        buf.write("\7\5\7g\n\7\3\7\3\7\5\7k\n\7\3\b\3\b\5\bo\n\b\3\b\3\b")
        buf.write("\3\b\3\b\3\b\5\bv\n\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b")
        buf.write("\3\b\5\b\u0081\n\b\5\b\u0083\n\b\3\b\3\b\5\b\u0087\n\b")
        buf.write("\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\5\t\u0093\n\t")
        buf.write("\3\n\3\n\3\n\3\n\3\13\3\13\3\f\6\f\u009c\n\f\r\f\16\f")
        buf.write("\u009d\3\f\2\2\r\2\4\6\b\n\f\16\20\22\24\26\2\3\4\2\23")
        buf.write("\23\30\32\2\u00ab\2\31\3\2\2\2\4*\3\2\2\2\6\60\3\2\2\2")
        buf.write("\b\63\3\2\2\2\n\66\3\2\2\2\fj\3\2\2\2\16\u0086\3\2\2\2")
        buf.write("\20\u0092\3\2\2\2\22\u0094\3\2\2\2\24\u0098\3\2\2\2\26")
        buf.write("\u009b\3\2\2\2\30\32\5\4\3\2\31\30\3\2\2\2\32\33\3\2\2")
        buf.write("\2\33\31\3\2\2\2\33\34\3\2\2\2\34\35\3\2\2\2\35\37\7\5")
        buf.write("\2\2\36 \7\n\2\2\37\36\3\2\2\2\37 \3\2\2\2 !\3\2\2\2!")
        buf.write("#\5\24\13\2\"$\5\6\4\2#\"\3\2\2\2#$\3\2\2\2$&\3\2\2\2")
        buf.write("%\'\5\b\5\2&%\3\2\2\2&\'\3\2\2\2\'(\3\2\2\2()\7\2\2\3")
        buf.write(")\3\3\2\2\2*+\7\3\2\2+.\5\n\6\2,-\7\4\2\2-/\5\20\t\2.")
        buf.write(",\3\2\2\2./\3\2\2\2/\5\3\2\2\2\60\61\7\b\2\2\61\62\5\24")
        buf.write("\13\2\62\7\3\2\2\2\63\64\7\t\2\2\64\65\7\31\2\2\65\t\3")
        buf.write("\2\2\2\66K\5\f\7\2\679\7\23\2\28:\5\16\b\298\3\2\2\29")
        buf.write(":\3\2\2\2:;\3\2\2\2;G\7\21\2\2<>\7\22\2\2=?\5\16\b\2>")
        buf.write("=\3\2\2\2>?\3\2\2\2?@\3\2\2\2@G\7\23\2\2AC\7\23\2\2BD")
        buf.write("\5\16\b\2CB\3\2\2\2CD\3\2\2\2DE\3\2\2\2EG\7\23\2\2F\67")
        buf.write("\3\2\2\2F<\3\2\2\2FA\3\2\2\2GH\3\2\2\2HJ\5\f\7\2IF\3\2")
        buf.write("\2\2JM\3\2\2\2KI\3\2\2\2KL\3\2\2\2L\13\3\2\2\2MK\3\2\2")
        buf.write("\2NP\7\r\2\2OQ\5\26\f\2PO\3\2\2\2PQ\3\2\2\2QR\3\2\2\2")
        buf.write("RS\7\20\2\2SX\5\26\f\2TU\7\17\2\2UV\5\22\n\2VW\7\24\2")
        buf.write("\2WY\3\2\2\2XT\3\2\2\2XY\3\2\2\2YZ\3\2\2\2Z[\7\16\2\2")
        buf.write("[k\3\2\2\2\\]\7\r\2\2]`\5\26\f\2^_\7\20\2\2_a\5\26\f\2")
        buf.write("`^\3\2\2\2`a\3\2\2\2af\3\2\2\2bc\7\17\2\2cd\5\22\n\2d")
        buf.write("e\7\24\2\2eg\3\2\2\2fb\3\2\2\2fg\3\2\2\2gh\3\2\2\2hi\7")
        buf.write("\16\2\2ik\3\2\2\2jN\3\2\2\2j\\\3\2\2\2k\r\3\2\2\2ln\7")
        buf.write("\25\2\2mo\5\26\f\2nm\3\2\2\2no\3\2\2\2op\3\2\2\2pq\7\20")
        buf.write("\2\2qu\5\26\f\2rs\7\33\2\2st\7\20\2\2tv\5\26\f\2ur\3\2")
        buf.write("\2\2uv\3\2\2\2vw\3\2\2\2wx\7\26\2\2x\u0087\3\2\2\2yz\7")
        buf.write("\25\2\2z\u0082\5\26\f\2{|\7\20\2\2|\u0080\5\26\f\2}~\7")
        buf.write("\33\2\2~\177\7\20\2\2\177\u0081\5\26\f\2\u0080}\3\2\2")
        buf.write("\2\u0080\u0081\3\2\2\2\u0081\u0083\3\2\2\2\u0082{\3\2")
        buf.write("\2\2\u0082\u0083\3\2\2\2\u0083\u0084\3\2\2\2\u0084\u0085")
        buf.write("\7\26\2\2\u0085\u0087\3\2\2\2\u0086l\3\2\2\2\u0086y\3")
        buf.write("\2\2\2\u0087\17\3\2\2\2\u0088\u0089\5\22\n\2\u0089\u008a")
        buf.write("\7\27\2\2\u008a\u008b\7\f\2\2\u008b\u008c\5\26\f\2\u008c")
        buf.write("\u008d\7\f\2\2\u008d\u0093\3\2\2\2\u008e\u008f\5\22\n")
        buf.write("\2\u008f\u0090\7\27\2\2\u0090\u0091\5\26\f\2\u0091\u0093")
        buf.write("\3\2\2\2\u0092\u0088\3\2\2\2\u0092\u008e\3\2\2\2\u0093")
        buf.write("\21\3\2\2\2\u0094\u0095\5\24\13\2\u0095\u0096\7\30\2\2")
        buf.write("\u0096\u0097\5\26\f\2\u0097\23\3\2\2\2\u0098\u0099\5\26")
        buf.write("\f\2\u0099\25\3\2\2\2\u009a\u009c\t\2\2\2\u009b\u009a")
        buf.write("\3\2\2\2\u009c\u009d\3\2\2\2\u009d\u009b\3\2\2\2\u009d")
        buf.write("\u009e\3\2\2\2\u009e\27\3\2\2\2\30\33\37#&.9>CFKPX`fj")
        buf.write("nu\u0080\u0082\u0086\u0092\u009d")
        return buf.getvalue()


class CypherParser ( Parser ):

    grammarFileName = "CypherParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'MATCH'", "'WHERE'", "'RETURN'", "'WITH'", 
                     "'AS'", "'ORDER BY'", "'LIMIT'", "'DISTINCT'", "<INVALID>", 
                     "'\"'", "'('", "')'", "'{'", "':'", "'->'", "'<-'", 
                     "'-'", "'}'", "'['", "']'", "'='", "'.'", "<INVALID>", 
                     "<INVALID>", "'|'", "' '" ]

    symbolicNames = [ "<INVALID>", "Match", "Where", "Return", "With", "As", 
                      "OrderBy", "Limit", "Distinct", "WS", "SEP", "LP", 
                      "RP", "LB", "C", "TORIGHT", "TOLEFT", "UND", "RB", 
                      "LSB", "RSB", "EQUAL", "DOT", "INTEGER", "STRING_LITERAL", 
                      "OR", "SPACE" ]

    RULE_root = 0
    RULE_matchClause = 1
    RULE_orderByClause = 2
    RULE_limitClause = 3
    RULE_path = 4
    RULE_node = 5
    RULE_relationship = 6
    RULE_constraint = 7
    RULE_attribute = 8
    RULE_var = 9
    RULE_string = 10

    ruleNames =  [ "root", "matchClause", "orderByClause", "limitClause", 
                   "path", "node", "relationship", "constraint", "attribute", 
                   "var", "string" ]

    EOF = Token.EOF
    Match=1
    Where=2
    Return=3
    With=4
    As=5
    OrderBy=6
    Limit=7
    Distinct=8
    WS=9
    SEP=10
    LP=11
    RP=12
    LB=13
    C=14
    TORIGHT=15
    TOLEFT=16
    UND=17
    RB=18
    LSB=19
    RSB=20
    EQUAL=21
    DOT=22
    INTEGER=23
    STRING_LITERAL=24
    OR=25
    SPACE=26

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Return(self):
            return self.getToken(CypherParser.Return, 0)

        def var(self):
            return self.getTypedRuleContext(CypherParser.VarContext,0)


        def EOF(self):
            return self.getToken(CypherParser.EOF, 0)

        def matchClause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CypherParser.MatchClauseContext)
            else:
                return self.getTypedRuleContext(CypherParser.MatchClauseContext,i)


        def Distinct(self):
            return self.getToken(CypherParser.Distinct, 0)

        def orderByClause(self):
            return self.getTypedRuleContext(CypherParser.OrderByClauseContext,0)


        def limitClause(self):
            return self.getTypedRuleContext(CypherParser.LimitClauseContext,0)


        def getRuleIndex(self):
            return CypherParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)




    def root(self):

        localctx = CypherParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 22
                self.matchClause()
                self.state = 25 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==CypherParser.Match):
                    break

            self.state = 27
            self.match(CypherParser.Return)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==CypherParser.Distinct:
                self.state = 28
                self.match(CypherParser.Distinct)


            self.state = 31
            self.var()
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==CypherParser.OrderBy:
                self.state = 32
                self.orderByClause()


            self.state = 36
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==CypherParser.Limit:
                self.state = 35
                self.limitClause()


            self.state = 38
            self.match(CypherParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MatchClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Match(self):
            return self.getToken(CypherParser.Match, 0)

        def path(self):
            return self.getTypedRuleContext(CypherParser.PathContext,0)


        def Where(self):
            return self.getToken(CypherParser.Where, 0)

        def constraint(self):
            return self.getTypedRuleContext(CypherParser.ConstraintContext,0)


        def getRuleIndex(self):
            return CypherParser.RULE_matchClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMatchClause" ):
                listener.enterMatchClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMatchClause" ):
                listener.exitMatchClause(self)




    def matchClause(self):

        localctx = CypherParser.MatchClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_matchClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(CypherParser.Match)
            self.state = 41
            self.path()
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==CypherParser.Where:
                self.state = 42
                self.match(CypherParser.Where)
                self.state = 43
                self.constraint()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderByClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OrderBy(self):
            return self.getToken(CypherParser.OrderBy, 0)

        def var(self):
            return self.getTypedRuleContext(CypherParser.VarContext,0)


        def getRuleIndex(self):
            return CypherParser.RULE_orderByClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderByClause" ):
                listener.enterOrderByClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderByClause" ):
                listener.exitOrderByClause(self)




    def orderByClause(self):

        localctx = CypherParser.OrderByClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_orderByClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(CypherParser.OrderBy)
            self.state = 47
            self.var()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LimitClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Limit(self):
            return self.getToken(CypherParser.Limit, 0)

        def INTEGER(self):
            return self.getToken(CypherParser.INTEGER, 0)

        def getRuleIndex(self):
            return CypherParser.RULE_limitClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLimitClause" ):
                listener.enterLimitClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLimitClause" ):
                listener.exitLimitClause(self)




    def limitClause(self):

        localctx = CypherParser.LimitClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_limitClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(CypherParser.Limit)
            self.state = 50
            self.match(CypherParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def node(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CypherParser.NodeContext)
            else:
                return self.getTypedRuleContext(CypherParser.NodeContext,i)


        def UND(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.UND)
            else:
                return self.getToken(CypherParser.UND, i)

        def TORIGHT(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.TORIGHT)
            else:
                return self.getToken(CypherParser.TORIGHT, i)

        def TOLEFT(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.TOLEFT)
            else:
                return self.getToken(CypherParser.TOLEFT, i)

        def relationship(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CypherParser.RelationshipContext)
            else:
                return self.getTypedRuleContext(CypherParser.RelationshipContext,i)


        def getRuleIndex(self):
            return CypherParser.RULE_path

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPath" ):
                listener.enterPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPath" ):
                listener.exitPath(self)




    def path(self):

        localctx = CypherParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.node()
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CypherParser.TOLEFT or _la==CypherParser.UND:
                self.state = 68
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 53
                    self.match(CypherParser.UND)
                    self.state = 55
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==CypherParser.LSB:
                        self.state = 54
                        self.relationship()


                    self.state = 57
                    self.match(CypherParser.TORIGHT)
                    pass

                elif la_ == 2:
                    self.state = 58
                    self.match(CypherParser.TOLEFT)
                    self.state = 60
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==CypherParser.LSB:
                        self.state = 59
                        self.relationship()


                    self.state = 62
                    self.match(CypherParser.UND)
                    pass

                elif la_ == 3:
                    self.state = 63
                    self.match(CypherParser.UND)
                    self.state = 65
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==CypherParser.LSB:
                        self.state = 64
                        self.relationship()


                    self.state = 67
                    self.match(CypherParser.UND)
                    pass


                self.state = 70
                self.node()
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LP(self):
            return self.getToken(CypherParser.LP, 0)

        def C(self):
            return self.getToken(CypherParser.C, 0)

        def string(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CypherParser.StringContext)
            else:
                return self.getTypedRuleContext(CypherParser.StringContext,i)


        def RP(self):
            return self.getToken(CypherParser.RP, 0)

        def LB(self):
            return self.getToken(CypherParser.LB, 0)

        def attribute(self):
            return self.getTypedRuleContext(CypherParser.AttributeContext,0)


        def RB(self):
            return self.getToken(CypherParser.RB, 0)

        def getRuleIndex(self):
            return CypherParser.RULE_node

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNode" ):
                listener.enterNode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNode" ):
                listener.exitNode(self)




    def node(self):

        localctx = CypherParser.NodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_node)
        self._la = 0 # Token type
        try:
            self.state = 104
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 76
                self.match(CypherParser.LP)
                self.state = 78
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CypherParser.UND) | (1 << CypherParser.DOT) | (1 << CypherParser.INTEGER) | (1 << CypherParser.STRING_LITERAL))) != 0):
                    self.state = 77
                    self.string()


                self.state = 80
                self.match(CypherParser.C)
                self.state = 81
                self.string()
                self.state = 86
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CypherParser.LB:
                    self.state = 82
                    self.match(CypherParser.LB)
                    self.state = 83
                    self.attribute()
                    self.state = 84
                    self.match(CypherParser.RB)


                self.state = 88
                self.match(CypherParser.RP)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 90
                self.match(CypherParser.LP)
                self.state = 91
                self.string()
                self.state = 94
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CypherParser.C:
                    self.state = 92
                    self.match(CypherParser.C)
                    self.state = 93
                    self.string()


                self.state = 100
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CypherParser.LB:
                    self.state = 96
                    self.match(CypherParser.LB)
                    self.state = 97
                    self.attribute()
                    self.state = 98
                    self.match(CypherParser.RB)


                self.state = 102
                self.match(CypherParser.RP)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationshipContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LSB(self):
            return self.getToken(CypherParser.LSB, 0)

        def C(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.C)
            else:
                return self.getToken(CypherParser.C, i)

        def string(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CypherParser.StringContext)
            else:
                return self.getTypedRuleContext(CypherParser.StringContext,i)


        def RSB(self):
            return self.getToken(CypherParser.RSB, 0)

        def OR(self):
            return self.getToken(CypherParser.OR, 0)

        def getRuleIndex(self):
            return CypherParser.RULE_relationship

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationship" ):
                listener.enterRelationship(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationship" ):
                listener.exitRelationship(self)




    def relationship(self):

        localctx = CypherParser.RelationshipContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_relationship)
        self._la = 0 # Token type
        try:
            self.state = 132
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 106
                self.match(CypherParser.LSB)
                self.state = 108
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CypherParser.UND) | (1 << CypherParser.DOT) | (1 << CypherParser.INTEGER) | (1 << CypherParser.STRING_LITERAL))) != 0):
                    self.state = 107
                    self.string()


                self.state = 110
                self.match(CypherParser.C)
                self.state = 111
                self.string()
                self.state = 115
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CypherParser.OR:
                    self.state = 112
                    self.match(CypherParser.OR)
                    self.state = 113
                    self.match(CypherParser.C)
                    self.state = 114
                    self.string()


                self.state = 117
                self.match(CypherParser.RSB)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 119
                self.match(CypherParser.LSB)
                self.state = 120
                self.string()
                self.state = 128
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CypherParser.C:
                    self.state = 121
                    self.match(CypherParser.C)
                    self.state = 122
                    self.string()
                    self.state = 126
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==CypherParser.OR:
                        self.state = 123
                        self.match(CypherParser.OR)
                        self.state = 124
                        self.match(CypherParser.C)
                        self.state = 125
                        self.string()




                self.state = 130
                self.match(CypherParser.RSB)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def attribute(self):
            return self.getTypedRuleContext(CypherParser.AttributeContext,0)


        def EQUAL(self):
            return self.getToken(CypherParser.EQUAL, 0)

        def SEP(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.SEP)
            else:
                return self.getToken(CypherParser.SEP, i)

        def string(self):
            return self.getTypedRuleContext(CypherParser.StringContext,0)


        def getRuleIndex(self):
            return CypherParser.RULE_constraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstraint" ):
                listener.enterConstraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstraint" ):
                listener.exitConstraint(self)




    def constraint(self):

        localctx = CypherParser.ConstraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_constraint)
        try:
            self.state = 144
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 134
                self.attribute()
                self.state = 135
                self.match(CypherParser.EQUAL)
                self.state = 136
                self.match(CypherParser.SEP)
                self.state = 137
                self.string()
                self.state = 138
                self.match(CypherParser.SEP)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 140
                self.attribute()
                self.state = 141
                self.match(CypherParser.EQUAL)
                self.state = 142
                self.string()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var(self):
            return self.getTypedRuleContext(CypherParser.VarContext,0)


        def DOT(self):
            return self.getToken(CypherParser.DOT, 0)

        def string(self):
            return self.getTypedRuleContext(CypherParser.StringContext,0)


        def getRuleIndex(self):
            return CypherParser.RULE_attribute

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttribute" ):
                listener.enterAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttribute" ):
                listener.exitAttribute(self)




    def attribute(self):

        localctx = CypherParser.AttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_attribute)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 146
            self.var()
            self.state = 147
            self.match(CypherParser.DOT)
            self.state = 148
            self.string()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(CypherParser.StringContext,0)


        def getRuleIndex(self):
            return CypherParser.RULE_var

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar" ):
                listener.enterVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar" ):
                listener.exitVar(self)




    def var(self):

        localctx = CypherParser.VarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_var)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 150
            self.string()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.STRING_LITERAL)
            else:
                return self.getToken(CypherParser.STRING_LITERAL, i)

        def INTEGER(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.INTEGER)
            else:
                return self.getToken(CypherParser.INTEGER, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.DOT)
            else:
                return self.getToken(CypherParser.DOT, i)

        def UND(self, i:int=None):
            if i is None:
                return self.getTokens(CypherParser.UND)
            else:
                return self.getToken(CypherParser.UND, i)

        def getRuleIndex(self):
            return CypherParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)




    def string(self):

        localctx = CypherParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_string)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 152
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CypherParser.UND) | (1 << CypherParser.DOT) | (1 << CypherParser.INTEGER) | (1 << CypherParser.STRING_LITERAL))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()

                else:
                    raise NoViableAltException(self)
                self.state = 155 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,21,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





