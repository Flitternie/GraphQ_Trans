from antlr4 import *

from graphq_trans.kopl.KoplLexer import KoplLexer
from graphq_trans.kopl.KoplParser import KoplParser
from graphq_trans.kopl.KoplListener import KoplListener

from graphq_trans.utils import *
from graphq_trans.ir.utils import *


class IREmitter(KoplListener):
    def __init__(self):
        self.output = ""
        
        self.setOP_vocab = {    
            "and": "and",
            "or": "or" 
        }

        self.stringOP_vocab = { 
            "largest": "largest", 
            "smallest": "smallest", 
            "greater": "larger", 
            "less": "smaller"
        }
        
        self.skeleton = {
            "WhatEntityQuery": "what is {}",
            "HowManyEntityQuery": "how many {}",
            "WhatAttributeQuery": "what is the attribute {} of {}",
            "WhatRelationQuery": "what is the relation from {} to {}",
            "AttributeSatisfyQuery": "whether {} {} {}{}",
            "WhatAttributeQualifierQuery": "what is the qualifier {} of {} whose {} is {}",
            "WhatRelationQualifierQuery": "what is the qualifier {} of {} that {} to {}",
        }
        
    def emit(self, ctx):
        return self.output
    
    def find_aux_entityset(self, ctx):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        if ctx.slots["entitySet"][0].startswith("ones"):
            ctx.slots["entitySet"] = [ctx.slots["entitySet"][1], ctx.slots["entitySet"][0]]
            return True
        elif ctx.slots["entitySet"][1].startswith("ones"):
            return True
        else:
            return False

    def enterRoot(self, ctx: KoplParser.RootContext):
        self.output = ""
        ctx.slots = strictDict({"query": ""})
        return super().enterRoot(ctx)

    def exitRoot(self, ctx: KoplParser.RootContext):
        self.output = str(ctx.slots["query"])
        return super().exitRoot(ctx)    

    def enterWhatEntityQuery(self, ctx: KoplParser.WhatEntityQueryContext):
        ctx.slots = strictDict({"entitySet": ""})
        return super().enterWhatEntityQuery(ctx)
    
    def exitWhatEntityQuery(self, ctx: KoplParser.WhatEntityQueryContext):
        if str(ctx.slots["entitySet"]).startswith("which"):
            ctx.parentCtx.slots["query"] = ctx.slots["entitySet"]
        else:
            ctx.parentCtx.slots["query"] = self.skeleton["WhatEntityQuery"].format(scoping("entity", ctx.slots["entitySet"]))
        return super().exitWhatEntityQuery(ctx)
    
    def enterHowManyEntityQuery(self, ctx: KoplParser.HowManyEntityQueryContext):
        ctx.slots = strictDict({"entitySet": ""})
        return super().enterHowManyEntityQuery(ctx)
    
    def exitHowManyEntityQuery(self, ctx: KoplParser.HowManyEntityQueryContext):
        ctx.parentCtx.slots["query"] = self.skeleton["HowManyEntityQuery"].format(scoping("entity", ctx.slots["entitySet"]))
        return super().exitHowManyEntityQuery(ctx)

    def enterWhatAttributeQuery(self, ctx: KoplParser.WhatAttributeQueryContext):
        ctx.slots = strictDict({"entitySet": "", "attribute": ""})
        return super().enterWhatAttributeQuery(ctx)

    def exitWhatAttributeQuery(self, ctx: KoplParser.WhatAttributeQueryContext):
        ctx.parentCtx.slots["query"] = self.skeleton["WhatAttributeQuery"].format(scoping("attribute", ctx.slots["attribute"]), scoping("entity", ctx.slots["entitySet"]))
        return super().exitWhatAttributeQuery(ctx)
    
    def enterWhatRelationQuery(self, ctx: KoplParser.WhatRelationQueryContext):
        ctx.slots = strictDict({"entitySetGroup": []})
        return super().enterWhatRelationQuery(ctx)
    
    def exitWhatRelationQuery(self, ctx: KoplParser.WhatRelationQueryContext):
        ctx.parentCtx.slots["query"] = self.skeleton["WhatRelationQuery"].format(scoping("entity", ctx.slots["entitySetGroup"][0]), scoping("entity", ctx.slots["entitySetGroup"][1]))
        return super().exitWhatRelationQuery(ctx)

    def enterAttributeSatisfyQuery(self, ctx: KoplParser.AttributeSatisfyQueryContext):
        ctx.slots = strictDict({"entitySet": "", "attribute": "", "verify": "", "qualifier": ""})
        return super().enterAttributeSatisfyQuery(ctx)
    
    def exitAttributeSatisfyQuery(self, ctx: KoplParser.AttributeSatisfyQueryContext):
        ctx.parentCtx.slots["query"] = self.skeleton["AttributeSatisfyQuery"].format(scoping("entity", ctx.slots["entitySet"]), scoping("attribute", ctx.slots["attribute"]), ctx.slots["verify"], ctx.slots["qualifier"])
        return super().exitAttributeSatisfyQuery(ctx)

    def enterWhatAttributeQualifierQuery(self, ctx: KoplParser.WhatAttributeQualifierQueryContext):
        ctx.slots = strictDict({"entitySet": "", "attribute": "", "value": "", "qualifier": ""})
        return super().enterWhatAttributeQualifierQuery(ctx)

    def exitWhatAttributeQualifierQuery(self, ctx: KoplParser.WhatAttributeQualifierQueryContext):
        ctx.parentCtx.slots["query"] = self.skeleton["WhatAttributeQualifierQuery"].format(scoping("qualifier", ctx.slots["qualifier"]), scoping("entity", ctx.slots["entitySet"]), scoping("attribute", ctx.slots["attribute"]), scoping("value", ctx.slots["value"]))
        return super().exitWhatAttributeQualifierQuery(ctx)
    
    def enterQueryAttrQualifier(self, ctx: KoplParser.QueryAttrQualifierContext):
        ctx.slots = strictDict({"key": "", "value": "", "qkey": ""})
        return super().enterQueryAttrQualifier(ctx)
    
    def exitQueryAttrQualifier(self, ctx: KoplParser.QueryAttrQualifierContext):
        ctx.parentCtx.slots["attribute"] = ctx.slots["key"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"]
        ctx.parentCtx.slots["qualifier"] = ctx.slots["qkey"]
        return super().exitQueryAttrQualifier(ctx)


    def enterWhatRelationQualifierQuery(self, ctx: KoplParser.WhatRelationQualifierQueryContext):
        ctx.slots = strictDict({"entitySetGroup": [], "predicate": "", "qualifier": ""})
        return super().enterWhatRelationQualifierQuery(ctx)
    
    def exitWhatRelationQualifierQuery(self, ctx: KoplParser.WhatRelationQualifierQueryContext):
        ctx.parentCtx.slots["query"] = self.skeleton["WhatRelationQualifierQuery"].format(scoping("qualifier", ctx.slots["qualifier"]), scoping("entity", ctx.slots["entitySetGroup"][0]), scoping("relation", ctx.slots["predicate"]), scoping("entity", ctx.slots["entitySetGroup"][1]))
        return super().exitWhatRelationQualifierQuery(ctx) 

    def enterQueryRelationQualifier(self, ctx: KoplParser.QueryRelationQualifierContext):
        ctx.slots = strictDict({"predicate": "", "qkey": ""})
        return super().enterQueryRelationQualifier(ctx)
    
    def exitQueryRelationQualifier(self, ctx: KoplParser.QueryRelationQualifierContext):
        ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"]
        ctx.parentCtx.slots["qualifier"] = ctx.slots["qkey"]
        return super().exitQueryRelationQualifier(ctx)
 

    def enterEntitySetGroup(self, ctx: KoplParser.EntitySetGroupContext):
        ctx.slots = strictDict({"entitySet": []})
        return super().enterEntitySetGroup(ctx)
    
    def exitEntitySetGroup(self, ctx: KoplParser.EntitySetGroupContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        ctx.parentCtx.slots["entitySetGroup"] = ctx.slots["entitySet"]
        return super().exitEntitySetGroup(ctx)

    def enterEntitySetByOP(self, ctx: KoplParser.EntitySetByOPContext):
        ctx.slots = strictDict({"entitySet": [], "setOP": ""})
        return super().enterEntitySetByOP(ctx)
    
    def exitEntitySetByOP(self, ctx: KoplParser.EntitySetByOPContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        if ctx.slots["setOP"] == self.setOP_vocab["and"] and self.find_aux_entityset(ctx):
            insert(ctx.parentCtx, "{} ({})".format(scoping("entity", ctx.slots["entitySet"][0]), scoping("entity", ctx.slots["entitySet"][1])))
        else:
            insert(ctx.parentCtx, "{} {} {}".format(scoping("entity", ctx.slots["entitySet"][0]), ctx.slots["setOP"], scoping("entity", ctx.slots["entitySet"][1])))
        return super().exitEntitySetByOP(ctx)

    def enterEntitySetByRank(self, ctx: KoplParser.EntitySetByRankContext):
        ctx.slots = strictDict({"entitySet": "", "attributeRankFilter": ""})
        return super().enterEntitySetByRank(ctx)
    
    def exitEntitySetByRank(self, ctx: KoplParser.EntitySetByRankContext):
        insert(ctx.parentCtx, "{} among {}".format(ctx.slots["attributeRankFilter"], scoping("entity", ctx.slots["entitySet"])))
        return super().exitEntitySetByRank(ctx)
    
    # def enterEntitySetNested(self, ctx: KoplParser.EntitySetNestedContext):
    #     ctx.slots = strictDict({"entitySet": "", "relationFilter": "", "attributeFilter": "", "conceptFilter": "", "qualifierFilter": ""})
    #     return super().enterEntitySetNested(ctx)
    
    # def exitEntitySetNested(self, ctx: KoplParser.EntitySetNestedContext):
    #     if ctx.slots["relationFilter"]:
    #         if ctx.slots["conceptFilter"]:
    #             insert(ctx.parentCtx, "the {}{} {}{}".format(ctx.slots["conceptFilter"], ctx.slots["relationFilter"], scoping("entity", ctx.slots["entitySet"]), ctx.slots["qualifierFilter"]))
    #         else:
    #             insert(ctx.parentCtx, "the one {} {}{}".format(ctx.slots["relationFilter"], scoping("entity", ctx.slots["entitySet"]), ctx.slots["qualifierFilter"]))
    #     elif ctx.slots["attributeFilter"]:
    #         insert(ctx.parentCtx, "{}{} {}{}".format(ctx.slots["conceptFilter"], scoping("entity", ctx.slots["entitySet"]), ctx.slots["attributeFilter"], ctx.slots["qualifierFilter"]))
    #     return super().exitEntitySetNested(ctx)
    
    # def enterEntitySetByFilter(self, ctx: KoplParser.EntitySetByFilterContext):
    #     ctx.slots = strictDict({"attributeFilter": "", "conceptFilter": "", "qualifierFilter": ""})
    #     return super().enterEntitySetByFilter(ctx)
    
    # def exitEntitySetByFilter(self, ctx: KoplParser.EntitySetByFilterContext):
    #     insert(ctx.parentCtx, "{}{}{}".format(ctx.slots["conceptFilter"], ctx.slots["attributeFilter"], ctx.slots["qualifierFilter"]))
    #     return super().exitEntitySetByFilter(ctx)
    
    def enterEntitySetByRelation(self, ctx: KoplParser.EntitySetByRelationContext):
        ctx.slots = strictDict({"entitySet": "", "relationFilter": "", "conceptFilter": "", "qualifierFilter": ""})
        return super().enterEntitySetByRelation(ctx)
    
    def exitEntitySetByRelation(self, ctx: KoplParser.EntitySetByRelationContext):
        if ctx.slots["conceptFilter"]:
            insert(ctx.parentCtx, "{}{} {}{}".format(ctx.slots["conceptFilter"], ctx.slots["relationFilter"], scoping("entity", ctx.slots["entitySet"]), ctx.slots["qualifierFilter"]))
        else:
            insert(ctx.parentCtx, "ones {} {}{}".format(ctx.slots["relationFilter"], scoping("entity", ctx.slots["entitySet"]), ctx.slots["qualifierFilter"]))
        return super().exitEntitySetByRelation(ctx)
    
    def enterEntitySetByAttribute(self, ctx: KoplParser.EntitySetByAttributeContext):
        ctx.slots = strictDict({"entitySet": "", "attributeFilter": "", "conceptFilter": "", "qualifierFilter": ""})
        return super().enterEntitySetByAttribute(ctx)

    def exitEntitySetByAttribute(self, ctx: KoplParser.EntitySetByAttributeContext):
        if ctx.slots["conceptFilter"]:
            if ctx.slots["entitySet"].is_pop:
                insert(ctx.parentCtx, "{}{}{}".format(ctx.slots["conceptFilter"], ctx.slots["attributeFilter"], ctx.slots["qualifierFilter"]))
            else:
                insert(ctx.parentCtx, "{}{} {}{}".format(ctx.slots["conceptFilter"], scoping("entity", ctx.slots["entitySet"]), ctx.slots["attributeFilter"], ctx.slots["qualifierFilter"]))
        else:
            insert(ctx.parentCtx, "{} {}{}".format(scoping("entity", ctx.slots["entitySet"]), ctx.slots["attributeFilter"], ctx.slots["qualifierFilter"]))
        return super().exitEntitySetByAttribute(ctx)
    
    def enterEntitySetByConcept(self, ctx: KoplParser.EntitySetByConceptContext):
        ctx.slots = strictDict({"entitySet": "", "conceptFilter": ""})
        return super().enterEntitySetByConcept(ctx)

    def exitEntitySetByConcept(self, ctx: KoplParser.EntitySetByConceptContext):
        insert(ctx.parentCtx, "{}{}".format(ctx.slots["conceptFilter"], scoping("entity", ctx.slots["entitySet"])))
        return super().exitEntitySetByConcept(ctx)
    
    def exitEntitySetPopulation(self, ctx: KoplParser.EntitySetPopulationContext):
        if isinstance(ctx.parentCtx, KoplParser.EntitySetByRelationContext):
            return super().exitEntitySetPopulation(ctx)
        if isinstance(ctx.parentCtx, KoplParser.EntitySetByConceptContext):
            insert(ctx.parentCtx, "", is_pop=True)
        else:
            insert(ctx.parentCtx, "ones", is_pop=True)
        return super().exitEntitySetPopulation(ctx)
    
    def enterEntitySetAtom(self, ctx: KoplParser.EntitySetAtomContext):
        ctx.slots = strictDict({"entity": ""})
        return super().enterEntitySetAtom(ctx)
    
    def exitEntitySetAtom(self, ctx: KoplParser.EntitySetAtomContext):
        insert(ctx.parentCtx, ctx.slots["entity"], is_atom=True)
        return super().exitEntitySetAtom(ctx)



    def enterEntityFilterByRelation(self, ctx: KoplParser.EntityFilterByRelationContext):
        ctx.slots = strictDict({"predicate": "", "direction": "", "qualifier": "", "concept": ""})
        return super().enterEntityFilterByRelation(ctx)
    
    def exitEntityFilterByRelation(self, ctx: KoplParser.EntityFilterByRelationContext):
        ctx.parentCtx.slots["relationFilter"] = "that {} {} to".format(scoping("relation", ctx.slots["predicate"]), ctx.slots["direction"])
        if ctx.slots["qualifier"]:
            ctx.parentCtx.slots["qualifierFilter"] = ctx.slots["qualifier"]
        if ctx.slots["concept"]:
            ctx.parentCtx.slots["conceptFilter"] = "{} ".format(scoping("concept", ctx.slots["concept"]))
        return super().exitEntityFilterByRelation(ctx)
    
    def enterEntityFilterByAttribute(self, ctx: KoplParser.EntityFilterByAttributeContext):
        ctx.slots = strictDict({"attribute": "", "qualifier": "", "concept": ""})
        return super().enterEntityFilterByAttribute(ctx)
    
    def exitEntityFilterByAttribute(self, ctx: KoplParser.EntityFilterByAttributeContext):
        ctx.parentCtx.slots["attributeFilter"] = "whose {}".format(ctx.slots["attribute"])
        if ctx.slots["qualifier"]:
            ctx.parentCtx.slots["qualifierFilter"] = ctx.slots["qualifier"]
        if ctx.slots["concept"]:
            ctx.parentCtx.slots["conceptFilter"] = "{} ".format(scoping("concept", ctx.slots["concept"]))
        return super().exitEntityFilterByAttribute(ctx)   

    def enterEntityFilterByConcept(self, ctx: KoplParser.EntityFilterByConceptContext):
        ctx.slots = strictDict({"concept": ""})
        return super().enterEntityFilterByConcept(ctx)
    
    def exitEntityFilterByConcept(self, ctx: KoplParser.EntityFilterByConceptContext):
        ctx.parentCtx.slots["conceptFilter"] = "{} ".format(scoping("concept", ctx.slots["concept"]))
        return super().exitEntityFilterByConcept(ctx)



    def enterFilterConcept(self, ctx: KoplParser.FilterConceptContext):
        ctx.slots = strictDict({"concept": ""})
        return super().enterFilterConcept(ctx)

    def exitFilterConcept(self, ctx: KoplParser.FilterConceptContext):
        ctx.parentCtx.slots["concept"] = ctx.slots["concept"]
        return super().exitFilterConcept(ctx)
    
    def enterRelate(self, ctx: KoplParser.RelateContext):
        ctx.slots = strictDict({"predicate": "", "direction": ""})
        return super().enterRelate(ctx)
    
    def exitRelate(self, ctx: KoplParser.RelateContext):
        ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"]
        ctx.parentCtx.slots["direction"] = ctx.slots["direction"]
        return super().exitRelate(ctx)

    def enterFilterAttr(self, ctx: KoplParser.FilterAttrContext):
        ctx.slots = strictDict({"attribute": "", "value": "", "valueType": "", "OP": ""})
        return super().enterFilterAttr(ctx)
    
    def exitFilterAttr(self, ctx: KoplParser.FilterAttrContext):
        ctx.parentCtx.slots["attribute"] = "{} {} {} {}".format(scoping("attribute", ctx.slots["attribute"]), ctx.slots["OP"], ctx.slots["valueType"], scoping("value", ctx.slots["value"]))
        return super().exitFilterAttr(ctx)
    
    def enterFilterQualifier(self, ctx: KoplParser.FilterQualifierContext):
        ctx.slots = strictDict({"attribute": "", "value": "", "valueType": "", "OP": ""})
        return super().enterFilterQualifier(ctx)
    
    def exitFilterQualifier(self, ctx: KoplParser.FilterQualifierContext):
        ctx.parentCtx.slots["qualifier"] = " ( {} {} {} {} )".format(scoping("qualifier", ctx.slots["attribute"]), ctx.slots["OP"], ctx.slots["valueType"], scoping("value", ctx.slots["value"]))
        return super().exitFilterQualifier(ctx)

    def enterSelect(self, ctx: KoplParser.SelectContext):
        ctx.slots = strictDict({"key": "", "OP": "", "topK": "", "start": ""})
        return super().enterSelect(ctx)
    
    def exitSelect(self, ctx: KoplParser.SelectContext):
        try:
            assert ctx.slots["start"] == '0'
        except:
            raise NotImplementedError("customized start position inside Select() function is not supported yet.")
        if ctx.slots["topK"] == '1':
            ctx.parentCtx.slots["attributeRankFilter"] = "which one has the {} {}".format(ctx.slots["OP"], scoping("attribute", ctx.slots["key"]))
        else:
            ctx.parentCtx.slots["attributeRankFilter"] = "which one has the top {} {} {}".format(ctx.slots["topK"], ctx.slots["OP"], scoping("attribute", ctx.slots["key"]))
        return super().exitSelect(ctx)     
    
    def enterQueryAttribute(self, ctx: KoplParser.QueryAttributeContext):
        ctx.slots = strictDict({"key": ""})
        return super().enterQueryAttribute(ctx)

    def exitQueryAttribute(self, ctx: KoplParser.QueryAttributeContext):
        ctx.parentCtx.slots["attribute"] = ctx.slots["key"]
        return super().exitQueryAttribute(ctx)

    def enterQueryAttributeUnderCondition(self, ctx: KoplParser.QueryAttributeUnderConditionContext):
        ctx.slots = strictDict({"key": "", "qkey": "", "qvalue": ""})
        return super().enterQueryAttributeUnderCondition(ctx)
    
    def exitQueryAttributeUnderCondition(self, ctx: KoplParser.QueryAttributeUnderConditionContext):
        ctx.parentCtx.slots["attribute"] = ctx.slots["key"]
        ctx.parentCtx.slots["qualifier"] = " ( {} is {} )".format(scoping("qualifier", ctx.slots["qkey"]), scoping("value", ctx.slots["qvalue"]))
        return super().exitQueryAttributeUnderCondition(ctx)

    def enterVerify(self, ctx: KoplParser.VerifyContext):
        ctx.slots = strictDict({"value": "", "valueType": "", "OP": ""})
        return super().enterVerify(ctx)
    
    def exitVerify(self, ctx: KoplParser.VerifyContext):
        ctx.parentCtx.slots["verify"] = "{} {} {}".format(ctx.slots["OP"], ctx.slots["valueType"], scoping("value", ctx.slots["value"]))
        return super().exitVerify(ctx)

    
    def enterFilterStr(self, ctx: KoplParser.FilterStrContext):
        ctx.slots = strictDict({"key": "", "OP": "", "value": ""})
        return super().enterFilterStr(ctx)

    def exitFilterStr(self, ctx: KoplParser.FilterStrContext):
        ctx.parentCtx.slots["valueType"] = "text"
        ctx.parentCtx.slots["attribute"] = ctx.slots["key"]
        ctx.parentCtx.slots["OP"] = "is"
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().exitFilterStr(ctx)

    def enterFilterNum(self, ctx: KoplParser.FilterNumContext):
        ctx.slots = strictDict({"key": "", "OP": "", "value": ""})
        return super().enterFilterNum(ctx)

    def exitFilterNum(self, ctx: KoplParser.FilterNumContext):
        ctx.parentCtx.slots["valueType"] = "number"
        ctx.parentCtx.slots["attribute"] = ctx.slots["key"]
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().exitFilterNum(ctx)

    def enterFilterYear(self, ctx: KoplParser.FilterYearContext):
        ctx.slots = strictDict({"key": "", "OP": "", "value": ""})
        return super().enterFilterYear(ctx)

    def exitFilterYear(self, ctx: KoplParser.FilterYearContext):
        ctx.parentCtx.slots["valueType"] = "year"
        ctx.parentCtx.slots["attribute"] = ctx.slots["key"]
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().exitFilterYear(ctx)

    def enterFilterDate(self, ctx: KoplParser.FilterDateContext):
        ctx.slots = strictDict({"key": "", "OP": "", "value": ""})
        return super().enterFilterDate(ctx)

    def exitFilterDate(self, ctx: KoplParser.FilterDateContext):
        ctx.parentCtx.slots["valueType"] = "date"
        ctx.parentCtx.slots["attribute"] = ctx.slots["key"]
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().exitFilterDate(ctx)



    def enterFilterStrQualifier(self, ctx: KoplParser.FilterStrQualifierContext):
        ctx.slots = strictDict({"qkey": "", "OP": "", "qvalue": ""})
        return super().enterFilterStrQualifier(ctx)
    
    def exitFilterStrQualifier(self, ctx: KoplParser.FilterStrQualifierContext):
        ctx.parentCtx.slots["valueType"] = "text"
        ctx.parentCtx.slots["attribute"] = ctx.slots["qkey"]
        ctx.parentCtx.slots["OP"] = "is"
        ctx.parentCtx.slots["value"] = ctx.slots["qvalue"] 
        return super().exitFilterStrQualifier(ctx)
    
    def enterFilterNumQualifier(self, ctx: KoplParser.FilterNumQualifierContext):
        ctx.slots = strictDict({"qkey": "", "OP": "", "qvalue": ""})
        return super().enterFilterNumQualifier(ctx)
    
    def exitFilterNumQualifier(self, ctx: KoplParser.FilterNumQualifierContext):
        ctx.parentCtx.slots["valueType"] = "number"
        ctx.parentCtx.slots["attribute"] = ctx.slots["qkey"]
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["qvalue"] 
        return super().exitFilterNumQualifier(ctx)
    
    def enterFilterYearQualifier(self, ctx: KoplParser.FilterYearQualifierContext):
        ctx.slots = strictDict({"qkey": "", "OP": "", "qvalue": ""})
        return super().enterFilterYearQualifier(ctx)

    def exitFilterYearQualifier(self, ctx: KoplParser.FilterYearQualifierContext):
        ctx.parentCtx.slots["valueType"] = "year"
        ctx.parentCtx.slots["attribute"] = ctx.slots["qkey"]
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["qvalue"] 
        return super().exitFilterYearQualifier(ctx)

    def enterFilterDateQualifier(self, ctx: KoplParser.FilterDateQualifierContext):
        ctx.slots = strictDict({"qkey": "", "OP": "", "qvalue": ""})
        return super().enterFilterDateQualifier(ctx)

    def exitFilterDateQualifier(self, ctx: KoplParser.FilterDateQualifierContext):
        ctx.parentCtx.slots["valueType"] = "date"
        ctx.parentCtx.slots["attribute"] = ctx.slots["qkey"]
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["qvalue"] 
        return super().exitFilterDateQualifier(ctx)



    def enterVerifyStr(self, ctx: KoplParser.VerifyStrContext):
        ctx.slots = strictDict({"value": "", "valueType": "", "OP": ""})
        return super().enterVerifyStr(ctx)

    def exitVerifyStr(self, ctx: KoplParser.VerifyStrContext):
        ctx.parentCtx.slots["valueType"] = "text"
        ctx.parentCtx.slots["OP"] = "is"
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().enterVerifyStr(ctx)
    
    def enterVerifyNum(self, ctx: KoplParser.VerifyNumContext):
        ctx.slots = strictDict({"value": "", "valueType": "", "OP": ""})
        return super().enterVerifyNum(ctx)
    
    def exitVerifyNum(self, ctx: KoplParser.VerifyNumContext):
        ctx.parentCtx.slots["valueType"] = "number"
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().exitVerifyNum(ctx)
    
    def enterVerifyYear(self, ctx: KoplParser.VerifyYearContext):
        ctx.slots = strictDict({"value": "", "valueType": "", "OP": ""})
        return super().enterVerifyYear(ctx)

    def exitVerifyYear(self, ctx: KoplParser.VerifyYearContext):
        ctx.parentCtx.slots["valueType"] = "year"
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().exitVerifyYear(ctx)
    
    def enterVerifyDate(self, ctx: KoplParser.VerifyDateContext):
        ctx.slots = strictDict({"value": "", "valueType": "", "OP": ""})
        return super().enterVerifyDate(ctx)

    def exitVerifyDate(self, ctx: KoplParser.VerifyDateContext):
        ctx.parentCtx.slots["valueType"] = "date"
        ctx.parentCtx.slots["OP"] = ctx.slots["OP"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"] 
        return super().exitVerifyDate(ctx)
    

    def enterEntity(self, ctx: KoplParser.EntityContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterEntity(ctx)
    
    def exitEntity(self, ctx: KoplParser.EntityContext):
        ctx.parentCtx.slots["entity"] = ctx.slots["string"]
        return super().exitEntity(ctx)
    
    def enterConcept(self, ctx: KoplParser.ConceptContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterConcept(ctx)
    
    def exitConcept(self, ctx: KoplParser.ConceptContext):
        ctx.parentCtx.slots["concept"] = ctx.slots["string"]
        return super().exitConcept(ctx)
    
    def enterPredicate(self, ctx: KoplParser.PredicateContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterPredicate(ctx)
    
    def exitPredicate(self, ctx: KoplParser.PredicateContext):
        ctx.parentCtx.slots["predicate"] = ctx.slots["string"]
        return super().exitPredicate(ctx)
    
    def enterKey(self, ctx: KoplParser.KeyContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterKey(ctx)
    
    def exitKey(self, ctx: KoplParser.KeyContext):
        ctx.parentCtx.slots["key"] = ctx.slots["string"]
        return super().exitKey(ctx)
    
    def enterValue(self, ctx: KoplParser.ValueContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterValue(ctx)
    
    def exitValue(self, ctx: KoplParser.ValueContext):
        ctx.parentCtx.slots["value"] = ctx.slots["string"]
        return super().exitValue(ctx)
    
    def enterQkey(self, ctx: KoplParser.QkeyContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterQkey(ctx)
    
    def exitQkey(self, ctx: KoplParser.QkeyContext):
        ctx.parentCtx.slots["qkey"] = ctx.slots["string"]
        return super().exitQkey(ctx)
    
    def enterQvalue(self, ctx: KoplParser.QvalueContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterQvalue(ctx)
    
    def exitQvalue(self, ctx: KoplParser.QvalueContext):
        ctx.parentCtx.slots["qvalue"] = ctx.slots["string"]
        return super().exitQvalue(ctx)
    
    def enterTopk(self, ctx: KoplParser.TopkContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterTopk(ctx)
    
    def exitTopk(self, ctx: KoplParser.TopkContext):
        ctx.parentCtx.slots["topK"] = ctx.slots["string"]
        return super().exitTopk(ctx)
    
    def enterStart(self, ctx: KoplParser.StartContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterStart(ctx)

    def exitStart(self, ctx: KoplParser.StartContext):
        ctx.parentCtx.slots["start"] = ctx.slots["string"]
        return super().exitStart(ctx)

    def exitSymbolOP(self, ctx: KoplParser.SymbolOPContext):
        op = ctx.stop.text
        ctx.parentCtx.parentCtx.slots["OP"] = symbolOP_vocab[op]
        return super().exitSymbolOP(ctx)
    
    def exitStringOP(self, ctx: KoplParser.StringOPContext):
        op = ctx.stop.text
        ctx.parentCtx.parentCtx.slots["OP"] = self.stringOP_vocab[op]
        return super().exitStringOP(ctx)
    
    def exitAnd(self, ctx: KoplParser.AndContext):
        ctx.parentCtx.parentCtx.slots["setOP"] = self.setOP_vocab["and"]
        return super().exitAnd(ctx)
    
    def exitOr(self, ctx: KoplParser.OrContext):
        ctx.parentCtx.parentCtx.slots["setOP"] = self.setOP_vocab["or"]
        return super().exitOr(ctx)
    
    def exitDirection(self, ctx: KoplParser.DirectionContext):
        if not isinstance(ctx.parentCtx, KoplParser.StringContext):
            direction = str(ctx.getText())
            if direction == "forward":
                ctx.parentCtx.slots["direction"] = "backward"
            elif direction == "backward":
                ctx.parentCtx.slots["direction"] = "forward"
            else:
                raise ValueError("Direction must be either 'forward' or 'backward'") 
        return super().exitDirection(ctx)

    def enterString(self, ctx: KoplParser.StringContext):
        if not isinstance(ctx.parentCtx, KoplParser.StringContext):
            ctx.parentCtx.slots["string"] = str(ctx.getText())
        


    


    