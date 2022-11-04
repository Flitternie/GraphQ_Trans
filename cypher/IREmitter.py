import re
from antlr4 import *
import antlr4.tree.Tree as t

from graphq_trans.cypher.CypherLexer import CypherLexer
from graphq_trans.cypher.CypherParser import CypherParser
from graphq_trans.cypher.CypherParserListener import CypherParserListener

from graphq_trans.utils import *
from graphq_trans.cypher.utils import *
from graphq_trans.ir.utils import *


class IREmitter(CypherParserListener):
    def __init__(self):
        self.output = ""

        self.skeleton = {
            "EntityQuery": "what is {}",
            "CountQuery": "how many {}",
            "AttributeQuery": "what is the attribute <A> {} </A> of {}",
            "PredicateQuery": "what is the relation from {} to {}",
            "VerifyQuery": "whether {}",
            "QualifierQuery": "what is the qualifier <Q> {} </Q> of {}",
            "SelectQuery": "which one has the {} <A> {} </A> among {}"
        }

        self.symOP = {
            "=": "is",
            "<>": "is not",
            "<": "smaller than",
            ">": "larger than",
            ">=": "at least",
            "<=": "at most",
        }

    def initialize(self):
        self.output = ""

    def emit(self, ctx):
        return self.output

    # Enter a parse tree produced by CypherParser#root.
    def enterRoot(self, ctx: CypherParser.RootContext):
        self.initialize()
        ctx.slots = strictDict(
            {"var_list": [], "query_var": [], "query_attr": [], "query_func": [], "order": [], "order_var": [],
             "order_attr": [], "limit": None}
        )
        return super().enterRoot(ctx)

    # Exit a parse tree produced by CypherParser#root.
    def exitRoot(self, ctx: CypherParser.RootContext):

        if len(ctx.slots["query_var"]) > 1:
            query_attr = ctx.slots["query_attr"][0]
            for i in range(len(ctx.slots["query_attr"])):
                if ctx.slots["query_attr"][i] != query_attr:
                    raise Exception("All query attributes must be the same!")
            query_func = ctx.slots["query_func"][0]
            for i in range(len(ctx.slots["query_func"])):
                if ctx.slots["query_func"][i] != query_func:
                    raise Exception("All query functions must be the same!")
            order = ctx.slots["order"][0]
            for i in range(len(ctx.slots["order"])):
                if ctx.slots["order"][i] != order:
                    raise Exception("All returning orders must remain the same!")
            order_attr = ctx.slots["order_attr"][0]
            for i in range(len(ctx.slots["order_attr"])):
                if ctx.slots["order_attr"][i] != order_attr:
                    raise Exception("All order attributes must remain the same!")

            if query_func:
                if query_func == "count":
                    es_ir_union_list = []
                    for i in range(len(ctx.slots["var_list"])):
                        for es in ctx.slots["var_list"][i]:
                            if es.var == ctx.slots["query_var"][i]:
                                es_ir_union_list.append(es.get_ir())
                                break

                    union_es = es_ir_union_list.pop()
                    while es_ir_union_list:
                        union_es = "<ES> {} or {} </ES>".format(union_es, es_ir_union_list.pop())
                    self.output = self.skeleton["CountQuery"].format(union_es)

                elif ctx.slots["query_func"] == "isEmpty":
                    es_ir_union_list = []
                    for i in range(len(ctx.slots["var_list"])):
                        for es in ctx.slots["var_list"][i]:
                            if es.var == ctx.slots["query_var"][i]:
                                es_ir_union_list.append(es.get_ir())
                                break

                    union_es = es_ir_union_list.pop()
                    while es_ir_union_list:
                        union_es = "<ES> {} or {} </ES>".format(union_es, es_ir_union_list.pop())
                    self.output = self.skeleton["VerifyQuery"].format(union_es)

            elif query_attr == "name":
                if not order:
                    es_ir_union_list = []
                    for i in range(len(ctx.slots["var_list"])):
                        for es in ctx.slots["var_list"][i]:
                            if es.var == ctx.slots["query_var"][i]:
                                es_ir_union_list.append(es.get_ir())
                                break
                    union_es = es_ir_union_list.pop()
                    while es_ir_union_list:
                        union_es = "<ES> {} or {} </ES>".format(union_es, es_ir_union_list.pop())
                    self.output = self.skeleton["EntityQuery"].format(union_es)
                else:
                    es_ir_union_list = []
                    for i in range(len(ctx.slots["order_attr"])):
                        assert ctx.slots["order_var"][i] == ctx.slots["query_var"][i]
                    assert ctx.slots["limit"] == "1"
                    for i in range(len(ctx.slots["var_list"])):
                        for es in ctx.slots["var_list"][i]:
                            if es.var == ctx.slots["query_var"][i]:
                                es_ir_union_list.append(es.get_ir())
                                break
                    union_es = es_ir_union_list.pop()
                    while es_ir_union_list:
                        union_es = "<ES> {} or {} </ES>".format(union_es, es_ir_union_list.pop())
                    self.output = self.skeleton["SelectQuery"].format(order, order_attr, union_es)

            elif query_attr == "label":
                raise NotImplementedError("Current GraphQ IR design does not support this type of expression!")

            elif query_attr:
                es_ir_union_list4attr = []
                es_ir_union_list4qual = []
                for i in range(len(ctx.slots["var_list"])):
                    for es in ctx.slots["var_list"][i]:
                        if es.var == ctx.slots["query_var"][i]:
                            es_ir_union_list4attr.append(es.get_ir())
                            break
                        else:
                            for key in es.related_es.keys():
                                if es.related_es[key]["edge_var"] == ctx.slots["query_var"][i]:
                                    raise NotImplementedError("Current GraphQ IR design does not suppert this type of"
                                                              "expression!")
                                    break
                assert not all([es_ir_union_list4attr, es_ir_union_list4qual])
                if len(es_ir_union_list4attr):
                    union_es = es_ir_union_list4attr.pop()
                    while es_ir_union_list4attr:
                        union_es = "<ES> {} or {} </ES>".format(union_es, es_ir_union_list4attr.pop())
                    self.output = self.skeleton["AttributeQuery"].format(query_attr, union_es)
                else:
                    union_es = es_ir_union_list4qual.pop()
                    while es_ir_union_list4qual:
                        union_es = "<ES> {} or {} </ES>".format(union_es, es_ir_union_list4qual.pop())
                    self.output = self.skeleton["QualifierQuery"].format(query_attr, union_es)
            else:
                pass
        else:
            ctx.slots["var_list"] = ctx.slots["var_list"][0]
            ctx.slots["query_var"] = ctx.slots["query_var"][0]
            ctx.slots["query_attr"] = ctx.slots["query_attr"][0]
            ctx.slots["query_func"] = ctx.slots["query_func"][0]
            ctx.slots["order"] = ctx.slots["order"][0]
            ctx.slots["order_var"] = ctx.slots["order_var"][0]
            ctx.slots["order_attr"] = ctx.slots["order_attr"][0]

            if ctx.slots["query_func"]:
                if ctx.slots["query_func"] == "count":
                    for es in ctx.slots["var_list"]:
                        if es.var == ctx.slots["query_var"]:
                            self.output = self.skeleton["CountQuery"].format(es.get_ir())
                            break
                elif ctx.slots["query_func"] == "isEmpty":
                    for es in ctx.slots["var_list"]:
                        if es.var == ctx.slots["query_var"]:
                            self.output = self.skeleton["VerifyQuery"].format(es.get_ir())
                            break
            elif ctx.slots["query_attr"] == "name":
                if not ctx.slots["order"]:
                    for es in ctx.slots["var_list"]:
                        if es.var == ctx.slots["query_var"]:
                            self.output = self.skeleton["EntityQuery"].format(es.get_ir())
                            break
                else:
                    assert ctx.slots["order_var"] == ctx.slots["query_var"]
                    assert ctx.slots["limit"] == "1"
                    for es in ctx.slots["var_list"]:
                        if es.var == ctx.slots["query_var"]:
                            self.output = self.skeleton["SelectQuery"].format(
                                ctx.slots["order"], ctx.slots["order_attr"], es.get_ir()
                            )
                            break
            elif ctx.slots["query_attr"] == "label":
                for es in ctx.slots["var_list"]:
                    for key in es.related_es.keys():
                        if es.related_es[key]["edge_var"] == ctx.slots["query_var"]:
                            head_es = es
                            tail_es = es.related_es[key]["entitySet"]
                            self.output = self.skeleton["PredicateQuery"].format(
                                head_es.get_ir([tail_es]), tail_es.get_ir([head_es])
                            )
                            break
                    else:
                        continue
                    break

            elif ctx.slots["query_attr"]:
                for es in ctx.slots["var_list"]:
                    if es.var == ctx.slots["query_var"]:
                        self.output = self.skeleton["AttributeQuery"].format(ctx.slots["query_attr"], es.get_ir())
                        break
                    else:
                        for key in es.related_es.keys():
                            if es.related_es[key]["edge_var"] == ctx.slots["query_var"]:
                                self.output = self.skeleton["QualifierQuery"].format(
                                    ctx.slots["query_attr"], es.get_ir()
                                )
                                break
            else:
                pass

        return super().exitRoot(ctx)

    # Enter a parse tree produced by CypherParser#queryBlock.
    def enterQueryBlock(self, ctx: CypherParser.QueryBlockContext):
        ctx.slots = strictDict({"query_var": "", "query_attr": "", "order_var": "", "order_attr": "", "var_list": [],
                                "order": "", "query_func": ""})
        return super().enterQueryBlock(ctx)

    # Exit a parse tree produced by CypherParser#queryBlock.
    def exitQueryBlock(self, ctx: CypherParser.QueryBlockContext):
        ctx.parentCtx.slots["query_var"].append(ctx.slots["query_var"])
        ctx.parentCtx.slots["query_attr"].append(ctx.slots["query_attr"])
        ctx.parentCtx.slots["var_list"].append(ctx.slots["var_list"])
        ctx.parentCtx.slots["order_var"].append(ctx.slots["order_var"])
        ctx.parentCtx.slots["order_attr"].append(ctx.slots["order_attr"])
        ctx.parentCtx.slots["order"].append(ctx.slots["order"])
        ctx.parentCtx.slots["query_func"].append(ctx.slots["query_func"])
        return super().exitQueryBlock(ctx)

    # Enter a parse tree produced by CypherParser#matchClause.
    def enterMatchClause(self, ctx: CypherParser.MatchClauseContext):
        ctx.slots = strictDict({"var_list": [], "constraint_table": {}})
        return super().enterMatchClause(ctx)

    # Exit a parse tree produced by CypherParser#matchClause.
    def exitMatchClause(self, ctx: CypherParser.MatchClauseContext):

        # Attaching constraints
        for key in ctx.slots["constraint_table"].keys():
            for i in range(len(ctx.slots["var_list"])):
                if ctx.slots["var_list"][i].var == key:
                    # attach to entitySet as attribute constraint
                    for constraint_dict in ctx.slots["constraint_table"][key]:
                        if constraint_dict["attr"] == "name":
                            ctx.slots["var_list"][i].set_label(constraint_dict["value"])
                        else:
                            ctx.slots["var_list"][i].add_related_attr(
                                constraint_dict["attr"],
                                constraint_dict["symOP"],
                                constraint_dict["value_type"],
                                constraint_dict["value"]
                            )
                else:
                    for es in ctx.slots["var_list"][i].related_es.keys():
                        if ctx.slots["var_list"][i].related_es[es]["edge_var"] == key:
                            # attach to predicate as qualifier constraint
                            for constraint_dict in ctx.slots["constraint_table"][key]:
                                ctx.slots["var_list"][i].related_es[es]["qualifier"].append(
                                    constraint_dict["attr"],
                                    constraint_dict["symOP"],
                                    constraint_dict["value_type"],
                                    constraint_dict["value"]
                                )

        # merging the EntitySets with the parent node
        for es in ctx.slots["var_list"]:
            exist = False
            for exist_es in ctx.parentCtx.slots["var_list"]:
                if exist_es.var == es.var:

                    # Re-direct the pointers from this EntitySet to existed EntitySet
                    for other_es in ctx.slots["var_list"]:
                        if other_es != es and es in other_es.related_es.keys():
                            temp_dict = other_es.related_es.pop(es)
                            other_es.add_related_es(
                                temp_dict["predicate"], temp_dict["edge_var"], temp_dict["direction"], exist_es,
                                temp_dict["qualifier"]
                            )

                    if not exist_es.label:
                        exist_es.set_label(es.label)
                    if not exist_es.concept:
                        exist_es.set_concept(es.concept)

                    for key in es.related_es.keys():
                        if key not in exist_es.related_es.keys():
                            target_var = es.related_es[key]["entitySet"].var
                            target_es = es.related_es[key]["entitySet"]
                            for other_es in ctx.parentCtx.slots["var_list"]:
                                if other_es.var == target_var:
                                    target_es = other_es
                            exist_es.add_related_es(
                                es.related_es[key]["predicate"],
                                es.related_es[key]["edge_var"],
                                es.related_es[key]["direction"],
                                target_es,
                                es.related_es[key]["qualifier"]
                            )
                        else:
                            pass
                    for key in es.related_attr.keys():
                        if key not in exist_es.related_attr.keys():
                            for attr, symOP, v_type, val in es.related_attr[key]:
                                exist_es.add_related_attr(attr, symOP, v_type, val)
                        else:
                            pass
                    exist = True
                    break
            if not exist:
                ctx.parentCtx.slots["var_list"].append(es)

        return super().exitMatchClause(ctx)

    # Enter a parse tree produced by CypherParser#returnClause.
    def enterReturnClause(self, ctx: CypherParser.ReturnClauseContext):
        ctx.slots = strictDict({"var": "", "attr": "", "alias": "", "query_func": ""})
        return super().enterReturnClause(ctx)

    # Exit a parse tree produced by CypherParser#returnClause.
    def exitReturnClause(self, ctx: CypherParser.ReturnClauseContext):
        ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        ctx.parentCtx.slots["query_attr"] = ctx.slots["attr"]
        ctx.parentCtx.slots["query_func"] = ctx.slots["query_func"]
        return super().exitReturnClause(ctx)

    # Enter a parse tree produced by CypherParser#specialQuery.
    def enterSpecialQuery(self, ctx: CypherParser.SpecialQueryContext):
        ctx.slots = strictDict({"var": "", "attr": "", "query_func": ""})
        return super().enterSpecialQuery(ctx)

    # Exit a parse tree produced by CypherParser#specialQuery.
    def exitSpecialQuery(self, ctx: CypherParser.SpecialQueryContext):
        ctx.parentCtx.slots["var"] = ctx.slots["var"]
        ctx.parentCtx.slots["attr"] = ctx.slots["attr"]
        ctx.parentCtx.slots["query_func"] = ctx.slots["query_func"]
        return super().exitSpecialQuery(ctx)

    # Enter a parse tree produced by CypherParser#queryFunction.
    def enterQueryFunction(self, ctx: CypherParser.QueryFunctionContext):
        ctx.slots = strictDict({"query_func": ctx.getText()})
        return super().enterQueryFunction(ctx)

    # Exit a parse tree produced by CypherParser#queryFunction.
    def exitQueryFunction(self, ctx: CypherParser.QueryFunctionContext):
        ctx.parentCtx.slots["query_func"] = ctx.slots["query_func"]
        return super().exitQueryFunction(ctx)

    # Enter a parse tree produced by CypherParser#orderByClause.
    def enterOrderByClause(self, ctx: CypherParser.OrderByClauseContext):
        ctx.slots = strictDict({"var": "", "attr": ""})
        return super().enterNode(ctx)

    # Exit a parse tree produced by CypherParser#orderByClause.
    def exitOrderByClause(self, ctx: CypherParser.OrderByClauseContext):
        ctx.parentCtx.slots["order_var"] = ctx.slots["var"]
        ctx.parentCtx.slots["order_attr"] = ctx.slots["attr"]
        if "DESC" in ctx.getText():
            ctx.parentCtx.slots["order"] = "largest"
        else:
            ctx.parentCtx.slots["order"] = "smallest"
        return super().enterNode(ctx)

    # Enter a parse tree produced by CypherParser#limitClause.
    def enterLimitClause(self, ctx: CypherParser.LimitClauseContext):
        return super().enterNode(ctx)

    # Exit a parse tree produced by CypherParser#limitClause.
    def exitLimitClause(self, ctx: CypherParser.LimitClauseContext):
        if ctx.getText():
            ctx.parentCtx.slots["limit"] = re.search(r"(?<=LIMIT)\d+", ctx.getText()).group()
        else:
            ctx.parentCtx.slots["limit"] = None
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
        edge_var = None
        qualifier_constraints = []
        for i in range(len(paths)):

            if isinstance(paths[i], CypherParser.NodeContext):
                if paths[i].slots["label"]:
                    if len(paths[i].slots["label"]) > 1:
                        raise Exception("the current Graphq IR design does not support multiple types (labels)!")
                    else:
                        paths[i].slots["label"] = paths[i].slots["label"][0]
                ctx.slots["var_table"][i] = EntitySet(
                    paths[i].slots["var"], paths[i].slots["name"], paths[i].slots["label"]
                )
                for attr, sym, v_type, val in paths[i].slots["constraints"]:
                    ctx.slots["var_table"][i].add_related_attr(attr, sym, v_type, val)
                if previous_node_idxs is not None:
                    if edge_direction == "right":
                        ctx.slots["var_table"][previous_node_idxs].add_related_es(
                            edge, edge_var, "forward", ctx.slots["var_table"][i], qualifier_constraints
                        )
                        ctx.slots["var_table"][i].add_related_es(
                            edge, edge_var, "backward", ctx.slots["var_table"][previous_node_idxs], qualifier_constraints
                        )
                    elif edge_direction == "left":
                        ctx.slots["var_table"][previous_node_idxs].add_related_es(
                            edge, edge_var, "forward", ctx.slots["var_table"][i], qualifier_constraints
                        )
                        ctx.slots["var_table"][i].add_related_es(
                            edge, edge_var, "backward", ctx.slots["var_table"][previous_node_idxs], qualifier_constraints
                        )
                    else:
                        ctx.slots["var_table"][previous_node_idxs].add_related_es(
                            edge, edge_var, "undirected", ctx.slots["var_table"][i], qualifier_constraints
                        )
                        ctx.slots["var_table"][i].add_related_es(
                            edge, edge_var, "undirected", ctx.slots["var_table"][previous_node_idxs], qualifier_constraints
                        )

                previous_node_idxs = i
                edge_direction = None
                edge = None
                edge_var = None
                qualifier_constraints = []

            elif isinstance(paths[i], t.TerminalNodeImpl):
                if paths[i].getText() == "<-":
                    edge_direction = "left"
                elif paths[i].getText() == "->":
                    edge_direction = "right"

            elif isinstance(paths[i], CypherParser.RelationshipContext):

                edge_var = paths[i].slots["var"]
                qualifier_constraints = paths[i].slots["constraints"]
                if len(paths[i].slots["label"]) > 1:
                    raise Exception("Current UIR does not support more than one relationship labels!")
                elif len(paths[i].slots["label"]) == 1:
                    paths[i].slots["label"] = paths[i].slots["label"][0]
                    edge = paths[i].slots["label"]
                else:
                    edge = ""

        ctx.parentCtx.slots["var_list"] = list(ctx.slots["var_table"].values())
        return super().exitPath(ctx)

    # Enter a parse tree produced by CypherParser#node.
    def enterNode(self, ctx: CypherParser.NodeContext):
        ctx.slots = strictDict({"var": "", "name": "", "label": [], "constraints": []})
        return super().enterNode(ctx)

    # Exit a parse tree produced by CypherParser#node.
    def exitNode(self, ctx: CypherParser.NodeContext):
        return super().exitNode(ctx)

    # Enter a parse tree produced by CypherParser#nodeLabel.
    def enterNodeLabel(self, ctx: CypherParser.NodeLabelContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterNodeLabel(ctx)

    # Exit a parse tree produced by CypherParser#nodeLabel.
    def exitNodeLabel(self, ctx: CypherParser.NodeLabelContext):
        ctx.parentCtx.slots["label"].append(ctx.slots["string"])
        return super().exitNodeLabel(ctx)

    # Enter a parse tree produced by CypherParser#propertyConstraint.
    def enterPropertyConstraint(self, ctx: CypherParser.PropertyConstraintContext):
        ctx.slots = strictDict({"constraints": []})
        return super().enterPropertyConstraint(ctx)

    # Exit a parse tree produced by CypherParser#propertyConstraint.
    def exitPropertyConstraint(self, ctx: CypherParser.PropertyConstraintContext):
        ctx.parentCtx.slots["constraints"] = ctx.slots["constraints"]
        return super().exitPropertyConstraint(ctx)

    # Enter a parse tree produced by CypherParser#relationship.
    def enterRelationship(self, ctx: CypherParser.RelationshipContext):
        ctx.slots = strictDict({"var": "", "label": [], "constraints": []})
        return super().enterRelationship(ctx)

    # Exit a parse tree produced by CypherParser#relationship.
    def exitRelationship(self, ctx: CypherParser.RelationshipContext):
        return super().exitRelationship(ctx)

    # Enter a parse tree produced by CypherParser#relationshipLabel.
    def enterRelationshipLabel(self, ctx: CypherParser.RelationshipLabelContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterRelationshipLabel(ctx)

    # Exit a parse tree produced by CypherParser#relationshipLabel.
    def exitRelationshipLabel(self, ctx: CypherParser.RelationshipLabelContext):
        ctx.parentCtx.slots["label"].append(ctx.slots["string"])
        return super().exitRelationshipLabel(ctx)

    # Enter a parse tree produced by CypherParser#constraint.
    def enterConstraint(self, ctx: CypherParser.ConstraintContext):
        ctx.slots = strictDict({"var": "", "attr": "", "symOP": "", "value_type": "", "value": ""})
        return super().enterConstraint(ctx)

    # Exit a parse tree produced by CypherParser#constraint.
    def exitConstraint(self, ctx: CypherParser.ConstraintContext):
        assert ctx.slots["var"] is not None
        if ctx.slots["var"] not in ctx.parentCtx.slots["constraint_table"].keys():
            ctx.parentCtx.slots["constraint_table"][ctx.slots["var"]] = []
        ctx.parentCtx.slots["constraint_table"][ctx.slots["var"]].append({
            "attr": ctx.slots["attr"],
            "symOP": ctx.slots["symOP"],
            "value_type": ctx.slots["value_type"],
            "value": ctx.slots["value"],
        })
        return super().exitConstraint(ctx)

    # Enter a parse tree produced by CypherParser#alias.
    def enterAlias(self, ctx: CypherParser.AliasContext):
        ctx.slots = strictDict({"var": ""})
        return super().enterAlias(ctx)

    # Exit a parse tree produced by CypherParser#alias.
    def exitAlias(self, ctx: CypherParser.AliasContext):
        ctx.parentCtx.slots["alias"] = ctx.slots["var"]
        return super().exitAlias(ctx)


    # Enter a parse tree produced by CypherParser#symbolOP.
    def enterSymbolOP(self, ctx: CypherParser.SymbolOPContext):
        ctx.slots = strictDict({"OP": ""})
        try:
            ctx.slots["OP"] = self.symOP[ctx.getText()]
        except KeyError:
            raise Exception("Illegal operator!")
        return super().enterSymbolOP(ctx)

    # Exit a parse tree produced by CypherParser#symbolOP.
    def exitSymbolOP(self, ctx: CypherParser.SymbolOPContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["OP"]
        return super().exitSymbolOP(ctx)

    # Enter a parse tree produced by CypherParser#variable.
    def enterVariable(self, ctx: CypherParser.VariableContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterVariable(ctx)

    # Exit a parse tree produced by CypherParser#variable.
    def exitVariable(self, ctx: CypherParser.VariableContext):
        if isinstance(ctx.parentCtx, CypherParser.NodeOrRelationshipPropertyContext):
            ctx.parentCtx.slots["attr"] = ctx.slots["string"]
        else:
            ctx.parentCtx.slots["var"] = ctx.slots["string"]
        return super().exitVariable(ctx)

    # Enter a parse tree produced by CypherParser#variableAttribute.
    def enterVariableAttribute(self, ctx: CypherParser.VariableAttributeContext):
        ctx.slots = strictDict({"var": "", "attr": ""})
        return super().enterVariableAttribute(ctx)

    # Exit a parse tree produced by CypherParser#variableAttribute.
    def exitVariableAttribute(self, ctx: CypherParser.VariableAttributeContext):
        ctx.slots["var"] = list(ctx.getChildren())[0].slots["string"]
        ctx.slots["attr"] = list(ctx.getChildren())[2].slots["string"]

        ctx.parentCtx.slots["var"] = ctx.slots["var"]
        ctx.parentCtx.slots["attr"] = ctx.slots["attr"]
        return super().exitVariableAttribute(ctx)

    # Enter a parse tree produced by CypherParser#nodeProperty.
    def enterNodeOrRelationshipProperty(self, ctx: CypherParser.NodeOrRelationshipPropertyContext):
        ctx.slots = strictDict({"attr": "", "symOP": "is", "value_type": "text", "value": ""})
        return super().enterNodeOrRelationshipProperty(ctx)

    # Exit a parse tree produced by CypherParser#nodeProperty.
    def exitNodeOrRelationshipProperty(self, ctx: CypherParser.NodeOrRelationshipPropertyContext):
        ctx.parentCtx.slots["constraints"].append(
            (ctx.slots["attr"], ctx.slots["symOP"],  ctx.slots["value_type"], ctx.slots["value"])
        )
        return super().exitNodeOrRelationshipProperty(ctx)

    # Enter a parse tree produced by CypherParser#value.
    def enterValue(self, ctx: CypherParser.ValueContext):
        ctx.slots = strictDict({"string": "", "dtype": None})
        return super().enterValue(ctx)

    # Exit a parse tree produced by CypherParser#value.
    def exitValue(self, ctx: CypherParser.ValueContext):
        if len(list(ctx.getChildren())) != 1:
            ctx.slots["dtype"] = "text"
        elif re.match(r'\d{4}(\-\d{2}){2}', ctx.slots["string"]):
            ctx.slots["dtype"] = "date"
        else:
            ctx.slots["dtype"] = "number"
        ctx.parentCtx.slots['value'] = ctx.slots["string"]
        ctx.parentCtx.slots["value_type"] = ctx.slots["dtype"]
        return super().exitValue(ctx)

    # Enter a parse tree produced by CypherParser#varString.
    def enterVarString(self, ctx: CypherParser.VarStringContext):
        ctx.slots = strictDict({"string": ctx.getText()})
        return super().enterVarString(ctx)

    # Exit a parse tree produced by CypherParser#varString.
    def exitVarString(self, ctx: CypherParser.VarStringContext):
        ctx.parentCtx.slots['string'] = ctx.slots["string"]
        return super().exitVarString(ctx)

    # Enter a parse tree produced by CypherParser#string.
    def enterString(self, ctx: CypherParser.StringContext):
        ctx.slots = strictDict({"string": ctx.getText()})
        return super().enterString(ctx)

    # Exit a parse tree produced by CypherParser#string.
    def exitString(self, ctx: CypherParser.StringContext):
        ctx.slots["string"] = (" ".join([c.getText() for c in list(ctx.getChildren())])).strip()
        ctx.parentCtx.slots['string'] = ctx.slots["string"]
        return super().exitString(ctx)

