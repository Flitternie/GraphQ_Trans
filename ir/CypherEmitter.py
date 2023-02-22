import re
import warnings
from antlr4 import *

from graphq_trans.ir.IRLexer import IRLexer
from graphq_trans.ir.IRParser import IRParser
from graphq_trans.ir.IRParserListener import IRParserListener

from graphq_trans.utils import *
from graphq_trans.ir.misc import *


class CypherEmitter(IRParserListener):
    def __init__(self):
        self.output = ""

        self.entitySetSet = [
            IRParser.EntitySetGroupContext,
            IRParser.EntitySetIntersectContext,
            IRParser.EntitySetFilterContext,
            IRParser.EntitySetAtomContext,
            IRParser.EntitySetPlaceholderContext,
        ]

    def initialize(self):
        self.output = ""

    def emit(self, ctx):
        return self.output

    # Enter a parse tree produced by IRParser#root.
    def enterRoot(self, ctx: IRParser.RootContext):
        self.initialize()
        ctx.slots = strictDict({"matchClauses": [], "returnClause": "", "orderByClause": "", "limitClause": "",
                                "parallelQuery": {}})
        return super().enterRoot(ctx)

    # Exit a parse tree produced by IRParser#root.
    def exitRoot(self, ctx: IRParser.RootContext):
        for clause in ctx.slots["matchClauses"]:
            self.output += clause + "\n"
        self.output += ctx.slots["returnClause"]
        if ctx.slots["orderByClause"]:
            self.output += "\n" + ctx.slots["orderByClause"]
        if ctx.slots["parallelQuery"]:
            self.output += "\n" + "UNION\n"
            for clause in ctx.slots["parallelQuery"]["matchClauses"]:
                self.output += clause + "\n"
            self.output += ctx.slots["parallelQuery"]["returnClause"]
            if "orderByClause" in ctx.slots["parallelQuery"].keys():
                self.output += "\n" + ctx.slots["orderByClause"]

        if ctx.slots["limitClause"]:
            self.output += "\n" + ctx.slots["limitClause"]

        return super().exitRoot(ctx)

    # Enter a parse tree produced by IRParser#entityQuery.
    def enterEntityQuery(self, ctx: IRParser.EntityQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": ""})
        return super().enterEntityQuery(ctx)

    # Exit a parse tree produced by IRParser#entityQuery.
    def exitEntityQuery(self, ctx: IRParser.EntityQueryContext):
        return_clause = "RETURN {}.name".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitEntityQuery(ctx)

    # Enter a parse tree produced by IRParser#attributeQuery.
    def enterAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "query_attr": ""})
        return super().enterAttributeQuery(ctx)

    # Exit a parse tree produced by IRParser#attributeQuery.
    def exitAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        return_clause = "RETURN {}.{}".format(ctx.slots["query_var"], ctx.slots["query_attr"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitEntityQuery(ctx)

    # Enter a parse tree produced by IRParser#predicateQuery.
    def enterPredicateQuery(self, ctx: IRParser.PredicateQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "clauses": [], "edge_var": "", "var": ""})
        return super().enterPredicateQuery(ctx)

    # Exit a parse tree produced by IRParser#predicateQuery.
    def exitPredicateQuery(self, ctx: IRParser.PredicateQueryContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        assert len(children) == 2
        head, tail = children
        clauses_head, clauses_tail = ctx.slots["clauses"]

        n_step, r_step = find_max_idx(clauses_head)
        if n_step == 0:
            head.slots["var"] = "n1"
            n_step = 1

        tail.slots["var"] = re.sub(r"(?<=n)\d+", lambda x: str(int(x.group()) + n_step), tail.slots["var"])
        tail.slots["edge_var"] = re.sub(r"(?<=r)\d+", lambda x: str(int(x.group()) + r_step + 1),
                                        tail.slots["edge_var"])

        _, edge_idxs = find_min_unsused(clauses_head, clauses_tail)
        ctx.slots["edge_var"] = "r{}".format(edge_idxs)
        ctx.slots["var"] = head.slots["var"]
        ctx.slots["clauses"] = clauses_head + shift_index(n_step, r_step, clauses_tail)

        clause = "MATCH ({})<-[{}]-({})".format(head.slots["var"], ctx.slots["edge_var"], tail.slots["var"])
        ctx.slots["clauses"].append(clause)

        ctx.slots["matchClauses"] = ctx.slots["clauses"]
        ctx.slots["query_var"] = ctx.slots["edge_var"]

        return_clause = "RETURN {}.label".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitPredicateQuery(ctx)

    # Enter a parse tree produced by IRParser#qualifierQuery.
    def enterQualifierQuery(self, ctx: IRParser.QualifierQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "query_attr": ""})
        return super().enterQualifierQuery(ctx)

    # Exit a parse tree produced by IRParser#qualifierQuery.
    def exitQualifierQuery(self, ctx: IRParser.QualifierQueryContext):
        return_clause = "RETURN {}.{}".format(ctx.slots["query_var"], ctx.slots["query_attr"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitQualifierQuery(ctx)

    # Enter a parse tree produced by IRParser#countQuery.
    def enterCountQuery(self, ctx: IRParser.CountQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "extra_es": []})
        return super().enterCountQuery(ctx)

    # Exit a parse tree produced by IRParser#countQuery.
    def exitCountQuery(self, ctx: IRParser.CountQueryContext):
        return_clause = "RETURN count({})".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        if ctx.slots["extra_es"]:
            parallel_clauses, parallel_var = ctx.slots["extra_es"]
            parallel_return_clause = "RETURN count({})".format(parallel_var)
            ctx.parentCtx.slots["parallelQuery"] = {
                "matchClauses": parallel_clauses,
                "returnClause": parallel_return_clause
            }
        return super().exitCountQuery(ctx)

    # Enter a parse tree produced by IRParser#verifyQuery.
    def enterVerifyQuery(self, ctx: IRParser.VerifyQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": ""})
        return super().enterVerifyQuery(ctx)

    # Exit a parse tree produced by IRParser#verifyQuery.
    def exitVerifyQuery(self, ctx: IRParser.VerifyQueryContext):
        return_clause = "RETURN isEmpty({})".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitVerifyQuery(ctx)

    # Enter a parse tree produced by IRParser#selectQuery.
    def enterSelectQuery(self, ctx: IRParser.SelectQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "query_attr": "", "order": "", "extra_es": []})
        return super().enterSelectQuery(ctx)

    # Exit a parse tree produced by IRParser#selectQuery.
    def exitSelectQuery(self, ctx: IRParser.SelectQueryContext):
        orderByClause = "ORDER BY {}.{}".format(ctx.slots["query_var"], ctx.slots["query_attr"])
        if ctx.slots["order"] == "largest":
            orderByClause += " DESC"

        return_clause = "RETURN {}.name AS name".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        ctx.parentCtx.slots["orderByClause"] = orderByClause
        ctx.parentCtx.slots["limitClause"] = "LIMIT 1"

        if ctx.slots["extra_es"]:
            parallel_clauses, parallel_var = ctx.slots["extra_es"]
            parallel_orderByClause = "ORDER BY {}.{}".format(parallel_var, ctx.slots["query_attr"])
            if ctx.slots["order"] == "largest":
                parallel_orderByClause += " DESC"
            parallel_return_clause = "RETURN {}.name AS name".format(parallel_var)

            ctx.parentCtx.slots["parallelQuery"] = {
                "matchClauses": parallel_clauses,
                "returnClause": parallel_return_clause,
                "orderByClause": parallel_orderByClause
            }

        return super().exitSelectQuery(ctx)

    # Enter a parse tree produced by IRParser#valueQuery.
    def enterValueQuery(self, ctx: IRParser.ValueQueryContext):
        return super().enterValueQuery(ctx)

    # Exit a parse tree produced by IRParser#valueQuery.
    def exitValueQuery(self, ctx: IRParser.ValueQueryContext):
        return super().exitValueQuery(ctx)

    # Enter a parse tree produced by IRParser#verifyByAttribute.
    def enterVerifyByAttribute(self, ctx: IRParser.VerifyByAttributeContext):
        ctx.slots = strictDict(
            {"nodeProperty": "", "relationshipProperty": "", "var": "", "edge_var": "", "clauses": []})
        return super().enterVerifyByAttribute(ctx)

    # Exit a parse tree produced by IRParser#verifyByAttribute.
    def exitVerifyByAttribute(self, ctx: IRParser.VerifyByAttributeContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        assert len(children) == 1
        head = children[0]
        clauses_head = ctx.slots["clauses"][0]
        clauses = []
        has_added = False
        for clause in clauses_head:
            if head.slots["var"] in clause and not has_added:
                if "WHERE" not in clause:
                    clause = clause + " WHERE " + ctx.slots["nodeProperty"].format(head.slots["var"])
                else:
                    clause = re.sub(r"(?<=WHERE)\s", " (", clause)
                    clause = clause + " AND " + ctx.slots["nodeProperty"].format(head.slots["var"]) + ")"
                has_added = True
                clauses.append(clause)
            else:
                clauses.append(clause)

        ctx.slots["var"] = head.slots["var"]
        ctx.slots["edge_var"] = head.slots["edge_var"]
        ctx.slots["clauses"] = clauses
        ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
        if isinstance(ctx.parentCtx, IRParser.VerifyQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["edge_var"]

        return super().exitVerifyByAttribute(ctx)

    # Enter a parse tree produced by IRParser#verifyByPredicate.
    def enterVerifyByPredicate(self, ctx: IRParser.VerifyByPredicateContext):
        ctx.slots = strictDict({"predicate": "", "direction": "", "var": "", "edge_var": "", "clauses": [],
                                "relationshipProperty": ""})
        return super().enterVerifyByPredicate(ctx)

    # Exit a parse tree produced by IRParser#verifyByPredicate.
    def exitVerifyByPredicate(self, ctx: IRParser.VerifyByPredicateContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        assert len(children) == 2
        head, tail = children
        clauses_head, clauses_tail = ctx.slots["clauses"]

        n_step, r_step = find_max_idx(clauses_head)

        tail.slots["var"] = re.sub(r"(?<=n)\d+", lambda x: str(int(x.group()) + n_step), tail.slots["var"])
        tail.slots["edge_var"] = re.sub(r"(?<=r)\d+", lambda x: str(int(x.group()) + r_step), tail.slots["edge_var"])

        ctx.slots["clauses"] = clauses_head + shift_index(n_step, r_step, clauses_tail)

        if tail.slots["edge_var"]:
            ctx.slots["edge_var"] = re.sub(r"(?<=r)\d+", lambda x: str(int(x.group()) + 1), tail.slots["edge_var"])
        else:
            ctx.slots["edge_var"] = re.sub(r"(?<=r)\d+", lambda x: str(int(x.group()) + r_step), ctx.slots["edge_var"])

        if ctx.slots["direction"] == "backward":
            clause = "MATCH ({})<-[{}:{}]-({})"
        else:
            clause = "MATCH ({})-[{}:{}]->({})"

        clause = clause.format(head.slots["var"], ctx.slots["edge_var"], ctx.slots["predicate"], tail.slots["var"])
        if ctx.slots["relationshipProperty"]:
            pass
        ctx.slots["clauses"].append(clause)
        ctx.slots["var"] = head.slots["var"]

        ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
        if isinstance(ctx.parentCtx, IRParser.VerifyQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["edge_var"]
        return super().exitVerifyByPredicate(ctx)

    # Enter a parse tree produced by IRParser#entitySetGroup.
    def enterEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        ctx.slots = strictDict({"clauses": [], "var": "", "edge_var": "", "setOP": ""})
        return super().enterEntitySetGroup(ctx)

    # Exit a parse tree produced by IRParser#entitySetGroup.
    def exitEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        assert len(children) == 2
        head, tail = children
        clauses_head, clauses_tail = ctx.slots["clauses"]
        if ctx.slots["setOP"] == "OR":
            if isinstance(ctx.parentCtx, IRParser.SelectQueryContext):
                ctx.slots["clauses"] = clauses_head
                ctx.slots["var"] = head.slots["var"]
                ctx.slots["edge_var"] = head.slots["edge_var"]
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]

                ctx.parentCtx.slots["extra_es"] = (clauses_tail, tail.slots["var"])
            elif isinstance(ctx.parentCtx, IRParser.CountQueryContext):
                ctx.slots["clauses"] = clauses_head
                ctx.slots["var"] = head.slots["var"]
                ctx.slots["edge_var"] = head.slots["edge_var"]
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]

                ctx.parentCtx.slots["extra_es"] = (clauses_tail, tail.slots["var"])
            else:
                pass
        elif ctx.slots["setOP"] == "AND":
            n_new, _ = find_min_unsused(clauses_head, clauses_tail)
            clauses = []
            for clause in clauses_head:
                clauses.append(clause.replace(head.slots["var"], f"n{n_new}"))

            for clause in clauses_tail:
                clauses.append(clause.replace(tail.slots["var"], f"n{n_new}"))

            head.slots["var"] = f"n{n_new}"
            tail.slots["var"] = f"n{n_new}"
            ctx.slots["var"] = f"n{n_new}"

            ctx.slots["clauses"] = clauses
            if head.slots["edge_var"]:
                ctx.slots["edge_var"] = head.slots["edge_var"]
            else:
                ctx.slots["edge_var"] = tail.slots["edge_var"]
            # raise NotImplementedError("Recursive UNION not implemented yet")

            if isinstance(ctx.parentCtx, IRParser.AttributeQueryContext):
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
            elif isinstance(ctx.parentCtx, IRParser.EntityQueryContext):
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
            elif isinstance(ctx.parentCtx, IRParser.CountQueryContext):
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
            elif isinstance(ctx.parentCtx, IRParser.EntitySetByPredicateContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, IRParser.EntitySetGroupContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, IRParser.VerifyByPredicateContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, IRParser.VerifyByAttributeContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, IRParser.PredicateQueryContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])

        return super().exitEntitySetGroup(ctx)

    # Enter a parse tree produced by IRParser#entitySetIntersect.
    def enterEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        ctx.slots = strictDict({"clauses": [], "var": "", "edge_var": ""})
        return super().enterEntitySetIntersect(ctx)

    # Exit a parse tree produced by IRParser#entitySetIntersect.
    def exitEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        assert len(children) == 2
        head, tail = children
        clauses_head, clauses_tail = ctx.slots["clauses"]
        n_new, _ = find_min_unsused(clauses_head, clauses_tail)

        clauses = []
        for clause in clauses_head:
            clauses.append(clause.replace(head.slots["var"], f"n{n_new}"))

        for clause in clauses_tail:
            clauses.append(clause.replace(tail.slots["var"], f"n{n_new}"))

        head.slots["var"] = f"n{n_new}"
        tail.slots["var"] = f"n{n_new}"
        ctx.slots["var"] = f"n{n_new}"

        ctx.slots["clauses"] = clauses
        if head.slots["edge_var"]:
            ctx.slots["edge_var"] = head.slots["edge_var"]
        else:
            ctx.slots["edge_var"] = tail.slots["edge_var"]

        if isinstance(ctx.parentCtx, IRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.EntityQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.CountQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.EntitySetByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.EntitySetGroupContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.VerifyByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.PredicateQueryContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]

        return super().exitEntitySetIntersect(ctx)

    # Enter a parse tree produced by IRParser#entitySetFilter.
    def enterEntitySetFilter(self, ctx: IRParser.EntitySetFilterContext):
        ctx.slots = strictDict({"clauses": [], "var": "", "edge_var": ""})
        return super().enterEntitySetFilter(ctx)

    # Exit a parse tree produced by IRParser#entitySetFilter.
    def exitEntitySetFilter(self, ctx: IRParser.EntitySetFilterContext):
        if isinstance(ctx.parentCtx, IRParser.EntitySetByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.EntitySetIntersectContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.VerifyByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.EntitySetGroupContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.EntityQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.CountQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.SelectQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, IRParser.PredicateQueryContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        return super().exitEntitySetFilter(ctx)

    # Enter a parse tree produced by IRParser#entitySetAtom.
    def enterEntitySetAtom(self, ctx: IRParser.EntitySetAtomContext):
        ctx.slots = strictDict({"var": "n1", "edge_var": "", "entity": "ones", "clauses": []})
        return super().enterEntitySetAtom(ctx)

    # Exit a parse tree produced by IRParser#entitySetAtom.
    def exitEntitySetAtom(self, ctx: IRParser.EntitySetAtomContext):
        ctx.slots["clauses"] = ["MATCH ({}) WHERE {}.name = {}".format(
            ctx.slots["var"], ctx.slots["var"], ctx.slots["entity"]
        )]
        if isinstance(ctx.parentCtx, IRParser.EntitySetByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.EntitySetByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.VerifyByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.EntitySetIntersectContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.EntitySetGroupContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.PredicateQueryContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, IRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        else:
            pass
        return super().exitEntitySetAtom(ctx)

    # Enter a parse tree produced by IRParser#entitySetPlaceholder.
    def enterEntitySetPlaceholder(self, ctx: IRParser.EntitySetPlaceholderContext):
        ctx.slots = strictDict({"var": "", "edge_var": "", "entity": "ones", "clauses": []})
        return super().enterEntitySetPlaceholder(ctx)

    # Exit a parse tree produced by IRParser#entitySetPlaceholder.
    def exitEntitySetPlaceholder(self, ctx: IRParser.EntitySetPlaceholderContext):
        ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        return super().exitEntitySetPlaceholder(ctx)

    # Enter a parse tree produced by IRParser#entitySetByAttribute.
    def enterEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        ctx.slots = strictDict(
            {"clauses": [], "var": "n1", "edge_var": "", "concept": "", "nodeProperty": "",
             "relationshipProperty": ""})
        return super().enterEntitySetByAttribute(ctx)

    # Exit a parse tree produced by IRParser#entitySetByAttribute.
    def exitEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        if ctx.slots["relationshipProperty"]:
            warnings.warn("Cypher does not support attribute qualifier since it's not treated as a proper edge!")
        if children:
            head = children[0]
            clauses_head = ctx.slots["clauses"][0]
            ctx.slots["var"] = head.slots["var"]
            ctx.slots["edge_var"] = head.slots["edge_var"]
            clauses = clauses_head
        else:
            ctx.slots["var"] = "n1"
            clauses = []
        ctx.slots["nodeProperty"] = ctx.slots["nodeProperty"].format(ctx.slots["var"])

        if ctx.slots["concept"]:
            clause = "MATCH ({}:{}) WHERE {}"
        else:
            clause = "MATCH ({}{}) WHERE {}"

        clause = clause.format(ctx.slots["var"], ctx.slots["concept"], ctx.slots["nodeProperty"])
        clauses.append(clause)

        ctx.slots["clauses"] = clauses

        ctx.parentCtx.slots["clauses"].extend(ctx.slots["clauses"])
        ctx.parentCtx.slots["var"] = ctx.slots["var"]
        return super().exitEntitySetByAttribute(ctx)

    # Enter a parse tree produced by IRParser#entitySetByPredicate.
    def enterEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        ctx.slots = strictDict(
            {"clauses": [], "var": "", "edge_var": "", "concept": "", "predicate": "", "direction": "",
             "relationshipProperty": ""}
        )
        return super().enterEntitySetByPredicate(ctx)

    # Exit a parse tree produced by IRParser#entitySetByPredicate.
    def exitEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        if len(children) == 1:
            tail = children[0]
            clauses_tail = ctx.slots["clauses"][0]
            n_step, r_step = 1, 1

            ctx.slots["var"] = "n1"
            ctx.slots["edge_var"] = "r1"
            ctx.slots["clauses"] = shift_index(n_step, r_step, clauses_tail)

            tail.slots["var"] = re.sub(r"(?<=n)\d+", lambda x: str(int(x.group()) + n_step), tail.slots["var"])
            tail.slots["edge_var"] = re.sub(r"(?<=r)\d+", lambda x: str(int(x.group()) + r_step),
                                            tail.slots["edge_var"])

            if ctx.slots["concept"]:
                if ctx.slots["direction"] == "backward":
                    clause = "MATCH ({}:{})<-[{}:{}]-({})"
                else:
                    clause = "MATCH ({}:{})-[{}:{}]->({})"
            else:
                if ctx.slots["direction"] == "backward":
                    clause = "MATCH ({}{})<-[{}:{}]-({})"
                else:
                    clause = "MATCH ({}{})-[{}:{}]->({})"

            clause = clause.format(
                    ctx.slots["var"], ctx.slots["concept"], ctx.slots["edge_var"], ctx.slots["predicate"],
                    tail.slots["var"]
                )

            if ctx.slots["relationshipProperty"]:
                ctx.slots["relationshipProperty"] = ctx.slots["relationshipProperty"].format(ctx.slots["edge_var"])
                clause = clause + " WHERE " + ctx.slots["relationshipProperty"]

            ctx.slots["clauses"].append(clause)
            ctx.parentCtx.slots["clauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["var"] = ctx.slots["var"]
            ctx.parentCtx.slots["edge_var"] = ctx.slots["edge_var"]
        elif len(children) == 2:
            head, tail = children
            clauses_head, clauses_tail = ctx.slots["clauses"]
            n_step, r_step = find_max_idx(head.slots["clauses"])
            if n_step == 0:
                head.slots["var"] = "n1"
                n_step = 1

            tail.slots["var"] = re.sub(r"(?<=n)\d+", lambda x: str(int(x.group()) + n_step), tail.slots["var"])
            tail.slots["edge_var"] = re.sub(r"(?<=r)\d+", lambda x: str(int(x.group()) + r_step + 1),
                                            tail.slots["edge_var"])

            ctx.slots["edge_var"] = "r1"
            ctx.slots["var"] = head.slots["var"]
            ctx.slots["clauses"] = clauses_head + shift_index(n_step, r_step, clauses_tail)

            if ctx.slots["concept"]:
                if ctx.slots["direction"] == "backward":
                    clause = "MATCH ({}:{})<-[{}:{}]-({})"
                else:
                    clause = "MATCH ({}:{})-[{}:{}]->({})"
            else:
                if ctx.slots["direction"] == "backward":
                    clause = "MATCH ({}{})<-[{}:{}]-({})"
                else:
                    clause = "MATCH ({}{})-[{}:{}]->({})"

            clause = clause.format(
                ctx.slots["var"], ctx.slots["concept"], ctx.slots["edge_var"], ctx.slots["predicate"],
                tail.slots["var"]
            )

            ctx.slots["clauses"].append(clause)
            ctx.parentCtx.slots["clauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["var"] = ctx.slots["var"]
            ctx.parentCtx.slots["edge_var"] = ctx.slots["edge_var"]
        else:
            raise Exception("Get more than two EntitySets!")

        return super().exitEntitySetByPredicate(ctx)

    # Enter a parse tree produced by IRParser#entitySetByConcept.
    def enterEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        ctx.slots = strictDict({"concept": "", "var": "", "edge_var": "", "clauses": []})
        return super().enterEntitySetByConcept(ctx)

    # Exit a parse tree produced by IRParser#entitySetByConcept.
    def exitEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]

        if children:
            head = children[0]
            clauses_head = ctx.slots["clauses"]
            new_clauses = []
            for clause in clauses_head:
                new_clauses.append(re.sub(r"(?<=\(){}(?=\))".format(re.escape(head.slots["var"])),
                                          "{}:{}".format(ctx.slots["concept"], head.slots["var"])))
            if head.slots["var"]:
                ctx.slots["var"] = head.slots["var"]
            else:
                ctx.slots["var"] = "n1"
            ctx.slots["edge_var"] = head.slots["edge_var"]
            ctx.slots["clauses"] = new_clauses
        else:
            ctx.slots["var"] = "n1"
            ctx.slots["clauses"] = ["MATCH ({}:{})".format(ctx.slots["var"], ctx.slots["concept"])]
        ctx.parentCtx.slots["clauses"].extend(ctx.slots["clauses"])
        ctx.parentCtx.slots["var"] = ctx.slots["var"]
        ctx.parentCtx.slots["edge_var"] = ctx.slots["edge_var"]

        return super().enterEntitySetByConcept(ctx)

    # Enter a parse tree produced by IRParser#entitySetByRank.
    def enterEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetByRank.
    def exitEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        pass

    # Enter a parse tree produced by IRParser#filterByRank.
    def enterFilterByRank(self, ctx: IRParser.FilterByRankContext):
        ctx.slots = strictDict({"attribute": "", "number": "", "stringOP": ""})
        return super().enterFilterByRank(ctx)

    # Exit a parse tree produced by IRParser#filterByRank.
    def exitFilterByRank(self, ctx: IRParser.FilterByRankContext):
        if isinstance(ctx.parentCtx, IRParser.SelectQueryContext):
            ctx.parentCtx.slots["query_attr"] = ctx.slots["attribute"]
            ctx.parentCtx.slots["order"] = ctx.slots["stringOP"]
        else:
            pass
        return super().exitFilterByRank(ctx)

    # Enter a parse tree produced by IRParser#filterByAttribute.
    def enterFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        ctx.slots = strictDict({"attribute": None, "symOP": None, "value": ""})
        return super().enterFilterByAttribute(ctx)

    # Exit a parse tree produced by IRParser#filterByAttribute.
    def exitFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        ctx.parentCtx.slots["nodeProperty"] = "{}.{} {} {}".format(
            "{}", ctx.slots["attribute"], ctx.slots["symOP"], ctx.slots["value"]
        )
        return super().exitFilterByAttribute(ctx)

    # Enter a parse tree produced by IRParser#filterByPredicate.
    def enterFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        ctx.slots = strictDict({"predicate": None, "direction": None, "edge_var": ""})
        return super().enterFilterByPredicate(ctx)

    # Exit a parse tree produced by IRParser#filterByPredicate.
    def exitFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"]
        ctx.parentCtx.slots["direction"] = ctx.slots["direction"]
        ctx.parentCtx.slots["edge_var"] = ctx.slots["edge_var"]
        return super().exitFilterByPredicate(ctx)

    # Enter a parse tree produced by IRParser#filterByQualifier.
    def enterFilterByQualifier(self, ctx: IRParser.FilterByQualifierContext):
        ctx.slots = strictDict({"qualifier": "", "symOP": "", "value": ""})
        return super().enterFilterByQualifier(ctx)

    # Exit a parse tree produced by IRParser#filterByQualifier.
    def exitFilterByQualifier(self, ctx: IRParser.FilterByQualifierContext):
        ctx.parentCtx.slots["relationshipProperty"] = "{}.{} {} {}".format(
            "{}", ctx.slots["qualifier"], ctx.slots["symOP"], ctx.slots["value"]
        )
        return super().exitFilterByQualifier(ctx)

    # Enter a parse tree produced by IRParser#forward.
    def enterForward(self, ctx: IRParser.ForwardContext):
        return super().enterForward(ctx)

    # Exit a parse tree produced by IRParser#forward.
    def exitForward(self, ctx: IRParser.ForwardContext):
        ctx.parentCtx.slots["direction"] = "forward"
        return super().exitForward(ctx)

    # Enter a parse tree produced by IRParser#backward.
    def enterBackward(self, ctx: IRParser.BackwardContext):
        return super().enterBackward(ctx)

    # Exit a parse tree produced by IRParser#backward.
    def exitBackward(self, ctx: IRParser.BackwardContext):
        ctx.parentCtx.slots["direction"] = "backward"
        return super().exitBackward(ctx)

    # Enter a parse tree produced by IRParser#and.
    def enterAnd(self, ctx: IRParser.AndContext):
        ctx.slots = strictDict({"setOP": "AND"})
        return super().enterAnd(ctx)

    # Exit a parse tree produced by IRParser#and.
    def exitAnd(self, ctx: IRParser.AndContext):
        ctx.parentCtx.slots["setOP"] = ctx.slots["setOP"]
        return super().exitAnd(ctx)

    # Enter a parse tree produced by IRParser#or.
    def enterOr(self, ctx: IRParser.OrContext):
        ctx.slots = strictDict({"setOP": "OR"})
        return super().enterOr(ctx)

    # Exit a parse tree produced by IRParser#or.
    def exitOr(self, ctx: IRParser.OrContext):
        ctx.parentCtx.slots["setOP"] = ctx.slots["setOP"]
        return super().exitOr(ctx)

    # Enter a parse tree produced by IRParser#not.
    def enterNot(self, ctx: IRParser.NotContext):
        pass

    # Exit a parse tree produced by IRParser#not.
    def exitNot(self, ctx: IRParser.NotContext):
        pass

    # Enter a parse tree produced by IRParser#notEqual.
    def enterNotEqual(self, ctx: IRParser.NotEqualContext):
        ctx.slots = strictDict({"symOP": "<>"})
        return super().enterNotEqual(ctx)

    # Exit a parse tree produced by IRParser#notEqual.
    def exitNotEqual(self, ctx: IRParser.NotEqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitNotEqual(ctx)

    # Enter a parse tree produced by IRParser#equal.
    def enterEqual(self, ctx: IRParser.EqualContext):
        ctx.slots = strictDict({"symOP": "="})
        return super().enterEqual(ctx)

    # Exit a parse tree produced by IRParser#equal.
    def exitEqual(self, ctx: IRParser.EqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitEqual(ctx)

    # Enter a parse tree produced by IRParser#larger.
    def enterLarger(self, ctx: IRParser.LargerContext):
        ctx.slots = strictDict({"symOP": ">"})
        return super().enterLarger(ctx)

    # Exit a parse tree produced by IRParser#larger.
    def exitLarger(self, ctx: IRParser.LargerContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitLarger(ctx)

    # Enter a parse tree produced by IRParser#smaller.
    def enterSmaller(self, ctx: IRParser.SmallerContext):
        ctx.slots = strictDict({"symOP": "<"})
        return super().enterSmaller(ctx)

    # Exit a parse tree produced by IRParser#smaller.
    def exitSmaller(self, ctx: IRParser.SmallerContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitSmaller(ctx)

    # Enter a parse tree produced by IRParser#largerEqual.
    def enterLargerEqual(self, ctx: IRParser.LargerEqualContext):
        ctx.slots = strictDict({"symOP": ">="})
        return super().enterLargerEqual(ctx)

    # Exit a parse tree produced by IRParser#largerEqual.
    def exitLargerEqual(self, ctx: IRParser.LargerEqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitLargerEqual(ctx)

    # Enter a parse tree produced by IRParser#smallerEqual.
    def enterSmallerEqual(self, ctx: IRParser.SmallerEqualContext):
        ctx.slots = strictDict({"symOP": "<="})
        return super().enterSmallerEqual(ctx)

    # Exit a parse tree produced by IRParser#smallerEqual.
    def exitSmallerEqual(self, ctx: IRParser.SmallerEqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitSmallerEqual(ctx)

    # Enter a parse tree produced by IRParser#largest.
    def enterLargest(self, ctx: IRParser.LargestContext):
        ctx.slots = strictDict({"stringOP": "largest"})
        return super().enterLargest(ctx)

    # Exit a parse tree produced by IRParser#largest.
    def exitLargest(self, ctx: IRParser.LargestContext):
        ctx.parentCtx.slots["stringOP"] = ctx.slots["stringOP"]
        return super().exitLargest(ctx)

    # Enter a parse tree produced by IRParser#smallest.
    def enterSmallest(self, ctx: IRParser.SmallestContext):
        ctx.slots = strictDict({"stringOP": "largest"})
        return super().enterSmallest(ctx)

    # Exit a parse tree produced by IRParser#smallest.
    def exitSmallest(self, ctx: IRParser.SmallestContext):
        ctx.parentCtx.slots["stringOP"] = ctx.slots["stringOP"]
        return super().exitSmallest(ctx)

    # Enter a parse tree produced by IRParser#sum.
    def enterSum(self, ctx: IRParser.SumContext):
        pass

    # Exit a parse tree produced by IRParser#sum.
    def exitSum(self, ctx: IRParser.SumContext):
        pass

    # Enter a parse tree produced by IRParser#average.
    def enterAverage(self, ctx: IRParser.AverageContext):
        pass

    # Exit a parse tree produced by IRParser#average.
    def exitAverage(self, ctx: IRParser.AverageContext):
        pass

    # Enter a parse tree produced by IRParser#valueByUnion.
    def enterValueByUnion(self, ctx: IRParser.ValueByUnionContext):
        pass

    # Exit a parse tree produced by IRParser#valueByUnion.
    def exitValueByUnion(self, ctx: IRParser.ValueByUnionContext):
        pass

    # Enter a parse tree produced by IRParser#valueByAggregate.
    def enterValueByAggregate(self, ctx: IRParser.ValueByAggregateContext):
        pass

    # Exit a parse tree produced by IRParser#valueByAggregate.
    def exitValueByAggregate(self, ctx: IRParser.ValueByAggregateContext):
        pass

    # Enter a parse tree produced by IRParser#valueByAttribute.
    def enterValueByAttribute(self, ctx: IRParser.ValueByAttributeContext):
        pass

    # Exit a parse tree produced by IRParser#valueByAttribute.
    def exitValueByAttribute(self, ctx: IRParser.ValueByAttributeContext):
        pass

    # Enter a parse tree produced by IRParser#valueAtom.
    def enterValueAtom(self, ctx: IRParser.ValueAtomContext):
        ctx.slots = strictDict({"valueType": "", "value": ""})
        return super().enterValueAtom(ctx)

    # Exit a parse tree produced by IRParser#valueAtom.
    def exitValueAtom(self, ctx: IRParser.ValueAtomContext):
        if isinstance(ctx.parentCtx, IRParser.FilterByAttributeContext):
            if ctx.slots["valueType"] == "text":
                ctx.parentCtx.slots["value"] = valid_str(ctx.slots["value"])
            else:
                ctx.parentCtx.slots["value"] = ctx.slots["value"]
        elif isinstance(ctx.parentCtx, IRParser.FilterByQualifierContext):
            if ctx.slots["valueType"] == "text":
                ctx.parentCtx.slots["value"] = valid_str(ctx.slots["value"])
            else:
                ctx.parentCtx.slots["value"] = ctx.slots["value"]

        return super().exitValueAtom(ctx)

    # Enter a parse tree produced by IRParser#text.
    def enterText(self, ctx: IRParser.TextContext):
        ctx.slots = strictDict({"string": ctx.getText()})
        return super().enterText(ctx)

    # Exit a parse tree produced by IRParser#text.
    def exitText(self, ctx: IRParser.TextContext):
        ctx.parentCtx.slots["valueType"] = ctx.slots["string"]
        return super().exitNumber(ctx)

    # Enter a parse tree produced by IRParser#quantity.
    def enterQuantity(self, ctx: IRParser.QuantityContext):
        pass

    # Exit a parse tree produced by IRParser#quantity.
    def exitQuantity(self, ctx: IRParser.QuantityContext):
        pass

    # Enter a parse tree produced by IRParser#date.
    def enterDate(self, ctx: IRParser.DateContext):
        pass

    # Exit a parse tree produced by IRParser#date.
    def exitDate(self, ctx: IRParser.DateContext):
        pass

    # Enter a parse tree produced by IRParser#Month.
    def enterMonth(self, ctx: IRParser.MonthContext):
        pass

    # Exit a parse tree produced by IRParser#Month.
    def exitMonth(self, ctx: IRParser.MonthContext):
        pass

    # Enter a parse tree produced by IRParser#year.
    def enterYear(self, ctx: IRParser.YearContext):
        pass

    # Exit a parse tree produced by IRParser#year.
    def exitYear(self, ctx: IRParser.YearContext):
        pass

    # Enter a parse tree produced by IRParser#time.
    def enterTime(self, ctx: IRParser.TimeContext):
        pass

    # Exit a parse tree produced by IRParser#time.
    def exitTime(self, ctx: IRParser.TimeContext):
        pass

    # Enter a parse tree produced by IRParser#entity.
    def enterEntity(self, ctx: IRParser.EntityContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterEntity(ctx)

    # Exit a parse tree produced by IRParser#entity.
    def exitEntity(self, ctx: IRParser.EntityContext):
        ctx.parentCtx.slots["entity"] = valid_str(ctx.slots["string"])
        return super().exitEntity(ctx)

    # Enter a parse tree produced by IRParser#attribute.
    def enterAttribute(self, ctx: IRParser.AttributeContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterAttribute(ctx)

    # Exit a parse tree produced by IRParser#attribute.
    def exitAttribute(self, ctx: IRParser.AttributeContext):
        if isinstance(ctx.parentCtx, IRParser.AttributeQueryContext):
            ctx.parentCtx.slots["query_attr"] = valid_var(ctx.slots["string"])
        else:
            ctx.parentCtx.slots["attribute"] = valid_var(ctx.slots["string"])
        return super().exitAttribute(ctx)

    # Enter a parse tree produced by IRParser#concept.
    def enterConcept(self, ctx: IRParser.ConceptContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterConcept(ctx)

    # Exit a parse tree produced by IRParser#concept.
    def exitConcept(self, ctx: IRParser.ConceptContext):
        ctx.parentCtx.slots["concept"] = valid_var(ctx.slots["string"])
        return super().exitConcept(ctx)

    # Enter a parse tree produced by IRParser#predicate.
    def enterPredicate(self, ctx: IRParser.PredicateContext):
        ctx.slots = strictDict({"string": "", "var": "r1"})
        return super().enterPredicate(ctx)

    # Exit a parse tree produced by IRParser#predicate.
    def exitPredicate(self, ctx: IRParser.PredicateContext):
        ctx.parentCtx.slots["predicate"] = valid_var(ctx.slots["string"])
        ctx.parentCtx.slots["edge_var"] = ctx.slots["var"]
        return super().exitPredicate(ctx)

    # Enter a parse tree produced by IRParser#qualifier.
    def enterQualifier(self, ctx: IRParser.QualifierContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterQualifier(ctx)

    # Exit a parse tree produced by IRParser#qualifier.
    def exitQualifier(self, ctx: IRParser.QualifierContext):
        if isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            ctx.parentCtx.slots["query_attr"] = valid_var(ctx.slots["string"])
        else:
            ctx.parentCtx.slots["qualifier"] = valid_var(ctx.slots["string"])

    # Enter a parse tree produced by IRParser#value.
    def enterValue(self, ctx: IRParser.ValueContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterValue(ctx)

    # Exit a parse tree produced by IRParser#value.
    def exitValue(self, ctx: IRParser.ValueContext):
        ctx.parentCtx.slots["value"] = ctx.slots["string"]
        return super().exitValue(ctx)

    # Enter a parse tree produced by IRParser#number.
    def enterNumber(self, ctx: IRParser.NumberContext):
        return super().enterNumber(ctx)

    # Exit a parse tree produced by IRParser#number.
    def exitNumber(self, ctx: IRParser.NumberContext):
        return super().exitNumber(ctx)

    # Enter a parse tree produced by IRParser#string.
    def enterString(self, ctx: IRParser.StringContext):
        ctx.slots = strictDict({"string": ctx.getText()})
        return super().enterString(ctx)

    # Exit a parse tree produced by IRParser#string.
    def exitString(self, ctx: IRParser.StringContext):
        ctx.parentCtx.slots["string"] = ctx.slots["string"]
        return super().exitString(ctx)


