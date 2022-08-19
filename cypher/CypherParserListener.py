# Generated from CypherParser.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CypherParser import CypherParser
else:
    from CypherParser import CypherParser

# This class defines a complete listener for a parse tree produced by CypherParser.
class CypherParserListener(ParseTreeListener):

    # Enter a parse tree produced by CypherParser#root.
    def enterRoot(self, ctx:CypherParser.RootContext):
        pass

    # Exit a parse tree produced by CypherParser#root.
    def exitRoot(self, ctx:CypherParser.RootContext):
        pass


    # Enter a parse tree produced by CypherParser#queryBlock.
    def enterQueryBlock(self, ctx:CypherParser.QueryBlockContext):
        pass

    # Exit a parse tree produced by CypherParser#queryBlock.
    def exitQueryBlock(self, ctx:CypherParser.QueryBlockContext):
        pass


    # Enter a parse tree produced by CypherParser#matchClause.
    def enterMatchClause(self, ctx:CypherParser.MatchClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#matchClause.
    def exitMatchClause(self, ctx:CypherParser.MatchClauseContext):
        pass


    # Enter a parse tree produced by CypherParser#returnClause.
    def enterReturnClause(self, ctx:CypherParser.ReturnClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#returnClause.
    def exitReturnClause(self, ctx:CypherParser.ReturnClauseContext):
        pass


    # Enter a parse tree produced by CypherParser#specialQuery.
    def enterSpecialQuery(self, ctx:CypherParser.SpecialQueryContext):
        pass

    # Exit a parse tree produced by CypherParser#specialQuery.
    def exitSpecialQuery(self, ctx:CypherParser.SpecialQueryContext):
        pass


    # Enter a parse tree produced by CypherParser#queryFunction.
    def enterQueryFunction(self, ctx:CypherParser.QueryFunctionContext):
        pass

    # Exit a parse tree produced by CypherParser#queryFunction.
    def exitQueryFunction(self, ctx:CypherParser.QueryFunctionContext):
        pass


    # Enter a parse tree produced by CypherParser#orderByClause.
    def enterOrderByClause(self, ctx:CypherParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#orderByClause.
    def exitOrderByClause(self, ctx:CypherParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by CypherParser#limitClause.
    def enterLimitClause(self, ctx:CypherParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#limitClause.
    def exitLimitClause(self, ctx:CypherParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by CypherParser#path.
    def enterPath(self, ctx:CypherParser.PathContext):
        pass

    # Exit a parse tree produced by CypherParser#path.
    def exitPath(self, ctx:CypherParser.PathContext):
        pass


    # Enter a parse tree produced by CypherParser#node.
    def enterNode(self, ctx:CypherParser.NodeContext):
        pass

    # Exit a parse tree produced by CypherParser#node.
    def exitNode(self, ctx:CypherParser.NodeContext):
        pass


    # Enter a parse tree produced by CypherParser#nodeLabel.
    def enterNodeLabel(self, ctx:CypherParser.NodeLabelContext):
        pass

    # Exit a parse tree produced by CypherParser#nodeLabel.
    def exitNodeLabel(self, ctx:CypherParser.NodeLabelContext):
        pass


    # Enter a parse tree produced by CypherParser#propertyConstraint.
    def enterPropertyConstraint(self, ctx:CypherParser.PropertyConstraintContext):
        pass

    # Exit a parse tree produced by CypherParser#propertyConstraint.
    def exitPropertyConstraint(self, ctx:CypherParser.PropertyConstraintContext):
        pass


    # Enter a parse tree produced by CypherParser#relationship.
    def enterRelationship(self, ctx:CypherParser.RelationshipContext):
        pass

    # Exit a parse tree produced by CypherParser#relationship.
    def exitRelationship(self, ctx:CypherParser.RelationshipContext):
        pass


    # Enter a parse tree produced by CypherParser#relationshipLabel.
    def enterRelationshipLabel(self, ctx:CypherParser.RelationshipLabelContext):
        pass

    # Exit a parse tree produced by CypherParser#relationshipLabel.
    def exitRelationshipLabel(self, ctx:CypherParser.RelationshipLabelContext):
        pass


    # Enter a parse tree produced by CypherParser#constraint.
    def enterConstraint(self, ctx:CypherParser.ConstraintContext):
        pass

    # Exit a parse tree produced by CypherParser#constraint.
    def exitConstraint(self, ctx:CypherParser.ConstraintContext):
        pass


    # Enter a parse tree produced by CypherParser#alias.
    def enterAlias(self, ctx:CypherParser.AliasContext):
        pass

    # Exit a parse tree produced by CypherParser#alias.
    def exitAlias(self, ctx:CypherParser.AliasContext):
        pass


    # Enter a parse tree produced by CypherParser#symbolOP.
    def enterSymbolOP(self, ctx:CypherParser.SymbolOPContext):
        pass

    # Exit a parse tree produced by CypherParser#symbolOP.
    def exitSymbolOP(self, ctx:CypherParser.SymbolOPContext):
        pass


    # Enter a parse tree produced by CypherParser#logicOP.
    def enterLogicOP(self, ctx:CypherParser.LogicOPContext):
        pass

    # Exit a parse tree produced by CypherParser#logicOP.
    def exitLogicOP(self, ctx:CypherParser.LogicOPContext):
        pass


    # Enter a parse tree produced by CypherParser#variable.
    def enterVariable(self, ctx:CypherParser.VariableContext):
        pass

    # Exit a parse tree produced by CypherParser#variable.
    def exitVariable(self, ctx:CypherParser.VariableContext):
        pass


    # Enter a parse tree produced by CypherParser#variableAttribute.
    def enterVariableAttribute(self, ctx:CypherParser.VariableAttributeContext):
        pass

    # Exit a parse tree produced by CypherParser#variableAttribute.
    def exitVariableAttribute(self, ctx:CypherParser.VariableAttributeContext):
        pass


    # Enter a parse tree produced by CypherParser#nodeOrRelationshipProperty.
    def enterNodeOrRelationshipProperty(self, ctx:CypherParser.NodeOrRelationshipPropertyContext):
        pass

    # Exit a parse tree produced by CypherParser#nodeOrRelationshipProperty.
    def exitNodeOrRelationshipProperty(self, ctx:CypherParser.NodeOrRelationshipPropertyContext):
        pass


    # Enter a parse tree produced by CypherParser#value.
    def enterValue(self, ctx:CypherParser.ValueContext):
        pass

    # Exit a parse tree produced by CypherParser#value.
    def exitValue(self, ctx:CypherParser.ValueContext):
        pass


    # Enter a parse tree produced by CypherParser#varString.
    def enterVarString(self, ctx:CypherParser.VarStringContext):
        pass

    # Exit a parse tree produced by CypherParser#varString.
    def exitVarString(self, ctx:CypherParser.VarStringContext):
        pass


    # Enter a parse tree produced by CypherParser#string.
    def enterString(self, ctx:CypherParser.StringContext):
        pass

    # Exit a parse tree produced by CypherParser#string.
    def exitString(self, ctx:CypherParser.StringContext):
        pass



del CypherParser