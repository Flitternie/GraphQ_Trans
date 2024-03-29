import os
import re
from antlr4 import *

from graphq_trans.ir.IRLexer import IRLexer
from graphq_trans.ir.IRParser import IRParser
from graphq_trans.ir.IRParserListener import IRParserListener

from graphq_trans.utils import *
from graphq_trans.ir.misc import *

class SparqlEmitter(IRParserListener):
    def __init__(self):
        self.output = ""
        try:
            self.value_typing = ValueTyping(os.path.join("./data/kqapro/data/", 'kb.json'))
        except:
            pass
            
        self.ambiguous_qualifiers = [
            "point in time", 
            "inception", 
            "start time",
            "end time",
            "dissolved, abolished or demolished",
            "work period (start)",
            "public domain date", 
            "publication date",
            "date of birth",
            "date of death"
        ]

        self.skeleton = {
            "entityQuery": "SELECT DISTINCT ?e WHERE {{ {} }}",
            "attributeQuery": "SELECT DISTINCT ?pv WHERE {{ {} }}",
            "predicateQuery": "SELECT DISTINCT ?p WHERE {{ {} }}",
            "qualifierQuery": "SELECT DISTINCT ?qpv WHERE {{ {} }}",
            "countQuery": "SELECT (COUNT(DISTINCT ?e) AS ?count) WHERE {{ {} }}",
            "verifyQuery": "ASK {{ {} }}",
            "selectQuery": "SELECT ?e WHERE {{ {} }} ORDER BY {} LIMIT {}"
        }
    
    def initialize(self):
        self.output = ""

    def emit(self, ctx):
        return self.output
    
    def get_value_type(self, key, value=None):
        try:
            v_type = self.value_typing.key_type[key]
            if key in self.ambiguous_qualifiers and v_type == "date" and re.match(r"-?[0-9]{3,4}(?!.)", value):
                return "year"
            return v_type
        except:
            return "string"
    
    def get_value_unit(self, value, value_type):
        if value_type == "quantity":
            if ' ' in value:
                vs = value.split()
                value = vs[0]
                unit = ' '.join(vs[1:])
            else:
                unit = '1'
        else:
            unit = None
        return value, unit

    def enterRoot(self, ctx: IRParser.RootContext):
        self.initialize()
        ctx.slots = strictDict({"query": ""})
        return super().enterRoot(ctx)

    def exitRoot(self, ctx: IRParser.RootContext):
        self.output = ctx.slots["query"]
        return super().exitRoot(ctx)
    
    def enterEntityQuery(self, ctx: IRParser.EntityQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "orderBy": ""})
        return super().enterEntityQuery(ctx)
    
    def exitEntityQuery(self, ctx: IRParser.EntityQueryContext):
        subqueries = reduce_variable(ctx.slots["entitySet"])
        ctx.parentCtx.slots["query"] = self.skeleton["entityQuery"].format(subqueries)
        if ctx.slots["orderBy"] != "":
            ctx.parentCtx.slots["query"] = \
                ctx.parentCtx.slots["query"] + " ORDER BY " + ctx.slots["orderBy"].format("?v") + " LIMIT 1"
        return super().exitEntityQuery(ctx)
    
    def enterAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        ctx.slots = strictDict({"attribute": "", "entitySet": entitySet()})
        return super().enterAttributeQuery(ctx)
    
    def exitAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        subqueries = append_attribute_value_query(ctx.slots["entitySet"], ctx.slots["attribute"])
        ctx.parentCtx.slots["query"] = self.skeleton["attributeQuery"].format(subqueries)
        return super().exitAttributeQuery(ctx)
    
    def enterPredicateQuery(self, ctx: IRParser.PredicateQueryContext):
        ctx.slots = strictDict({"entitySet": []})
        return super().enterPredicateQuery(ctx)
    
    def exitPredicateQuery(self, ctx: IRParser.PredicateQueryContext):
        # ctx.slots["entitySet"][0], ctx.slots["entitySet"][1] = replace_duplicate_variables(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1], same_sub=False)
        # subqueries = ctx.slots["entitySet"][0] + ctx.slots["entitySet"][1] + '?e_1 ?p ?e_2 . '
        subqueries = gen_relation_query(sbj_sparql=ctx.slots["entitySet"][0], sbj_variable='?e_1', obj_sparql=ctx.slots["entitySet"][1], obj_variable='?e_2')
        ctx.parentCtx.slots["query"] = self.skeleton["predicateQuery"].format(subqueries)
        return super().exitPredicateQuery(ctx)
    
    def enterQualifierQuery(self, ctx: IRParser.QualifierQueryContext):
        ctx.slots = strictDict({"qualifier": "", "verify": "", "factNode": ""})
        return super().enterQualifierQuery(ctx)
    
    def exitQualifierQuery(self, ctx: IRParser.QualifierQueryContext):
        subqueries = append_attribute_value_query(ctx.slots["verify"], ctx.slots["qualifier"], e=ctx.slots["factNode"], in_qualifier=True)
        ctx.parentCtx.slots["query"] = self.skeleton["qualifierQuery"].format(subqueries)
        return super().exitQualifierQuery(ctx)
    
    def enterCountQuery(self, ctx: IRParser.CountQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet()})
        return super().enterCountQuery(ctx)
    
    def exitCountQuery(self, ctx: IRParser.CountQueryContext):
        subqueries = reduce_variable(ctx.slots["entitySet"])
        ctx.parentCtx.slots["query"] = self.skeleton["countQuery"].format(subqueries)
        return super().exitCountQuery(ctx)
    
    def enterVerifyQuery(self, ctx: IRParser.VerifyQueryContext):
        ctx.slots = strictDict({"verify": ""})
        return super().enterVerifyQuery(ctx)
    
    def exitVerifyQuery(self, ctx: IRParser.VerifyQueryContext):
        subqueries = ctx.slots["verify"]
        ctx.parentCtx.slots["query"] = self.skeleton["verifyQuery"].format(subqueries)
        return super().exitVerifyQuery(ctx)
    
    def enterSelectQuery(self, ctx: IRParser.SelectQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "attribute": "", "orderBy": "", "number": ""})
        return super().enterSelectQuery(ctx)
    
    def exitSelectQuery(self, ctx: IRParser.SelectQueryContext):
        subqueries = append_attribute_value_query(ctx.slots["entitySet"], ctx.slots["attribute"], 'quantity')
        subqueries = reduce_variable(subqueries)
        ctx.parentCtx.slots["query"] = self.skeleton["selectQuery"].format(subqueries, ctx.slots["orderBy"].format('?v'), ctx.slots["number"])
        return super().exitSelectQuery(ctx)

    def enterVerifyByAttribute(self, ctx: IRParser.VerifyByAttributeContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "attribute": "", "op": "=", "valueType": "", "value": "", "qualifierFilter": {}})
        return super().enterVerifyByAttribute(ctx)
    
    def exitVerifyByAttribute(self, ctx: IRParser.VerifyByAttributeContext):
        ctx.slots["valueType"] = ctx.slots["valueType"] if ctx.slots["valueType"] != "" else self.get_value_type(ctx.slots["attribute"], ctx.slots["value"])
        ctx.slots["value"], v_unit = self.get_value_unit(ctx.slots["value"], ctx.slots["valueType"])

        subqueries = ctx.slots["entitySet"]
        subqueries, _ = replace_variable(subqueries, '?pv')
        subqueries, _ = replace_variable(subqueries, '?v')
        
        subqueries += gen_attribute_query(ctx.slots["attribute"], ctx.slots["value"], ctx.slots["valueType"], v_unit, ctx.slots["op"])
        fact_node = gen_attr_fact_node(ctx.slots["attribute"])
        
        if isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            ctx.parentCtx.slots["verify"] = subqueries
            ctx.parentCtx.slots["factNode"] = fact_node
        elif isinstance(ctx.parentCtx, IRParser.VerifyQueryContext):
            if ctx.slots["qualifierFilter"] != {}:
                subqueries, _ = replace_variable(subqueries, '?qpv')
                subqueries, _ = replace_variable(subqueries, '?qv')
                ctx.slots["qualifierFilter"]["valueType"] = ctx.slots["qualifierFilter"]["valueType"] if ctx.slots["qualifierFilter"]["valueType"] != "" else self.get_value_type(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"])
                ctx.slots["qualifierFilter"]["value"], qv_unit = self.get_value_unit(ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"])
                subqueries += gen_attribute_query(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"], qv_unit, ctx.slots["qualifierFilter"]["op"], e=fact_node, in_qualifier=True)
            ctx.parentCtx.slots["verify"] = subqueries
        else:
            raise Exception("Unexpected context")
        
        return super().exitVerifyByAttribute(ctx)

    def enterVerifyByPredicate(self, ctx: IRParser.VerifyByPredicateContext):
        ctx.slots = strictDict({"entitySet": [], "predicate": "", "direction": "", "qualifierFilter": {}})
        return super().enterVerifyByPredicate(ctx)

    def exitVerifyByPredicate(self, ctx: IRParser.VerifyByPredicateContext):
        ctx.slots["direction"] = ctx.slots["direction"] if ctx.slots["direction"] != "" else "forward"

        # ctx.slots["entitySet"][0], ctx.slots["entitySet"][1] = replace_duplicate_variables(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1], same_sub=False)
        # ctx.parentCtx.slots["verify"] = ctx.slots["entitySet"][0] + ctx.slots["entitySet"][1] + '?e_1 <{}> ?e_2 . '.format(legal(ctx.slots["predicate"]))
        subqueries = gen_relation_query(sbj_sparql=ctx.slots["entitySet"][0], sbj_variable='?e_1', obj_sparql=ctx.slots["entitySet"][1], obj_variable='?e_2', pred=ctx.slots["predicate"], direction=ctx.slots["direction"])
        fact_node = gen_rel_fact_node(ctx.slots["predicate"], ctx.slots["direction"], '?e_1', '?e_2')
        
        if isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            ctx.parentCtx.slots["verify"] = subqueries
            ctx.parentCtx.slots["factNode"] = fact_node
        elif isinstance(ctx.parentCtx, IRParser.VerifyQueryContext):
            if ctx.slots["qualifierFilter"] != {}:
                subqueries, _ = replace_variable(subqueries, '?qpv')
                subqueries, _ = replace_variable(subqueries, '?qv')
                ctx.slots["qualifierFilter"]["valueType"] = ctx.slots["qualifierFilter"]["valueType"] if ctx.slots["qualifierFilter"]["valueType"] != "" else self.get_value_type(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"])        
                ctx.slots["qualifierFilter"]["value"], qv_unit = self.get_value_unit(ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"])
                subqueries += gen_attribute_query(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"], qv_unit, ctx.slots["qualifierFilter"]["op"], e=fact_node, in_qualifier=True)
            ctx.parentCtx.slots["verify"] = subqueries
        else:
            raise Exception("Unexpected context")
        
        return super().exitVerifyByPredicate(ctx)

    def enterEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        ctx.slots = strictDict({"entitySet": [], "setOP": ""})
        return super().enterEntitySetGroup(ctx)
    
    def exitEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        if ctx.slots["setOP"] == "and":
            insert(ctx.parentCtx, and_two_descriptions(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1], same_concept(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1])))
        elif ctx.slots["setOP"] == "or":
            insert(ctx.parentCtx, or_two_descriptions(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1], same_concept(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1])))
        else:
            raise Exception("Unexpected set operator")
        return super().exitEntitySetGroup(ctx)
    
    def enterEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        ctx.slots = strictDict({"entitySet": []})
        return super().enterEntitySetIntersect(ctx)
    
    def exitEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        insert(ctx.parentCtx, and_two_descriptions(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1], same_concept(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1])))
        return super().exitEntitySetIntersect(ctx)
    
    def enterEntitySetFilter(self, ctx: IRParser.EntitySetFilterContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "orderBy": ""})
        return super().enterEntitySetFilter(ctx)
    
    def exitEntitySetFilter(self, ctx: IRParser.EntitySetFilterContext):
        insert(ctx.parentCtx, ctx.slots["entitySet"], concept=ctx.slots["entitySet"].concept)
        if ctx.slots["orderBy"] != "":
            context = ctx.parentCtx
            while not isinstance(context, IRParser.RootContext):
                if "orderBy" in context.slots:
                    context.slots["orderBy"] = ctx.slots["orderBy"]
                    break
                context = context.parentCtx
        return super().exitEntitySetFilter(ctx)
    
    def enterEntitySetPlaceholder(self, ctx: IRParser.EntitySetPlaceholderContext):
        return super().enterEntitySetPlaceholder(ctx)
    
    def exitEntitySetPlaceholder(self, ctx: IRParser.EntitySetPlaceholderContext):
        return super().exitEntitySetPlaceholder(ctx)

    def enterEntitySetAtom(self, ctx: IRParser.EntitySetAtomContext):
        ctx.slots = strictDict({"entity": ""})
        return super().enterEntitySetAtom(ctx)
    
    def exitEntitySetAtom(self, ctx: IRParser.EntitySetAtomContext):
        insert(ctx.parentCtx, gen_name_query(ctx.slots["entity"]))
        return super().exitEntitySetAtom(ctx)

    def enterEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        ctx.slots = strictDict({"concept": "", "entitySet": entitySet(), "attribute": "", "op": "", "valueType": "", "value": "", "qualifierFilter": {}})
        return super().enterEntitySetByAttribute(ctx)
    
    def exitEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        ctx.slots["valueType"] = ctx.slots["valueType"] if ctx.slots["valueType"] != "" else self.get_value_type(ctx.slots["attribute"], ctx.slots["value"])
        ctx.slots["value"], v_unit = self.get_value_unit(ctx.slots["value"], ctx.slots["valueType"])

        subqueries = gen_concept_query(ctx.slots["concept"]) if ctx.slots["concept"] != "" else ""
        subqueries += gen_attribute_query(ctx.slots["attribute"], ctx.slots["value"], ctx.slots["valueType"], v_unit, ctx.slots["op"])

        if ctx.slots["qualifierFilter"] != {}:
            fact_node = gen_attr_fact_node(ctx.slots["attribute"])
            ctx.slots["qualifierFilter"]["valueType"] = ctx.slots["qualifierFilter"]["valueType"] if ctx.slots["qualifierFilter"]["valueType"] != "" else self.get_value_type(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"])       
            ctx.slots["qualifierFilter"]["value"], qv_unit = self.get_value_unit(ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"])
            subqueries += gen_attribute_query(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"], qv_unit, ctx.slots["qualifierFilter"]["op"], e=fact_node, in_qualifier=True)

        if ctx.slots["entitySet"]:
            insert(ctx.parentCtx, and_two_descriptions(ctx.slots["entitySet"], subqueries, same_concept(ctx.slots["concept"], ctx.slots["entitySet"])), concept=ctx.slots["concept"])
        else:
            insert(ctx.parentCtx, subqueries, concept=ctx.slots["concept"])
        return super().exitEntitySetByAttribute(ctx)
    
    def enterEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        ctx.slots = strictDict({"concept": "", "entitySet": [], "predicate": "", "direction": "", "qualifierFilter": {}})
        return super().enterEntitySetByPredicate(ctx)
    
    def exitEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        ctx.slots["direction"] = ctx.slots["direction"] if ctx.slots["direction"] != "" else "forward"        
        subqueries = gen_concept_query(ctx.slots["concept"]) if ctx.slots["concept"] != "" else ""
        
        if len(ctx.slots["entitySet"]) == 2:
            if diff_concept(ctx.slots["entitySet"][0], ctx.slots["entitySet"][1]):
                new_query, _ = replace_variable(ctx.slots["entitySet"][1], "?c")
                ctx.slots["entitySet"][1] = ctx.slots["entitySet"][1].reassign(new_query)
            sbj_variable, obj_variable = '?e_1', '?e_2'
            # ctx.slots["entitySet"][1], obj_variable = replace_variable(ctx.slots["entitySet"][1], "?e")
            subqueries += gen_relation_query(sbj_sparql=ctx.slots["entitySet"][0], sbj_variable=sbj_variable, obj_sparql=ctx.slots["entitySet"][1], obj_variable=obj_variable, pred=ctx.slots["predicate"], direction=ctx.slots["direction"])
        elif len(ctx.slots["entitySet"]) == 1:
            if diff_concept(ctx.slots["concept"], ctx.slots["entitySet"][0]):
                new_query, _ = replace_variable(ctx.slots["entitySet"][0], "?c")
                ctx.slots["entitySet"][0] = ctx.slots["entitySet"][0].reassign(new_query)
            ctx.slots["entitySet"][0] = ctx.slots["entitySet"][0].reassign(reduce_variable(ctx.slots["entitySet"][0]))
            sbj_variable = '?e'
            new_query, obj_variable = replace_variable(ctx.slots["entitySet"][0], "?e")
            ctx.slots["entitySet"][0] = ctx.slots["entitySet"][0].reassign(new_query)
            subqueries += gen_relation_query(sbj_sparql=None, sbj_variable=sbj_variable, obj_sparql=ctx.slots["entitySet"][0], obj_variable=obj_variable, pred=ctx.slots["predicate"], direction=ctx.slots["direction"])
        else:
            raise Exception("Unexpected number of entitySet")
        
        if ctx.slots["qualifierFilter"] != {}:
            fact_node = gen_rel_fact_node(ctx.slots["predicate"], ctx.slots["direction"], sbj_variable, obj_variable)
            ctx.slots["qualifierFilter"]["valueType"] = ctx.slots["qualifierFilter"]["valueType"] if ctx.slots["qualifierFilter"]["valueType"] != "" else self.get_value_type(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"])
            ctx.slots["qualifierFilter"]["value"], qv_unit = self.get_value_unit(ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"])
            subqueries += gen_attribute_query(ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"], ctx.slots["qualifierFilter"]["valueType"], qv_unit, ctx.slots["qualifierFilter"]["op"], e=fact_node, in_qualifier=True)

        if ctx.slots["entitySet"][0].concept:
            ctx.slots["concept"] = ctx.slots["entitySet"][0].concept

        insert(ctx.parentCtx, subqueries, concept=ctx.slots["concept"])
        return super().exitEntitySetByPredicate(ctx)
    
    def enterEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        ctx.slots = strictDict({"concept": "", "entitySet": entitySet()})
        return super().enterEntitySetByConcept(ctx)
    
    def exitEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        subqueries = gen_concept_query(ctx.slots["concept"]) if ctx.slots["concept"] != "" else ""
        
        if ctx.slots["entitySet"]:
            insert(ctx.parentCtx, and_two_descriptions(ctx.slots["entitySet"], subqueries, same_concept(ctx.slots["concept"], ctx.slots["entitySet"])), concept=ctx.slots["concept"])
        else:
            insert(ctx.parentCtx, subqueries, concept=ctx.slots["concept"])
        return super().exitEntitySetByConcept(ctx)

    def enterEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "number": "1", "attribute": "", "orderBy": ""})
        return super().enterEntitySetByRank(ctx)

    def exitEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        insert(ctx.parentCtx,
               append_attribute_value_query(ctx.slots["entitySet"], ctx.slots["attribute"], "quantity"),
               concept=ctx.slots["entitySet"].concept)
        if ctx.slots["orderBy"] != "":
            ctx.parentCtx.slots["orderBy"] = ctx.slots["orderBy"]
        return super().exitEntitySetByRank(ctx)

    def enterFilterByRank(self, ctx: IRParser.FilterByRankContext):
        ctx.slots = strictDict({"number": "1", "attribute": ""})
        return super().enterFilterByRank(ctx)
    
    def exitFilterByRank(self, ctx: IRParser.FilterByRankContext):
        ctx.parentCtx.slots["number"] = ctx.slots["number"]
        ctx.parentCtx.slots["attribute"] = ctx.slots["attribute"]
        return super().exitFilterByRank(ctx)

    def enterFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        ctx.slots = strictDict({"attribute": "", "op": "=", "valueType":"", "value": ""})
        return super().enterFilterByAttribute(ctx)
    
    def exitFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        ctx.parentCtx.slots["attribute"] = ctx.slots["attribute"]
        ctx.parentCtx.slots["op"] = ctx.slots["op"]
        ctx.parentCtx.slots["valueType"] = ctx.slots["valueType"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"]
        return super().exitFilterByAttribute(ctx)

    def enterFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        ctx.slots = strictDict({"predicate": "", "direction": ""})
        return super().enterFilterByPredicate(ctx)
    
    def exitFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"]
        ctx.parentCtx.slots["direction"] = ctx.slots["direction"]
        return super().exitFilterByPredicate(ctx)

    def enterFilterByQualifier(self, ctx: IRParser.FilterByQualifierContext):
        ctx.slots = strictDict({"qualifier": "", "op": "=", "valueType":"", "value": ""})
        return super().enterFilterByQualifier(ctx)
    
    def exitFilterByQualifier(self, ctx: IRParser.FilterByQualifierContext):
        ctx.parentCtx.slots["qualifierFilter"]["qualifier"] = ctx.slots["qualifier"]
        ctx.parentCtx.slots["qualifierFilter"]["op"] = ctx.slots["op"]
        ctx.parentCtx.slots["qualifierFilter"]["valueType"] = ctx.slots["valueType"]
        ctx.parentCtx.slots["qualifierFilter"]["value"] = ctx.slots["value"]
        return super().exitFilterByQualifier(ctx)

    def enterValueAtom(self, ctx: IRParser.ValueAtomContext):
        ctx.slots = strictDict({"valueType": "", "value": ""})
        return super().enterValueAtom(ctx)
    
    def exitValueAtom(self, ctx: IRParser.ValueAtomContext):
        ctx.parentCtx.slots["valueType"] = ctx.slots["valueType"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"]
        return super().exitValueAtom(ctx)

    def enterEntity(self, ctx: IRParser.EntityContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterEntity(ctx)
    
    def exitEntity(self, ctx: IRParser.EntityContext):
        ctx.parentCtx.slots["entity"] = ctx.slots["string"]
        return super().exitEntity(ctx)
    
    def enterAttribute(self, ctx: IRParser.AttributeContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterAttribute(ctx)
    
    def exitAttribute(self, ctx: IRParser.AttributeContext):
        ctx.parentCtx.slots["attribute"] = ctx.slots["string"]
        return super().exitAttribute(ctx)
    
    def enterConcept(self, ctx: IRParser.ConceptContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterConcept(ctx)
    
    def exitConcept(self, ctx: IRParser.ConceptContext):
        ctx.parentCtx.slots["concept"] = ctx.slots["string"]
        return super().exitConcept(ctx)
    
    def enterPredicate(self, ctx: IRParser.PredicateContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterPredicate(ctx)
    
    def exitPredicate(self, ctx: IRParser.PredicateContext):
        ctx.parentCtx.slots["predicate"] = ctx.slots["string"]
        return super().exitPredicate(ctx)
    
    def enterQualifier(self, ctx: IRParser.QualifierContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterQualifier(ctx)
    
    def exitQualifier(self, ctx: IRParser.QualifierContext):
        ctx.parentCtx.slots["qualifier"] = ctx.slots["string"]
        return super().exitQualifier(ctx)
    
    def enterValue(self, ctx: IRParser.ValueContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterValue(ctx)
    
    def exitValue(self, ctx: IRParser.ValueContext):
        ctx.parentCtx.slots["value"] = ctx.slots["string"]
        return super().exitValue(ctx)
    

    def exitForward(self, ctx: IRParser.ForwardContext):
        ctx.parentCtx.slots["direction"] = "forward"
        return super().exitForward(ctx)
    
    def exitBackward(self, ctx: IRParser.BackwardContext):
        ctx.parentCtx.slots["direction"] = "backward"
        return super().exitBackward(ctx)
    
    def exitAnd(self, ctx: IRParser.AndContext):
        ctx.parentCtx.slots["setOP"] = "and"
        return super().exitAnd(ctx)
    
    def exitOr(self, ctx: IRParser.OrContext):
        ctx.parentCtx.slots["setOP"] = "or"
        return super().exitOr(ctx)

    def exitEqual(self, ctx: IRParser.EqualContext):
        ctx.parentCtx.slots["op"] = "="
        return super().exitEqual(ctx)
    
    def exitNotEqual(self, ctx: IRParser.NotEqualContext):
        ctx.parentCtx.slots["op"] = "!="
        return super().exitNotEqual(ctx)
    
    def exitLarger(self, ctx: IRParser.LargerContext):
        ctx.parentCtx.slots["op"] = ">"
        return super().exitLarger(ctx)
    
    def exitSmaller(self, ctx: IRParser.SmallerContext):
        ctx.parentCtx.slots["op"] = "<"
        return super().exitSmaller(ctx)
    
    def exitLargerEqual(self, ctx: IRParser.LargerEqualContext):
        ctx.parentCtx.slots["op"] = ">="
        return super().exitLargerEqual(ctx)
    
    def exitSmallerEqual(self, ctx: IRParser.SmallerEqualContext):
        ctx.parentCtx.slots["op"] = "<="
        return super().exitSmallerEqual(ctx)
    
    def exitText(self, ctx: IRParser.TextContext):
        ctx.parentCtx.slots["valueType"] = "string"
        return super().exitText(ctx)
    
    def exitQuantity(self, ctx: IRParser.QuantityContext):
        ctx.parentCtx.slots["valueType"] = "quantity"
        return super().exitQuantity(ctx)

    def exitDate(self, ctx: IRParser.DateContext):
        ctx.parentCtx.slots["valueType"] = "date"
        return super().exitDate(ctx)
    
    def exitMonth(self, ctx: IRParser.MonthContext):
        ctx.parentCtx.slots["valueType"] = "month"
        return super().exitMonth(ctx)
    
    def exitYear(self, ctx: IRParser.YearContext):
        ctx.parentCtx.slots["valueType"] = "year"
        return super().exitYear(ctx)
    
    def exitTime(self, ctx: IRParser.TimeContext):
        ctx.parentCtx.slots["valueType"] = "time"
        return super().exitTime(ctx)
    
    def exitLargest(self, ctx: IRParser.LargestContext):
        ctx.parentCtx.parentCtx.slots["orderBy"] = "DESC({})"
        return super().enterLargest(ctx)
    
    def exitSmallest(self, ctx: IRParser.SmallestContext):
        ctx.parentCtx.parentCtx.slots["orderBy"] = "{}"
        return super().exitSmallest(ctx)


    # def enterTopK(self, ctx: IRParser.TopKContext):
    #     ctx.slots = strictDict({"number": ""})
    #     return super().enterTopK(ctx)

    # def exitTopK(self, ctx: IRParser.TopKContext):
    #     ctx.parentCtx.parentCtx.slots["limit"] = ctx.slots["number"]
    #     return super().exitTopK(ctx)
    
    

    def enterString(self, ctx: IRParser.StringContext):
        if not isinstance(ctx.parentCtx, IRParser.StringContext):
            ctx.parentCtx.slots["string"] = str(ctx.getText())

    def enterNumber(self, ctx: IRParser.NumberContext):
        if not isinstance(ctx.parentCtx, IRParser.NumberContext):
            ctx.parentCtx.slots["number"] = str(ctx.getText())