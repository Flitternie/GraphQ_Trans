import os
import re
from antlr4 import *

import antlr4.tree.Tree as t

from .CypherLexer import CypherLexer
from .CypherParser import CypherParser
from .CypherParserListener import CypherParserListener

from ..utils import *
from .utils import *
from ..ir.utils import *


class IREmitter(CypherParserListener):
    def __init__(self):
        self.ir = ""

        self.skeleton = {
            "EntityQuery": "what is {}",
            "CountQuery": "how many {}",
            "AttributeQuery": "what is the attribute {} of {}",
            "PredicateQuery": "what is the relation from {} to {}",
            "VerifyQuery": "whether {}",
            "QualifierQuery": "what is the qualifier {} of {}",
        }

    def initialize(self):
        self.ir = ""

    def get_ir(self, ctx):
        return self.ir

    # Enter a parse tree produced by CypherParser#root.
    def enterRoot(self, ctx: CypherParser.RootContext):
        ctx.slots = strictDict({"var_list": [], "query_var": None, "query_attr": None})
        return super().enterRoot(ctx)

    # Exit a parse tree produced by CypherParser#root.
    def exitRoot(self, ctx: CypherParser.RootContext):
        if ctx.slots["query_attr"] == "name":
            for es in ctx.slots["var_list"]:
                if es.var == ctx.slots["query_var"]:
                    self.ir = self.skeleton["EntityQuery"].format(es.get_ir())
                    break

        return super().exitRoot(ctx)

    # Enter a parse tree produced by CypherParser#matchClause.
    def enterMatchClause(self, ctx: CypherParser.MatchClauseContext):
        ctx.slots = strictDict({"var_list": [], "constraint_table": {}})
        return super().enterMatchClause(ctx)

    # Exit a parse tree produced by CypherParser#matchClause.
    def exitMatchClause(self, ctx: CypherParser.MatchClauseContext):
        for key in ctx.slots["constraint_table"].keys():
            for i in range(len(ctx.slots["var_list"])):
                if ctx.slots["var_list"][i].var == key:
                    if ctx.slots["constraint_table"][key]["es_attr"] == "name":
                        ctx.slots["var_list"][i].set_label(ctx.slots["constraint_table"][key]["value"])
                    else:
                        ctx.slots["var_list"][i].add_related_attr(
                            ctx.slots["constraint_table"][key]["es_attr"],
                            ctx.slots["constraint_table"][key]["symOP"],
                            ctx.slots["constraint_table"][key]["value"]
                        )

        for es in ctx.slots["var_list"]:
            exist = False
            for exist_es in ctx.parentCtx.slots["var_list"]:
                if exist_es.var == es.var:
                    if exist_es.label is None:
                        exist_es.set_label(es.label)
                    if exist_es.concept is None:
                        exist_es.set_concept(es.concept)

                    for key in es.related_es.keys():
                        if key not in exist_es.related_es.keys():
                            exist_es.add_related_es(
                                es.related_es[key]["predicate"],
                                es.related_es[key]["direction"],
                                es.related_es[key]["entitySet"]
                            )
                        else:
                            pass

                    for key in es.related_attr.keys():
                        if key not in exist_es.related_attr.keys():
                            for attr, symOP, val in es.related_attr[key]:
                                exist_es.add_related_attr(attr, symOP, val)
                        else:
                            pass
                    exist = True
                    break
            if not exist:
                ctx.parentCtx.slots["var_list"].append(es)

        return super().exitMatchClause(ctx)

    # Enter a parse tree produced by CypherParser#orderByClause.
    def enterOrderByClause(self, ctx: CypherParser.OrderByClauseContext):
        return super().enterNode(ctx)

    # Exit a parse tree produced by CypherParser#orderByClause.
    def exitOrderByClause(self, ctx: CypherParser.OrderByClauseContext):
        return super().enterNode(ctx)

    # Enter a parse tree produced by CypherParser#limitClause.
    def enterLimitClause(self, ctx: CypherParser.LimitClauseContext):
        return super().enterNode(ctx)

    # Exit a parse tree produced by CypherParser#limitClause.
    def exitLimitClause(self, ctx: CypherParser.LimitClauseContext):
        return super().enterNode(ctx)

    # Enter a parse tree produced by CypherParser#path.
    def enterPath(self, ctx: CypherParser.PathContext):
        ctx.slots = strictDict({"var_table": {}})
        return super().enterPath(ctx)

    # Exit a parse tree produced by CypherParser#path.
    def exitPath(self, ctx: CypherParser.PathContext):
        paths = list(ctx.getChildren())
        previous_node_idxs = None
        edge_direction = None
        edge = None
        for i in range(len(paths)):
            if isinstance(paths[i], CypherParser.NodeContext):
                ctx.slots["var_table"][i] = EntitySet(
                    paths[i].slots["var"], paths[i].slots["name"], paths[i].slots["label"]
                )
                if previous_node_idxs is not None:
                    if edge_direction == "right":
                        ctx.slots["var_table"][previous_node_idxs].add_related_es(
                            edge, "forward", ctx.slots["var_table"][i]
                        )
                        ctx.slots["var_table"][i].add_related_es(
                            edge, "backward", ctx.slots["var_table"][previous_node_idxs]
                        )
                    elif edge_direction == "left":
                        ctx.slots["var_table"][previous_node_idxs].add_related_es(
                            edge, "backward", ctx.slots["var_table"][i]
                        )
                        ctx.slots["var_table"][i].add_related_es(
                            edge, "forward", ctx.slots["var_table"][previous_node_idxs]
                        )
                    else:
                        ctx.slots["var_table"][previous_node_idxs].add_related_es(
                            edge, "undirected", ctx.slots["var_table"][i]
                        )
                        ctx.slots["var_table"][i].add_related_es(
                            edge, "undirected", ctx.slots["var_table"][previous_node_idxs]
                        )

                previous_node_idxs = i
                edge_direction = None
                edge = None

            elif isinstance(paths[i], t.TerminalNodeImpl):
                if paths[i].getText() == "<-":
                    edge_direction = "left"
                elif paths[i].getText() == "->":
                    edge_direction = "right"
            elif isinstance(paths[i], CypherParser.RelationshipContext):
                edge = paths[i].slots["label"]
        ctx.parentCtx.slots["var_list"] = list(ctx.slots["var_table"].values())
        return super().exitPath(ctx)

    # Enter a parse tree produced by CypherParser#node.
    def enterNode(self, ctx: CypherParser.NodeContext):
        ctx.slots = strictDict({"var": None, "name": None, "label": None})
        return super().enterNode(ctx)

    # Exit a parse tree produced by CypherParser#node.
    def exitNode(self, ctx: CypherParser.NodeContext):
        return super().exitNode(ctx)

    # Enter a parse tree produced by CypherParser#nodeLabel.
    def enterNodeLabel(self, ctx: CypherParser.NodeLabelContext):
        return super().enterNodeLabel(ctx)

    # Exit a parse tree produced by CypherParser#nodeLabel.
    def exitNodeLabel(self, ctx: CypherParser.NodeLabelContext):
        return super().exitNodeLabel(ctx)

    # Enter a parse tree produced by CypherParser#nodePropertyConstraint.
    def enterNodePropertyConstraint(self, ctx: CypherParser.NodePropertyConstraintContext):
        return super().enterNodePropertyConstraint(ctx)

    # Exit a parse tree produced by CypherParser#nodePropertyConstraint.
    def exitNodePropertyConstraint(self, ctx: CypherParser.NodePropertyConstraintContext):
        return super().exitNodePropertyConstraint(ctx)

    # Enter a parse tree produced by CypherParser#relationship.
    def enterRelationship(self, ctx: CypherParser.RelationshipContext):
        ctx.slots = strictDict({"label": None})
        return super().enterRelationship(ctx)

    # Exit a parse tree produced by CypherParser#relationship.
    def exitRelationship(self, ctx: CypherParser.RelationshipContext):
        return super().exitRelationship(ctx)

    # Enter a parse tree produced by CypherParser#relationshipLabel.
    def enterRelationshipLabel(self, ctx: CypherParser.RelationshipLabelContext):
        ctx.slots = strictDict({"label": None})
        return super().enterRelationshipLabel(ctx)

    # Exit a parse tree produced by CypherParser#relationshipLabel.
    def exitRelationshipLabel(self, ctx: CypherParser.RelationshipLabelContext):
        ctx.parentCtx.slots["label"] = ctx.slots["label"]
        return super().exitRelationshipLabel(ctx)

    # Enter a parse tree produced by CypherParser#constraint.
    def enterConstraint(self, ctx: CypherParser.ConstraintContext):
        ctx.slots = strictDict({"es_var": None, "es_attr": None, "symOP": None, "value": None})
        return super().enterConstraint(ctx)

    # Exit a parse tree produced by CypherParser#constraint.
    def exitConstraint(self, ctx: CypherParser.ConstraintContext):
        assert ctx.slots["es_var"] is not None
        ctx.parentCtx.slots["constraint_table"][ctx.slots["es_var"]] = {
            "es_attr": ctx.slots["es_attr"],
            "symOP": ctx.slots["symOP"],
            "value": ctx.slots["value"]
        }
        return super().exitConstraint(ctx)

    # Enter a parse tree produced by CypherParser#symbolOP.
    def enterSymbolOP(self, ctx: CypherParser.SymbolOPContext):
        ctx.slots = strictDict({"OP": None})
        ctx.slots["OP"] = ctx.getText()
        return super().enterSymbolOP(ctx)

    # Exit a parse tree produced by CypherParser#symbolOP.
    def exitSymbolOP(self, ctx: CypherParser.SymbolOPContext):
        if isinstance(ctx.parentCtx, CypherParser.ConstraintContext):
            ctx.parentCtx.slots["symOP"] = ctx.slots["OP"]
        else:
            pass
        return super().exitSymbolOP(ctx)

    # Enter a parse tree produced by CypherParser#variable.
    def enterVariable(self, ctx: CypherParser.VariableContext):
        ctx.slots = strictDict({"string": None})
        return super().enterVariable(ctx)

    # Exit a parse tree produced by CypherParser#variable.
    def exitVariable(self, ctx: CypherParser.VariableContext):
        if isinstance(ctx.parentCtx, CypherParser.NodeContext):
            ctx.parentCtx.slots["var"] = ctx.slots["string"]
        return super().exitVariable(ctx)

    # Enter a parse tree produced by CypherParser#variableAttribute.
    def enterVariableAttribute(self, ctx: CypherParser.VariableAttributeContext):
        ctx.slots = strictDict({"var": None, "attr": None})
        return super().enterVariableAttribute(ctx)

    # Exit a parse tree produced by CypherParser#variableAttribute.
    def exitVariableAttribute(self, ctx: CypherParser.VariableAttributeContext):
        ctx.slots["var"] = list(ctx.getChildren())[0].slots["string"]
        ctx.slots["attr"] = list(ctx.getChildren())[2].slots["string"]
        if isinstance(ctx.parentCtx, CypherParser.RootContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
            ctx.parentCtx.slots["query_attr"] = ctx.slots["attr"]
        elif isinstance(ctx.parentCtx, CypherParser.ConstraintContext):
            ctx.parentCtx.slots["es_var"] = ctx.slots["var"]
            ctx.parentCtx.slots["es_attr"] = ctx.slots["attr"]
        return super().exitVariableAttribute(ctx)

    # Enter a parse tree produced by CypherParser#nodeProperty.
    def enterNodeProperty(self, ctx: CypherParser.NodePropertyContext):
        pass

    # Exit a parse tree produced by CypherParser#nodeProperty.
    def exitNodeProperty(self, ctx: CypherParser.NodePropertyContext):
        pass

    # Enter a parse tree produced by CypherParser#value.
    def enterValue(self, ctx: CypherParser.ValueContext):
        ctx.slots = strictDict({"value": None, "dtype": None})
        return super().enterValue(ctx)

    # Exit a parse tree produced by CypherParser#value.
    def exitValue(self, ctx: CypherParser.ValueContext):
        if isinstance(ctx.parentCtx, CypherParser.ConstraintContext):
            ctx.parentCtx.slots['value'] = ctx.getText()
        elif isinstance(ctx.parentCtx, CypherParser.NodePropertyContext):
            pass
        else:
            pass
        return super().exitValue(ctx)

    # Enter a parse tree produced by CypherParser#varString.
    def enterVarString(self, ctx: CypherParser.VarStringContext):
        return super().enterVarString(ctx)

    # Exit a parse tree produced by CypherParser#varString.
    def exitVarString(self, ctx: CypherParser.VarStringContext):
        if isinstance(ctx.parentCtx, CypherParser.VariableContext):
            ctx.parentCtx.slots['string'] = ctx.getText()
        elif isinstance(ctx.parentCtx, CypherParser.RelationshipLabelContext):
            ctx.parentCtx.slots['label'] = ctx.getText()
        return super().exitVarString(ctx)

    # Enter a parse tree produced by CypherParser#string.
    def enterString(self, ctx: CypherParser.StringContext):
        return super().enterString(ctx)

    # Exit a parse tree produced by CypherParser#string.
    def exitString(self, ctx: CypherParser.StringContext):
        if isinstance(ctx.parentCtx, CypherParser.ValueContext):
            ctx.parentCtx.slots['value'] = ctx.getText()
        else:
            pass
        return super().exitString(ctx)

