from antlr4 import *

from graphq_trans.ir.IRLexer import IRLexer
from graphq_trans.ir.IRParser import IRParser
from graphq_trans.ir.IRParserListener import IRParserListener

from graphq_trans.utils import *


class KoplEmitter(IRParserListener):
    def __init__(self):
        self.output = ""
        self.SEP = '<b>'
        
        ARG_SEP = '<c>'
        self.func = { 
            "QueryName": "What()",
            "Count": "Count()",
            "QueryRelation": "QueryRelation()",
            "QueryAttr": "QueryAttr(%s)" % ARG_SEP.join(["{}"]*1),
            "QueryAttrUnderCondition": "QueryAttrUnderCondition(%s)" % ARG_SEP.join(["{}"]*3),
            "Population": "FindAll()",
            "And": "And()",
            "Or": "Or()",
            "FilterEntity": "Find(%s)" % ARG_SEP.join(["{}"]*1),
            "FilterRelation": "Relate(%s)" % ARG_SEP.join(["{}"]*2),
            "FilterRank": "Select(%s)" % ARG_SEP.join(["{}"]*4),
            "FilterConcept": "FilterConcept(%s)" % ARG_SEP.join(["{}"]*1),
            "FilterAttrStr": "FilterStr(%s)" % ARG_SEP.join(["{}"]*2),
            "FilterAttrNum": "FilterNum(%s)" % ARG_SEP.join(["{}"]*3),
            "FilterAttrYear": "FilterYear(%s)" % ARG_SEP.join(["{}"]*3),
            "FilterAttrDate": "FilterDate(%s)" % ARG_SEP.join(["{}"]*3),
            "FilterQualifierStr": "QFilterStr(%s)" % ARG_SEP.join(["{}"]*2),
            "FilterQualifierNum": "QFilterNum(%s)" % ARG_SEP.join(["{}"]*3),
            "FilterQualifierYear": "QFilterYear(%s)" % ARG_SEP.join(["{}"]*3),
            "FilterQualifierDate": "QFilterDate(%s)" % ARG_SEP.join(["{}"]*3),
            "VerifyStr": "VerifyStr(%s)" % ARG_SEP.join(["{}"]*1),
            "VerifyNum": "VerifyNum(%s)" % ARG_SEP.join(["{}"]*2),
            "VerifyYear": "VerifyYear(%s)" % ARG_SEP.join(["{}"]*2),
            "VerifyDate": "VerifyDate(%s)" % ARG_SEP.join(["{}"]*2),
            "QueryQualifierAttr": "QueryAttrQualifier(%s)" % ARG_SEP.join(["{}"]*3),
            "QueryQualifierRelation": "QueryRelationQualifier(%s)" % ARG_SEP.join(["{}"]*2)
        }

        self.stringOP_vocab = { 
            "largest": "largest", 
            "smallest": "smallest", 
            "larger": "greater", 
            "smaller": "less"
        }


    def initialize(self):
        self.output = ""

    def emit(self, ctx):
        return self.output
    
    def reverse(self, direction):
        assert direction in ["forward", "backward"]
        return "forward" if direction == "backward" else "backward"
    
    def enterRoot(self, ctx: IRParser.RootContext):
        self.initialize()
        ctx.slots = strictDict({"query": ""})
        return super().enterRoot(ctx)
    
    def exitRoot(self, ctx: IRParser.RootContext):
        self.output = ctx.slots["query"]
        return super().exitRoot(ctx)
    
    def enterEntityQuery(self, ctx: IRParser.EntityQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet()})
        return super().enterEntityQuery(ctx)
    
    def exitEntityQuery(self, ctx: IRParser.EntityQueryContext):
        ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["QueryName"]
        return super().exitEntityQuery(ctx)
    
    def enterAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "attribute": ""})
        return super().enterAttributeQuery(ctx)
    
    def exitAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["QueryAttr"].format(ctx.slots["attribute"])
        return super().exitAttributeQuery(ctx)
    
    def enterPredicateQuery(self, ctx: IRParser.PredicateQueryContext):
        ctx.slots = strictDict({"entitySet": []})
        return super().enterPredicateQuery(ctx)
    
    def exitPredicateQuery(self, ctx: IRParser.PredicateQueryContext):
        ctx.parentCtx.slots["query"] = ctx.slots["entitySet"][0] + self.SEP + ctx.slots["entitySet"][1] + self.SEP + self.func["QueryRelation"] 
        return super().exitPredicateQuery(ctx)
    
    def enterQualifierQuery(self, ctx: IRParser.QualifierQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "attribute": "", "value": "", "predicate": "",  "qualifier": ""})
        return super().enterQualifierQuery(ctx)
    
    def exitQualifierQuery(self, ctx: IRParser.QualifierQueryContext):
        assert ctx.slots["qualifier"] != ""
        if ctx.slots["attribute"] and ctx.slots["value"] and not ctx.slots["predicate"]:
            ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["QueryQualifierAttr"].format(ctx.slots["attribute"], ctx.slots["value"], ctx.slots["qualifier"])
        elif ctx.slots["predicate"]:
            ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["QueryQualifierRelation"].format(ctx.slots["predicate"], ctx.slots["qualifier"])
        else:
            raise Exception("Unknown qualifier query")
        return super().exitQualifierQuery(ctx)
    
    def enterCountQuery(self, ctx: IRParser.CountQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet()})
        return super().enterCountQuery(ctx)
    
    def exitCountQuery(self, ctx: IRParser.CountQueryContext):
        ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["Count"]
        return super().exitCountQuery(ctx)
    
    def enterVerifyQuery(self, ctx: IRParser.VerifyQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "op": "", "valueType": "", "value": ""}) 
        return super().enterVerifyQuery(ctx)
    
    def exitVerifyQuery(self, ctx: IRParser.VerifyQueryContext):
        if ctx.slots["valueType"] == "string":
            ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["VerifyStr"].format(ctx.slots["value"])
        elif ctx.slots["valueType"] == "quantity":
            ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["VerifyNum"].format(ctx.slots["value"], ctx.slots["op"])
        elif ctx.slots["valueType"] == "year":
            ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["VerifyYear"].format(ctx.slots["value"], ctx.slots["op"])
        elif ctx.slots["valueType"] == "date":
            ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + self.func["VerifyDate"].format(ctx.slots["value"], ctx.slots["op"])
        else:
            raise Exception("Unknown verify query")
        return super().exitVerifyQuery(ctx)
    
    def enterSelectQuery(self, ctx: IRParser.SelectQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "rankFilter": ""})
        return super().enterSelectQuery(ctx)
    
    def exitSelectQuery(self, ctx: IRParser.SelectQueryContext):
        ctx.parentCtx.slots["query"] = ctx.slots["entitySet"] + self.SEP + ctx.slots["rankFilter"] + self.SEP + self.func["QueryName"]
        return super().exitSelectQuery(ctx)
    
    def enterVerifyByAttribute(self, ctx: IRParser.VerifyByAttributeContext):
        if isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            ctx.slots = strictDict({"entitySet": entitySet(), "attribute": "", "value": "", "op": "", "valueType": "", "qualifierFilter": {}})
        elif isinstance(ctx.parentCtx, IRParser.VerifyQueryContext):
            ctx.slots = strictDict({"entitySet": entitySet(), "attribute": "", "value": "", "op": "", "valueType": "", "qualifierFilter": {}})
        else:
            raise Exception("Unexpected parent context")
        return super().enterVerifyByAttribute(ctx)
    
    def exitVerifyByAttribute(self, ctx: IRParser.VerifyByAttributeContext):
        if isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            insert(ctx.parentCtx, ctx.slots["entitySet"])
            ctx.parentCtx.slots["attribute"] = ctx.slots["attribute"]
            ctx.parentCtx.slots["value"] = ctx.slots["value"]
        elif isinstance(ctx.parentCtx, IRParser.VerifyQueryContext):
            if ctx.slots["qualifierFilter"] == {}:
                insert(ctx.parentCtx, ctx.slots["entitySet"] + self.SEP + self.func["QueryAttr"].format(ctx.slots["attribute"]))
            else:
                insert(ctx.parentCtx, ctx.slots["entitySet"] + self.SEP + self.func["QueryAttrUnderCondition"].format(ctx.slots["attribute"], ctx.slots["qualifierFilter"]["qualifier"], ctx.slots["qualifierFilter"]["value"]))
            ctx.parentCtx.slots["value"] = ctx.slots["value"]
            ctx.parentCtx.slots["op"] = ctx.slots["op"]
            ctx.parentCtx.slots["valueType"] = ctx.slots["valueType"]
        return super().exitVerifyByAttribute(ctx)

    def enterVerifyByPredicate(self, ctx: IRParser.VerifyByPredicateContext):
        if isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            ctx.slots = strictDict({"entitySet": [], "predicate": "", "qualifierFilter": ""})
        else:
            raise Exception("Unexpected parent context")
        return super().enterVerifyByPredicate(ctx)
    
    def exitVerifyByPredicate(self, ctx: IRParser.VerifyByPredicateContext):
        if isinstance(ctx.parentCtx, IRParser.QualifierQueryContext):
            insert(ctx.parentCtx, ctx.slots["entitySet"][0] + self.SEP + ctx.slots["entitySet"][1])
            ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"]
        else:
            raise Exception("Unexpected parent context")
        return super().exitVerifyByPredicate(ctx)
    
    def enterEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        ctx.slots = strictDict({"entitySet": [], "setOP": ""})
        return super().enterEntitySetGroup(ctx)

    def exitEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        if ctx.slots["setOP"] == "and":
            insert(ctx.parentCtx, ctx.slots["entitySet"][0] + self.SEP + ctx.slots["entitySet"][1] + self.SEP + self.func["And"])
        elif ctx.slots["setOP"] == "or":
            insert(ctx.parentCtx, ctx.slots["entitySet"][0] + self.SEP + ctx.slots["entitySet"][1] + self.SEP + self.func["Or"])
        else:
            raise Exception("Unexpected set operator")
        return super().exitEntitySetGroup(ctx)    
    
    def enterEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        ctx.slots = strictDict({"entitySet": []})
        return super().enterEntitySetIntersect(ctx)
    
    def exitEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        if ctx.slots["entitySet"][0].is_pop:
            insert(ctx.parentCtx, ctx.slots["entitySet"][1])
        elif ctx.slots["entitySet"][1].is_pop:
            insert(ctx.parentCtx, ctx.slots["entitySet"][0])
        else:
            insert(ctx.parentCtx, ctx.slots["entitySet"][1] + self.SEP + ctx.slots["entitySet"][0] + self.SEP + self.func["And"])
        return super().exitEntitySetIntersect(ctx)

    def enterEntitySetFilter(self, ctx: IRParser.EntitySetFilterContext):
        ctx.slots = strictDict({"entitySet": entitySet()})
        return super().enterEntitySetFilter(ctx)
    
    def exitEntitySetFilter(self, ctx: IRParser.EntitySetFilterContext):
        insert(ctx.parentCtx, ctx.slots["entitySet"])
        return super().exitEntitySetFilter(ctx)

    def enterEntitySetAtom(self, ctx: IRParser.EntitySetAtomContext):
        ctx.slots = strictDict({"entity": ""})
        return super().enterEntitySetAtom(ctx)

    def exitEntitySetAtom(self, ctx: IRParser.EntitySetAtomContext):
        insert(ctx.parentCtx, self.func["FilterEntity"].format(ctx.slots["entity"]), is_atom=True)
        return super().exitEntitySetAtom(ctx)
    
    def exitEntitySetPlaceholder(self, ctx: IRParser.EntitySetPlaceholderContext):
        insert(ctx.parentCtx, self.func["Population"], is_pop=True)
        return super().exitEntitySetPlaceholder(ctx)
    
    def enterEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        ctx.slots = strictDict({"concept": "", "entitySet": entitySet(), "attributeFilter": "", "qualifierFilter": ""})
        return super().enterEntitySetByAttribute(ctx)
    
    def exitEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        assert ctx.slots["attributeFilter"] != ""
        if not ctx.slots["entitySet"]:
            ctx.slots["entitySet"] = entitySet(self.func["Population"], is_pop=True)
        subquery = ctx.slots["entitySet"]
        subquery += self.SEP + ctx.slots["attributeFilter"]
        if ctx.slots["qualifierFilter"]:
            subquery += self.SEP + ctx.slots["qualifierFilter"]
        if ctx.slots["concept"]:
            subquery += self.SEP + self.func["FilterConcept"].format(ctx.slots["concept"])
        insert(ctx.parentCtx, subquery)
        return super().exitEntitySetByAttribute(ctx)
    
    def enterFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        ctx.slots = strictDict({"attribute": "", "op": "", "value": "", "valueType": ""})
        return super().enterFilterByAttribute(ctx)
    
    def exitFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        if isinstance(ctx.parentCtx, IRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["attribute"] = ctx.slots["attribute"]
            ctx.parentCtx.slots["op"] = ctx.slots["op"]
            ctx.parentCtx.slots["value"] = ctx.slots["value"]
            ctx.parentCtx.slots["valueType"] = ctx.slots["valueType"]
        else:
            if ctx.slots["valueType"] == "string":
                ctx.parentCtx.slots["attributeFilter"] = self.func["FilterAttrStr"].format(ctx.slots["attribute"], ctx.slots["value"])
            elif ctx.slots["valueType"] == "quantity":
                ctx.parentCtx.slots["attributeFilter"] = self.func["FilterAttrNum"].format(ctx.slots["attribute"], ctx.slots["value"], ctx.slots["op"])
            elif ctx.slots["valueType"] == "year":
                ctx.parentCtx.slots["attributeFilter"] = self.func["FilterAttrYear"].format(ctx.slots["attribute"], ctx.slots["value"], ctx.slots["op"])
            elif ctx.slots["valueType"] == "date":
                ctx.parentCtx.slots["attributeFilter"] = self.func["FilterAttrDate"].format(ctx.slots["attribute"], ctx.slots["value"], ctx.slots["op"])
            else:
                raise Exception("Unexpected value type")
        return super().exitFilterByAttribute(ctx)
    
    def enterEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        ctx.slots = strictDict({"concept": "", "entitySet": [], "predicateFilter": "", "qualifierFilter": ""})
        return super().enterEntitySetByPredicate(ctx)
    
    def exitEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        assert ctx.slots["predicateFilter"] != ""
        if len(ctx.slots["entitySet"]) == 1:
            subquery = ctx.slots["entitySet"][0] + self.SEP + ctx.slots["predicateFilter"]
        elif ctx.slots["entitySet"][0].is_pop:
            subquery = ctx.slots["entitySet"][1] + self.SEP + ctx.slots["predicateFilter"]
        else:
            subquery = ctx.slots["entitySet"][1] + self.SEP + ctx.slots["predicateFilter"] + self.SEP + ctx.slots["entitySet"][0] 
        if ctx.slots["qualifierFilter"]:
            subquery += self.SEP + ctx.slots["qualifierFilter"]
        if ctx.slots["concept"]:
            subquery += self.SEP + self.func["FilterConcept"].format(ctx.slots["concept"])
        insert(ctx.parentCtx, subquery)
        return super().exitEntitySetByPredicate(ctx)
    
    def enterFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        ctx.slots = strictDict({"predicate": "", "direction": "forward"})
        return super().enterFilterByPredicate(ctx)
    
    def exitFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        if isinstance(ctx.parentCtx, IRParser.VerifyByPredicateContext):
            ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"]
        else:
            ctx.parentCtx.slots["predicateFilter"] = self.func["FilterRelation"].format(ctx.slots["predicate"], self.reverse(ctx.slots["direction"]))
        return super().exitFilterByPredicate(ctx)
    
    def enterFilterByQualifier(self, ctx: IRParser.FilterByQualifierContext):
        ctx.slots = strictDict({"qualifier": "", "op": "", "value": "", "valueType": ""})
        return super().enterFilterByQualifier(ctx)
    
    def exitFilterByQualifier(self, ctx: IRParser.FilterByQualifierContext):
        if isinstance(ctx.parentCtx, IRParser.VerifyByAttributeContext):
            ctx.parentCtx.slots["qualifierFilter"]["qualifier"] = ctx.slots["qualifier"]
            ctx.parentCtx.slots["qualifierFilter"]["op"] = ctx.slots["op"]
            ctx.parentCtx.slots["qualifierFilter"]["value"] = ctx.slots["value"]
            ctx.parentCtx.slots["qualifierFilter"]["valueType"] = ctx.slots["valueType"]
        else:
            if ctx.slots["valueType"] == "string":
                ctx.parentCtx.slots["qualifierFilter"] = self.func["FilterQualifierStr"].format(ctx.slots["qualifier"], ctx.slots["value"])
            elif ctx.slots["valueType"] == "quantity":
                ctx.parentCtx.slots["qualifierFilter"] = self.func["FilterQualifierNum"].format(ctx.slots["qualifier"], ctx.slots["value"], ctx.slots["op"])
            elif ctx.slots["valueType"] == "year":
                ctx.parentCtx.slots["qualifierFilter"] = self.func["FilterQualifierYear"].format(ctx.slots["qualifier"], ctx.slots["value"], ctx.slots["op"])
            elif ctx.slots["valueType"] == "date":
                ctx.parentCtx.slots["qualifierFilter"] = self.func["FilterQualifierDate"].format(ctx.slots["qualifier"], ctx.slots["value"], ctx.slots["op"])
            else:
                raise Exception("Unexpected value type")
        return super().exitFilterByQualifier(ctx)
    
    def enterEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "concept": ""})
        return super().enterEntitySetByConcept(ctx)
    
    def exitEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        if ctx.slots["entitySet"] == "":
            insert(ctx.parentCtx, self.func["Population"] + self.SEP + self.func["FilterConcept"].format(ctx.slots["concept"]))
        else:
            insert(ctx.parentCtx, ctx.slots["entitySet"] + self.SEP + self.func["FilterConcept"].format(ctx.slots["concept"]))
        return super().exitEntitySetByConcept(ctx)
    
    def enterEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "rankFilter": ""})
        return super().enterEntitySetByRank(ctx)
    
    def exitEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        assert ctx.slots["rankFilter"] != ""
        insert(ctx.parentCtx, ctx.slots["entitySet"] + self.SEP + ctx.slots["rankFilter"])
        return super().exitEntitySetByRank(ctx)
    
    def enterFilterByRank(self, ctx: IRParser.FilterByRankContext):
        ctx.slots = strictDict({"attribute": "", "stringOP": "", "number": 1})
        return super().enterFilterByRank(ctx)
    
    def exitFilterByRank(self, ctx: IRParser.FilterByRankContext):
        ctx.parentCtx.slots["rankFilter"] = self.func["FilterRank"].format(ctx.slots["attribute"], ctx.slots["stringOP"], ctx.slots["number"], 0)
        return super().exitFilterByRank(ctx)
    
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
    
    def exitYear(self, ctx: IRParser.YearContext):
        ctx.parentCtx.slots["valueType"] = "year"
        return super().exitYear(ctx)
    
    def exitLargest(self, ctx: IRParser.LargestContext):
        ctx.parentCtx.slots["stringOP"] = self.stringOP_vocab["largest"]
        return super().enterLargest(ctx)
    
    def exitSmallest(self, ctx: IRParser.SmallestContext):
        ctx.parentCtx.slots["stringOP"] = self.stringOP_vocab["smallest"]
        return super().exitSmallest(ctx)

    # def enterTopK(self, ctx: IRParser.TopKContext):
    #     ctx.slots = strictDict({"number": 1})
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
