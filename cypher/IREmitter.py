import os
import re
from antlr4 import *

from .CypherLexer import CypherLexer
from .CypherParser import CypherParser
from .CypherParserListener import CypherParserListener

from ..utils import *


class IREmitter(CypherParserListener):
    def __init__(self):
        self.logical_form = ""

    def initialize(self):
        self.logical_form = ""

    def get_ir(self, ctx):
        return self.logical_form

    # Enter a parse tree produced by CypherParser#root.
    def enterRoot(self, ctx: CypherParser.RootContext):
        self.initialize()
        pass

    # Exit a parse tree produced by CypherParser#root.
    def exitRoot(self, ctx: CypherParser.RootContext):
        pass

    # Enter a parse tree produced by CypherParser#matchClause.
    def enterMatchClause(self, ctx: CypherParser.MatchClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#matchClause.
    def exitMatchClause(self, ctx: CypherParser.MatchClauseContext):
        pass

    # Enter a parse tree produced by CypherParser#orderByClause.
    def enterOrderByClause(self, ctx: CypherParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#orderByClause.
    def exitOrderByClause(self, ctx: CypherParser.OrderByClauseContext):
        pass

    # Enter a parse tree produced by CypherParser#limitClause.
    def enterLimitClause(self, ctx: CypherParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#limitClause.
    def exitLimitClause(self, ctx: CypherParser.LimitClauseContext):
        pass

    # Enter a parse tree produced by CypherParser#path.
    def enterPath(self, ctx: CypherParser.PathContext):
        pass

    # Exit a parse tree produced by CypherParser#path.
    def exitPath(self, ctx: CypherParser.PathContext):
        pass

    # Enter a parse tree produced by CypherParser#node.
    def enterNode(self, ctx: CypherParser.NodeContext):
        pass

    # Exit a parse tree produced by CypherParser#node.
    def exitNode(self, ctx: CypherParser.NodeContext):
        pass

    # Enter a parse tree produced by CypherParser#relationship.
    def enterRelationship(self, ctx: CypherParser.RelationshipContext):
        pass

    # Exit a parse tree produced by CypherParser#relationship.
    def exitRelationship(self, ctx: CypherParser.RelationshipContext):
        pass

    # Enter a parse tree produced by CypherParser#constraint.
    def enterConstraint(self, ctx: CypherParser.ConstraintContext):
        pass

    # Exit a parse tree produced by CypherParser#constraint.
    def exitConstraint(self, ctx: CypherParser.ConstraintContext):
        pass

    # Enter a parse tree produced by CypherParser#attribute.
    def enterAttribute(self, ctx: CypherParser.AttributeContext):
        pass

    # Exit a parse tree produced by CypherParser#attribute.
    def exitAttribute(self, ctx: CypherParser.AttributeContext):
        pass

    # Enter a parse tree produced by CypherParser#var.
    def enterVar(self, ctx: CypherParser.VarContext):
        pass

    # Exit a parse tree produced by CypherParser#var.
    def exitVar(self, ctx: CypherParser.VarContext):
        pass

    # Enter a parse tree produced by CypherParser#string.
    def enterString(self, ctx: CypherParser.StringContext):
        pass

    # Exit a parse tree produced by CypherParser#string.
    def exitString(self, ctx: CypherParser.StringContext):
        pass



