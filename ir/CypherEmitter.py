import re
import warnings
from antlr4 import *

from graphq_trans.ir.UnifiedIRLexer import UnifiedIRLexer
from graphq_trans.ir.UnifiedIRParser import UnifiedIRParser
from graphq_trans.ir.UnifiedIRParserListener import UnifiedIRParserListener

from graphq_trans.utils import *
from graphq_trans.ir.misc import *


class CypherEmitter(UnifiedIRParserListener):
    def __init__(self):
        self.output = ""

        self.entitySetSet = [
            UnifiedIRParser.EntitySetGroupContext,
            UnifiedIRParser.EntitySetIntersectContext,
            UnifiedIRParser.EntitySetFilterContext,
            UnifiedIRParser.EntitySetAtomContext,
            UnifiedIRParser.EntitySetPlaceholderContext,
        ]

    def initialize(self):
        self.output = ""

    def emit(self, ctx):
        return self.output

    # Enter a parse tree produced by UnifiedIRParser#root.
    def enterRoot(self, ctx: UnifiedIRParser.RootContext):
        self.initialize()
        ctx.slots = strictDict({"matchClauses": [], "returnClause": "", "orderByClause": "", "limitClause": "",
                                "parallelQuery": {}})
        return super().enterRoot(ctx)

    # Exit a parse tree produced by UnifiedIRParser#root.
    def exitRoot(self, ctx: UnifiedIRParser.RootContext):
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

    # Enter a parse tree produced by UnifiedIRParser#entityQuery.
    def enterEntityQuery(self, ctx: UnifiedIRParser.EntityQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": ""})
        return super().enterEntityQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entityQuery.
    def exitEntityQuery(self, ctx: UnifiedIRParser.EntityQueryContext):
        return_clause = "RETURN {}.name".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitEntityQuery(ctx)

    # Enter a parse tree produced by UnifiedIRParser#attributeQuery.
    def enterAttributeQuery(self, ctx: UnifiedIRParser.AttributeQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "query_attr": ""})
        return super().enterAttributeQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#attributeQuery.
    def exitAttributeQuery(self, ctx: UnifiedIRParser.AttributeQueryContext):
        return_clause = "RETURN {}.{}".format(ctx.slots["query_var"], ctx.slots["query_attr"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitEntityQuery(ctx)

    # Enter a parse tree produced by UnifiedIRParser#predicateQuery.
    def enterPredicateQuery(self, ctx: UnifiedIRParser.PredicateQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "clauses": [], "edge_var": "", "var": ""})
        return super().enterPredicateQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#predicateQuery.
    def exitPredicateQuery(self, ctx: UnifiedIRParser.PredicateQueryContext):
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

        clause = "MATCH ({})-[{}]->({})".format(head.slots["var"], ctx.slots["edge_var"], tail.slots["var"])
        ctx.slots["clauses"].append(clause)

        ctx.slots["matchClauses"] = ctx.slots["clauses"]
        ctx.slots["query_var"] = ctx.slots["edge_var"]

        return_clause = "RETURN {}.label".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitPredicateQuery(ctx)

    # Enter a parse tree produced by UnifiedIRParser#qualifierQuery.
    def enterQualifierQuery(self, ctx: UnifiedIRParser.QualifierQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "query_attr": ""})
        return super().enterQualifierQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#qualifierQuery.
    def exitQualifierQuery(self, ctx: UnifiedIRParser.QualifierQueryContext):
        return_clause = "RETURN {}.{}".format(ctx.slots["query_var"], ctx.slots["query_attr"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitQualifierQuery(ctx)

    # Enter a parse tree produced by UnifiedIRParser#countQuery.
    def enterCountQuery(self, ctx: UnifiedIRParser.CountQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "extra_es": []})
        return super().enterCountQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#countQuery.
    def exitCountQuery(self, ctx: UnifiedIRParser.CountQueryContext):
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

    # Enter a parse tree produced by UnifiedIRParser#verifyQuery.
    def enterVerifyQuery(self, ctx: UnifiedIRParser.VerifyQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": ""})
        return super().enterVerifyQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#verifyQuery.
    def exitVerifyQuery(self, ctx: UnifiedIRParser.VerifyQueryContext):
        return_clause = "RETURN isEmpty({})".format(ctx.slots["query_var"])
        ctx.parentCtx.slots["matchClauses"] = ctx.slots["matchClauses"]
        ctx.parentCtx.slots["returnClause"] = return_clause
        return super().exitVerifyQuery(ctx)

    # Enter a parse tree produced by UnifiedIRParser#selectQuery.
    def enterSelectQuery(self, ctx: UnifiedIRParser.SelectQueryContext):
        ctx.slots = strictDict({"matchClauses": [], "query_var": "", "query_attr": "", "order": "", "extra_es": []})
        return super().enterSelectQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#selectQuery.
    def exitSelectQuery(self, ctx: UnifiedIRParser.SelectQueryContext):
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

    # Enter a parse tree produced by UnifiedIRParser#valueQuery.
    def enterValueQuery(self, ctx: UnifiedIRParser.ValueQueryContext):
        return super().enterValueQuery(ctx)

    # Exit a parse tree produced by UnifiedIRParser#valueQuery.
    def exitValueQuery(self, ctx: UnifiedIRParser.ValueQueryContext):
        return super().exitValueQuery(ctx)

    # Enter a parse tree produced by UnifiedIRParser#verifyByAttribute.
    def enterVerifyByAttribute(self, ctx: UnifiedIRParser.VerifyByAttributeContext):
        ctx.slots = strictDict(
            {"nodeProperty": "", "relationshipProperty": "", "var": "", "edge_var": "", "clauses": []})
        return super().enterVerifyByAttribute(ctx)

    # Exit a parse tree produced by UnifiedIRParser#verifyByAttribute.
    def exitVerifyByAttribute(self, ctx: UnifiedIRParser.VerifyByAttributeContext):
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
        if isinstance(ctx.parentCtx, UnifiedIRParser.VerifyQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.QualifierQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["edge_var"]

        return super().exitVerifyByAttribute(ctx)

    # Enter a parse tree produced by UnifiedIRParser#verifyByPredicate.
    def enterVerifyByPredicate(self, ctx: UnifiedIRParser.VerifyByPredicateContext):
        ctx.slots = strictDict({"predicate": "", "direction": "", "var": "", "edge_var": "", "clauses": [],
                                "relationshipProperty": ""})
        return super().enterVerifyByPredicate(ctx)

    # Exit a parse tree produced by UnifiedIRParser#verifyByPredicate.
    def exitVerifyByPredicate(self, ctx: UnifiedIRParser.VerifyByPredicateContext):
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

        if ctx.slots["direction"] == "forward":
            clause = "MATCH ({})<-[{}:{}]-({})"
        else:
            clause = "MATCH ({})-[{}:{}]->({})"

        clause = clause.format(head.slots["var"], ctx.slots["edge_var"], ctx.slots["predicate"], tail.slots["var"])
        if ctx.slots["relationshipProperty"]:
            pass
        ctx.slots["clauses"].append(clause)
        ctx.slots["var"] = head.slots["var"]

        ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
        if isinstance(ctx.parentCtx, UnifiedIRParser.VerifyQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.QualifierQueryContext):
            ctx.parentCtx.slots["query_var"] = ctx.slots["edge_var"]
        return super().exitVerifyByPredicate(ctx)

    # Enter a parse tree produced by UnifiedIRParser#entitySetGroup.
    def enterEntitySetGroup(self, ctx: UnifiedIRParser.EntitySetGroupContext):
        ctx.slots = strictDict({"clauses": [], "var": "", "edge_var": "", "setOP": ""})
        return super().enterEntitySetGroup(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetGroup.
    def exitEntitySetGroup(self, ctx: UnifiedIRParser.EntitySetGroupContext):
        children = [child for child in iter(ctx.getChildren()) if type(child) in self.entitySetSet]
        assert len(children) == 2
        head, tail = children
        clauses_head, clauses_tail = ctx.slots["clauses"]
        if ctx.slots["setOP"] == "OR":
            if isinstance(ctx.parentCtx, UnifiedIRParser.SelectQueryContext):
                ctx.slots["clauses"] = clauses_head
                ctx.slots["var"] = head.slots["var"]
                ctx.slots["edge_var"] = head.slots["edge_var"]
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]

                ctx.parentCtx.slots["extra_es"] = (clauses_tail, tail.slots["var"])
            elif isinstance(ctx.parentCtx, UnifiedIRParser.CountQueryContext):
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

            if isinstance(ctx.parentCtx, UnifiedIRParser.AttributeQueryContext):
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
            elif isinstance(ctx.parentCtx, UnifiedIRParser.EntityQueryContext):
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
            elif isinstance(ctx.parentCtx, UnifiedIRParser.CountQueryContext):
                ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
                ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
            elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetByPredicateContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetGroupContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByPredicateContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByAttributeContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
            elif isinstance(ctx.parentCtx, UnifiedIRParser.PredicateQueryContext):
                ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])

        return super().exitEntitySetGroup(ctx)

    # Enter a parse tree produced by UnifiedIRParser#entitySetIntersect.
    def enterEntitySetIntersect(self, ctx: UnifiedIRParser.EntitySetIntersectContext):
        ctx.slots = strictDict({"clauses": [], "var": "", "edge_var": ""})
        return super().enterEntitySetIntersect(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetIntersect.
    def exitEntitySetIntersect(self, ctx: UnifiedIRParser.EntitySetIntersectContext):
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

        if isinstance(ctx.parentCtx, UnifiedIRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntityQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.CountQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetGroupContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.PredicateQueryContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]

        return super().exitEntitySetIntersect(ctx)

    # Enter a parse tree produced by UnifiedIRParser#entitySetFilter.
    def enterEntitySetFilter(self, ctx: UnifiedIRParser.EntitySetFilterContext):
        ctx.slots = strictDict({"clauses": [], "var": "", "edge_var": ""})
        return super().enterEntitySetFilter(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetFilter.
    def exitEntitySetFilter(self, ctx: UnifiedIRParser.EntitySetFilterContext):
        if isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetIntersectContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetGroupContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntityQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.CountQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.SelectQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.PredicateQueryContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        return super().exitEntitySetFilter(ctx)

    # Enter a parse tree produced by UnifiedIRParser#entitySetAtom.
    def enterEntitySetAtom(self, ctx: UnifiedIRParser.EntitySetAtomContext):
        ctx.slots = strictDict({"var": "n1", "edge_var": "", "entity": "ones", "clauses": []})
        return super().enterEntitySetAtom(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetAtom.
    def exitEntitySetAtom(self, ctx: UnifiedIRParser.EntitySetAtomContext):
        ctx.slots["clauses"] = ["MATCH ({}) WHERE {}.name = {}".format(
            ctx.slots["var"], ctx.slots["var"], ctx.slots["entity"]
        )]
        if isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByPredicateContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetIntersectContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.EntitySetGroupContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.PredicateQueryContext):
            ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        elif isinstance(ctx.parentCtx, UnifiedIRParser.AttributeQueryContext):
            ctx.parentCtx.slots["matchClauses"].extend(ctx.slots["clauses"])
            ctx.parentCtx.slots["query_var"] = ctx.slots["var"]
        else:
            pass
        return super().exitEntitySetAtom(ctx)

    # Enter a parse tree produced by UnifiedIRParser#entitySetPlaceholder.
    def enterEntitySetPlaceholder(self, ctx: UnifiedIRParser.EntitySetPlaceholderContext):
        ctx.slots = strictDict({"var": "", "edge_var": "", "entity": "ones", "clauses": []})
        return super().enterEntitySetPlaceholder(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetPlaceholder.
    def exitEntitySetPlaceholder(self, ctx: UnifiedIRParser.EntitySetPlaceholderContext):
        ctx.parentCtx.slots["clauses"].append(ctx.slots["clauses"])
        return super().exitEntitySetPlaceholder(ctx)

    # Enter a parse tree produced by UnifiedIRParser#entitySetByAttribute.
    def enterEntitySetByAttribute(self, ctx: UnifiedIRParser.EntitySetByAttributeContext):
        ctx.slots = strictDict(
            {"clauses": [], "var": "n1", "edge_var": "", "concept": "", "nodeProperty": "",
             "relationshipProperty": ""})
        return super().enterEntitySetByAttribute(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetByAttribute.
    def exitEntitySetByAttribute(self, ctx: UnifiedIRParser.EntitySetByAttributeContext):
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

    # Enter a parse tree produced by UnifiedIRParser#entitySetByPredicate.
    def enterEntitySetByPredicate(self, ctx: UnifiedIRParser.EntitySetByPredicateContext):
        ctx.slots = strictDict(
            {"clauses": [], "var": "", "edge_var": "", "concept": "", "predicate": "", "direction": "",
             "relationshipProperty": ""}
        )
        return super().enterEntitySetByPredicate(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetByPredicate.
    def exitEntitySetByPredicate(self, ctx: UnifiedIRParser.EntitySetByPredicateContext):
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
                if ctx.slots["direction"] == "forward":
                    clause = "MATCH ({}:{})<-[{}:{}]-({})"
                else:
                    clause = "MATCH ({}:{})-[{}:{}]->({})"
            else:
                if ctx.slots["direction"] == "forward":
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
                if ctx.slots["direction"] == "forward":
                    clause = "MATCH ({}:{})<-[{}:{}]-({})"
                else:
                    clause = "MATCH ({}:{})-[{}:{}]->({})"
            else:
                if ctx.slots["direction"] == "forward":
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

    # Enter a parse tree produced by UnifiedIRParser#entitySetByConcept.
    def enterEntitySetByConcept(self, ctx: UnifiedIRParser.EntitySetByConceptContext):
        ctx.slots = strictDict({"concept": "", "var": "", "edge_var": "", "clauses": []})
        return super().enterEntitySetByConcept(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entitySetByConcept.
    def exitEntitySetByConcept(self, ctx: UnifiedIRParser.EntitySetByConceptContext):
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

    # Enter a parse tree produced by UnifiedIRParser#entitySetByRank.
    def enterEntitySetByRank(self, ctx: UnifiedIRParser.EntitySetByRankContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#entitySetByRank.
    def exitEntitySetByRank(self, ctx: UnifiedIRParser.EntitySetByRankContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#filterByRank.
    def enterFilterByRank(self, ctx: UnifiedIRParser.FilterByRankContext):
        ctx.slots = strictDict({"attribute": "", "number": "", "stringOP": ""})
        return super().enterFilterByRank(ctx)

    # Exit a parse tree produced by UnifiedIRParser#filterByRank.
    def exitFilterByRank(self, ctx: UnifiedIRParser.FilterByRankContext):
        if isinstance(ctx.parentCtx, UnifiedIRParser.SelectQueryContext):
            ctx.parentCtx.slots["query_attr"] = ctx.slots["attribute"]
            ctx.parentCtx.slots["order"] = ctx.slots["stringOP"]
        else:
            pass
        return super().exitFilterByRank(ctx)

    # Enter a parse tree produced by UnifiedIRParser#filterByAttribute.
    def enterFilterByAttribute(self, ctx: UnifiedIRParser.FilterByAttributeContext):
        ctx.slots = strictDict({"attribute": None, "symOP": None, "value": ""})
        return super().enterFilterByAttribute(ctx)

    # Exit a parse tree produced by UnifiedIRParser#filterByAttribute.
    def exitFilterByAttribute(self, ctx: UnifiedIRParser.FilterByAttributeContext):
        ctx.parentCtx.slots["nodeProperty"] = "{}.{} {} {}".format(
            "{}", ctx.slots["attribute"], ctx.slots["symOP"], ctx.slots["value"]
        )
        return super().exitFilterByAttribute(ctx)

    # Enter a parse tree produced by UnifiedIRParser#filterByPredicate.
    def enterFilterByPredicate(self, ctx: UnifiedIRParser.FilterByPredicateContext):
        ctx.slots = strictDict({"predicate": None, "direction": None, "edge_var": ""})
        return super().enterFilterByPredicate(ctx)

    # Exit a parse tree produced by UnifiedIRParser#filterByPredicate.
    def exitFilterByPredicate(self, ctx: UnifiedIRParser.FilterByPredicateContext):
        ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"]
        ctx.parentCtx.slots["direction"] = ctx.slots["direction"]
        ctx.parentCtx.slots["edge_var"] = ctx.slots["edge_var"]
        return super().exitFilterByPredicate(ctx)

    # Enter a parse tree produced by UnifiedIRParser#filterByQualifier.
    def enterFilterByQualifier(self, ctx: UnifiedIRParser.FilterByQualifierContext):
        ctx.slots = strictDict({"qualifier": "", "symOP": "", "value": ""})
        return super().enterFilterByQualifier(ctx)

    # Exit a parse tree produced by UnifiedIRParser#filterByQualifier.
    def exitFilterByQualifier(self, ctx: UnifiedIRParser.FilterByQualifierContext):
        ctx.parentCtx.slots["relationshipProperty"] = "{}.{} {} {}".format(
            "{}", ctx.slots["qualifier"], ctx.slots["symOP"], ctx.slots["value"]
        )
        return super().exitFilterByQualifier(ctx)

    # Enter a parse tree produced by UnifiedIRParser#forward.
    def enterForward(self, ctx: UnifiedIRParser.ForwardContext):
        return super().enterForward(ctx)

    # Exit a parse tree produced by UnifiedIRParser#forward.
    def exitForward(self, ctx: UnifiedIRParser.ForwardContext):
        ctx.parentCtx.slots["direction"] = "forward"
        return super().exitForward(ctx)

    # Enter a parse tree produced by UnifiedIRParser#backward.
    def enterBackward(self, ctx: UnifiedIRParser.BackwardContext):
        return super().enterBackward(ctx)

    # Exit a parse tree produced by UnifiedIRParser#backward.
    def exitBackward(self, ctx: UnifiedIRParser.BackwardContext):
        ctx.parentCtx.slots["direction"] = "backward"
        return super().exitBackward(ctx)

    # Enter a parse tree produced by UnifiedIRParser#and.
    def enterAnd(self, ctx: UnifiedIRParser.AndContext):
        ctx.slots = strictDict({"setOP": "AND"})
        return super().enterAnd(ctx)

    # Exit a parse tree produced by UnifiedIRParser#and.
    def exitAnd(self, ctx: UnifiedIRParser.AndContext):
        ctx.parentCtx.slots["setOP"] = ctx.slots["setOP"]
        return super().exitAnd(ctx)

    # Enter a parse tree produced by UnifiedIRParser#or.
    def enterOr(self, ctx: UnifiedIRParser.OrContext):
        ctx.slots = strictDict({"setOP": "OR"})
        return super().enterOr(ctx)

    # Exit a parse tree produced by UnifiedIRParser#or.
    def exitOr(self, ctx: UnifiedIRParser.OrContext):
        ctx.parentCtx.slots["setOP"] = ctx.slots["setOP"]
        return super().exitOr(ctx)

    # Enter a parse tree produced by UnifiedIRParser#not.
    def enterNot(self, ctx: UnifiedIRParser.NotContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#not.
    def exitNot(self, ctx: UnifiedIRParser.NotContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#notEqual.
    def enterNotEqual(self, ctx: UnifiedIRParser.NotEqualContext):
        ctx.slots = strictDict({"symOP": "<>"})
        return super().enterNotEqual(ctx)

    # Exit a parse tree produced by UnifiedIRParser#notEqual.
    def exitNotEqual(self, ctx: UnifiedIRParser.NotEqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitNotEqual(ctx)

    # Enter a parse tree produced by UnifiedIRParser#equal.
    def enterEqual(self, ctx: UnifiedIRParser.EqualContext):
        ctx.slots = strictDict({"symOP": "="})
        return super().enterEqual(ctx)

    # Exit a parse tree produced by UnifiedIRParser#equal.
    def exitEqual(self, ctx: UnifiedIRParser.EqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitEqual(ctx)

    # Enter a parse tree produced by UnifiedIRParser#larger.
    def enterLarger(self, ctx: UnifiedIRParser.LargerContext):
        ctx.slots = strictDict({"symOP": ">"})
        return super().enterLarger(ctx)

    # Exit a parse tree produced by UnifiedIRParser#larger.
    def exitLarger(self, ctx: UnifiedIRParser.LargerContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitLarger(ctx)

    # Enter a parse tree produced by UnifiedIRParser#smaller.
    def enterSmaller(self, ctx: UnifiedIRParser.SmallerContext):
        ctx.slots = strictDict({"symOP": "<"})
        return super().enterSmaller(ctx)

    # Exit a parse tree produced by UnifiedIRParser#smaller.
    def exitSmaller(self, ctx: UnifiedIRParser.SmallerContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitSmaller(ctx)

    # Enter a parse tree produced by UnifiedIRParser#largerEqual.
    def enterLargerEqual(self, ctx: UnifiedIRParser.LargerEqualContext):
        ctx.slots = strictDict({"symOP": ">="})
        return super().enterLargerEqual(ctx)

    # Exit a parse tree produced by UnifiedIRParser#largerEqual.
    def exitLargerEqual(self, ctx: UnifiedIRParser.LargerEqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitLargerEqual(ctx)

    # Enter a parse tree produced by UnifiedIRParser#smallerEqual.
    def enterSmallerEqual(self, ctx: UnifiedIRParser.SmallerEqualContext):
        ctx.slots = strictDict({"symOP": "<="})
        return super().enterSmallerEqual(ctx)

    # Exit a parse tree produced by UnifiedIRParser#smallerEqual.
    def exitSmallerEqual(self, ctx: UnifiedIRParser.SmallerEqualContext):
        ctx.parentCtx.slots["symOP"] = ctx.slots["symOP"]
        return super().exitSmallerEqual(ctx)

    # Enter a parse tree produced by UnifiedIRParser#largest.
    def enterLargest(self, ctx: UnifiedIRParser.LargestContext):
        ctx.slots = strictDict({"stringOP": "largest"})
        return super().enterLargest(ctx)

    # Exit a parse tree produced by UnifiedIRParser#largest.
    def exitLargest(self, ctx: UnifiedIRParser.LargestContext):
        ctx.parentCtx.slots["stringOP"] = ctx.slots["stringOP"]
        return super().exitLargest(ctx)

    # Enter a parse tree produced by UnifiedIRParser#smallest.
    def enterSmallest(self, ctx: UnifiedIRParser.SmallestContext):
        ctx.slots = strictDict({"stringOP": "largest"})
        return super().enterSmallest(ctx)

    # Exit a parse tree produced by UnifiedIRParser#smallest.
    def exitSmallest(self, ctx: UnifiedIRParser.SmallestContext):
        ctx.parentCtx.slots["stringOP"] = ctx.slots["stringOP"]
        return super().exitSmallest(ctx)

    # Enter a parse tree produced by UnifiedIRParser#sum.
    def enterSum(self, ctx: UnifiedIRParser.SumContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#sum.
    def exitSum(self, ctx: UnifiedIRParser.SumContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#average.
    def enterAverage(self, ctx: UnifiedIRParser.AverageContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#average.
    def exitAverage(self, ctx: UnifiedIRParser.AverageContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#valueByUnion.
    def enterValueByUnion(self, ctx: UnifiedIRParser.ValueByUnionContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#valueByUnion.
    def exitValueByUnion(self, ctx: UnifiedIRParser.ValueByUnionContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#valueByAggregate.
    def enterValueByAggregate(self, ctx: UnifiedIRParser.ValueByAggregateContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#valueByAggregate.
    def exitValueByAggregate(self, ctx: UnifiedIRParser.ValueByAggregateContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#valueByAttribute.
    def enterValueByAttribute(self, ctx: UnifiedIRParser.ValueByAttributeContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#valueByAttribute.
    def exitValueByAttribute(self, ctx: UnifiedIRParser.ValueByAttributeContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#valueAtom.
    def enterValueAtom(self, ctx: UnifiedIRParser.ValueAtomContext):
        ctx.slots = strictDict({"valueType": "", "value": ""})
        return super().enterValueAtom(ctx)

    # Exit a parse tree produced by UnifiedIRParser#valueAtom.
    def exitValueAtom(self, ctx: UnifiedIRParser.ValueAtomContext):
        if isinstance(ctx.parentCtx, UnifiedIRParser.FilterByAttributeContext):
            if ctx.slots["valueType"] == "text":
                ctx.parentCtx.slots["value"] = valid_str(ctx.slots["value"])
            else:
                ctx.parentCtx.slots["value"] = ctx.slots["value"]
        elif isinstance(ctx.parentCtx, UnifiedIRParser.FilterByQualifierContext):
            if ctx.slots["valueType"] == "text":
                ctx.parentCtx.slots["value"] = valid_str(ctx.slots["value"])
            else:
                ctx.parentCtx.slots["value"] = ctx.slots["value"]

        return super().exitValueAtom(ctx)

    # Enter a parse tree produced by UnifiedIRParser#text.
    def enterText(self, ctx: UnifiedIRParser.TextContext):
        ctx.slots = strictDict({"string": ctx.getText()})
        return super().enterText(ctx)

    # Exit a parse tree produced by UnifiedIRParser#text.
    def exitText(self, ctx: UnifiedIRParser.TextContext):
        ctx.parentCtx.slots["valueType"] = ctx.slots["string"]
        return super().exitNumber(ctx)

    # Enter a parse tree produced by UnifiedIRParser#quantity.
    def enterQuantity(self, ctx: UnifiedIRParser.QuantityContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#quantity.
    def exitQuantity(self, ctx: UnifiedIRParser.QuantityContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#date.
    def enterDate(self, ctx: UnifiedIRParser.DateContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#date.
    def exitDate(self, ctx: UnifiedIRParser.DateContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#Month.
    def enterMonth(self, ctx: UnifiedIRParser.MonthContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#Month.
    def exitMonth(self, ctx: UnifiedIRParser.MonthContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#year.
    def enterYear(self, ctx: UnifiedIRParser.YearContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#year.
    def exitYear(self, ctx: UnifiedIRParser.YearContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#time.
    def enterTime(self, ctx: UnifiedIRParser.TimeContext):
        pass

    # Exit a parse tree produced by UnifiedIRParser#time.
    def exitTime(self, ctx: UnifiedIRParser.TimeContext):
        pass

    # Enter a parse tree produced by UnifiedIRParser#entity.
    def enterEntity(self, ctx: UnifiedIRParser.EntityContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterEntity(ctx)

    # Exit a parse tree produced by UnifiedIRParser#entity.
    def exitEntity(self, ctx: UnifiedIRParser.EntityContext):
        ctx.parentCtx.slots["entity"] = valid_str(ctx.slots["string"])
        return super().exitEntity(ctx)

    # Enter a parse tree produced by UnifiedIRParser#attribute.
    def enterAttribute(self, ctx: UnifiedIRParser.AttributeContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterAttribute(ctx)

    # Exit a parse tree produced by UnifiedIRParser#attribute.
    def exitAttribute(self, ctx: UnifiedIRParser.AttributeContext):
        if isinstance(ctx.parentCtx, UnifiedIRParser.AttributeQueryContext):
            ctx.parentCtx.slots["query_attr"] = valid_var(ctx.slots["string"])
        else:
            ctx.parentCtx.slots["attribute"] = valid_var(ctx.slots["string"])
        return super().exitAttribute(ctx)

    # Enter a parse tree produced by UnifiedIRParser#concept.
    def enterConcept(self, ctx: UnifiedIRParser.ConceptContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterConcept(ctx)

    # Exit a parse tree produced by UnifiedIRParser#concept.
    def exitConcept(self, ctx: UnifiedIRParser.ConceptContext):
        ctx.parentCtx.slots["concept"] = valid_var(ctx.slots["string"])
        return super().exitConcept(ctx)

    # Enter a parse tree produced by UnifiedIRParser#predicate.
    def enterPredicate(self, ctx: UnifiedIRParser.PredicateContext):
        ctx.slots = strictDict({"string": "", "var": "r1"})
        return super().enterPredicate(ctx)

    # Exit a parse tree produced by UnifiedIRParser#predicate.
    def exitPredicate(self, ctx: UnifiedIRParser.PredicateContext):
        ctx.parentCtx.slots["predicate"] = valid_var(ctx.slots["string"])
        ctx.parentCtx.slots["edge_var"] = ctx.slots["var"]
        return super().exitPredicate(ctx)

    # Enter a parse tree produced by UnifiedIRParser#qualifier.
    def enterQualifier(self, ctx: UnifiedIRParser.QualifierContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterQualifier(ctx)

    # Exit a parse tree produced by UnifiedIRParser#qualifier.
    def exitQualifier(self, ctx: UnifiedIRParser.QualifierContext):
        if isinstance(ctx.parentCtx, UnifiedIRParser.QualifierQueryContext):
            ctx.parentCtx.slots["query_attr"] = valid_var(ctx.slots["string"])
        else:
            ctx.parentCtx.slots["qualifier"] = valid_var(ctx.slots["string"])

    # Enter a parse tree produced by UnifiedIRParser#value.
    def enterValue(self, ctx: UnifiedIRParser.ValueContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterValue(ctx)

    # Exit a parse tree produced by UnifiedIRParser#value.
    def exitValue(self, ctx: UnifiedIRParser.ValueContext):
        ctx.parentCtx.slots["value"] = ctx.slots["string"]
        return super().exitValue(ctx)

    # Enter a parse tree produced by UnifiedIRParser#number.
    def enterNumber(self, ctx: UnifiedIRParser.NumberContext):
        return super().enterNumber(ctx)

    # Exit a parse tree produced by UnifiedIRParser#number.
    def exitNumber(self, ctx: UnifiedIRParser.NumberContext):
        return super().exitNumber(ctx)

    # Enter a parse tree produced by UnifiedIRParser#string.
    def enterString(self, ctx: UnifiedIRParser.StringContext):
        ctx.slots = strictDict({"string": ctx.getText()})
        return super().enterString(ctx)

    # Exit a parse tree produced by UnifiedIRParser#string.
    def exitString(self, ctx: UnifiedIRParser.StringContext):
        ctx.parentCtx.slots["string"] = ctx.slots["string"]
        return super().exitString(ctx)


