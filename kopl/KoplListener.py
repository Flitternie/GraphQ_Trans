# Generated from Kopl.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .KoplParser import KoplParser
else:
    from KoplParser import KoplParser

# This class defines a complete listener for a parse tree produced by KoplParser.
class KoplListener(ParseTreeListener):

    # Enter a parse tree produced by KoplParser#root.
    def enterRoot(self, ctx:KoplParser.RootContext):
        pass

    # Exit a parse tree produced by KoplParser#root.
    def exitRoot(self, ctx:KoplParser.RootContext):
        pass


    # Enter a parse tree produced by KoplParser#whatEntityQuery.
    def enterWhatEntityQuery(self, ctx:KoplParser.WhatEntityQueryContext):
        pass

    # Exit a parse tree produced by KoplParser#whatEntityQuery.
    def exitWhatEntityQuery(self, ctx:KoplParser.WhatEntityQueryContext):
        pass


    # Enter a parse tree produced by KoplParser#howManyEntityQuery.
    def enterHowManyEntityQuery(self, ctx:KoplParser.HowManyEntityQueryContext):
        pass

    # Exit a parse tree produced by KoplParser#howManyEntityQuery.
    def exitHowManyEntityQuery(self, ctx:KoplParser.HowManyEntityQueryContext):
        pass


    # Enter a parse tree produced by KoplParser#whatAttributeQuery.
    def enterWhatAttributeQuery(self, ctx:KoplParser.WhatAttributeQueryContext):
        pass

    # Exit a parse tree produced by KoplParser#whatAttributeQuery.
    def exitWhatAttributeQuery(self, ctx:KoplParser.WhatAttributeQueryContext):
        pass


    # Enter a parse tree produced by KoplParser#whatRelationQuery.
    def enterWhatRelationQuery(self, ctx:KoplParser.WhatRelationQueryContext):
        pass

    # Exit a parse tree produced by KoplParser#whatRelationQuery.
    def exitWhatRelationQuery(self, ctx:KoplParser.WhatRelationQueryContext):
        pass


    # Enter a parse tree produced by KoplParser#attributeSatisfyQuery.
    def enterAttributeSatisfyQuery(self, ctx:KoplParser.AttributeSatisfyQueryContext):
        pass

    # Exit a parse tree produced by KoplParser#attributeSatisfyQuery.
    def exitAttributeSatisfyQuery(self, ctx:KoplParser.AttributeSatisfyQueryContext):
        pass


    # Enter a parse tree produced by KoplParser#whatAttributeQualifierQuery.
    def enterWhatAttributeQualifierQuery(self, ctx:KoplParser.WhatAttributeQualifierQueryContext):
        pass

    # Exit a parse tree produced by KoplParser#whatAttributeQualifierQuery.
    def exitWhatAttributeQualifierQuery(self, ctx:KoplParser.WhatAttributeQualifierQueryContext):
        pass


    # Enter a parse tree produced by KoplParser#whatRelationQualifierQuery.
    def enterWhatRelationQualifierQuery(self, ctx:KoplParser.WhatRelationQualifierQueryContext):
        pass

    # Exit a parse tree produced by KoplParser#whatRelationQualifierQuery.
    def exitWhatRelationQualifierQuery(self, ctx:KoplParser.WhatRelationQualifierQueryContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetGroup.
    def enterEntitySetGroup(self, ctx:KoplParser.EntitySetGroupContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetGroup.
    def exitEntitySetGroup(self, ctx:KoplParser.EntitySetGroupContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetByAttribute.
    def enterEntitySetByAttribute(self, ctx:KoplParser.EntitySetByAttributeContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetByAttribute.
    def exitEntitySetByAttribute(self, ctx:KoplParser.EntitySetByAttributeContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetPopulation.
    def enterEntitySetPopulation(self, ctx:KoplParser.EntitySetPopulationContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetPopulation.
    def exitEntitySetPopulation(self, ctx:KoplParser.EntitySetPopulationContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetByConcept.
    def enterEntitySetByConcept(self, ctx:KoplParser.EntitySetByConceptContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetByConcept.
    def exitEntitySetByConcept(self, ctx:KoplParser.EntitySetByConceptContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetAtom.
    def enterEntitySetAtom(self, ctx:KoplParser.EntitySetAtomContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetAtom.
    def exitEntitySetAtom(self, ctx:KoplParser.EntitySetAtomContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetByRank.
    def enterEntitySetByRank(self, ctx:KoplParser.EntitySetByRankContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetByRank.
    def exitEntitySetByRank(self, ctx:KoplParser.EntitySetByRankContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetByOP.
    def enterEntitySetByOP(self, ctx:KoplParser.EntitySetByOPContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetByOP.
    def exitEntitySetByOP(self, ctx:KoplParser.EntitySetByOPContext):
        pass


    # Enter a parse tree produced by KoplParser#entitySetByRelation.
    def enterEntitySetByRelation(self, ctx:KoplParser.EntitySetByRelationContext):
        pass

    # Exit a parse tree produced by KoplParser#entitySetByRelation.
    def exitEntitySetByRelation(self, ctx:KoplParser.EntitySetByRelationContext):
        pass


    # Enter a parse tree produced by KoplParser#entityFilterByRelation.
    def enterEntityFilterByRelation(self, ctx:KoplParser.EntityFilterByRelationContext):
        pass

    # Exit a parse tree produced by KoplParser#entityFilterByRelation.
    def exitEntityFilterByRelation(self, ctx:KoplParser.EntityFilterByRelationContext):
        pass


    # Enter a parse tree produced by KoplParser#entityFilterByAttribute.
    def enterEntityFilterByAttribute(self, ctx:KoplParser.EntityFilterByAttributeContext):
        pass

    # Exit a parse tree produced by KoplParser#entityFilterByAttribute.
    def exitEntityFilterByAttribute(self, ctx:KoplParser.EntityFilterByAttributeContext):
        pass


    # Enter a parse tree produced by KoplParser#entityFilterByConcept.
    def enterEntityFilterByConcept(self, ctx:KoplParser.EntityFilterByConceptContext):
        pass

    # Exit a parse tree produced by KoplParser#entityFilterByConcept.
    def exitEntityFilterByConcept(self, ctx:KoplParser.EntityFilterByConceptContext):
        pass


    # Enter a parse tree produced by KoplParser#queryName.
    def enterQueryName(self, ctx:KoplParser.QueryNameContext):
        pass

    # Exit a parse tree produced by KoplParser#queryName.
    def exitQueryName(self, ctx:KoplParser.QueryNameContext):
        pass


    # Enter a parse tree produced by KoplParser#count.
    def enterCount(self, ctx:KoplParser.CountContext):
        pass

    # Exit a parse tree produced by KoplParser#count.
    def exitCount(self, ctx:KoplParser.CountContext):
        pass


    # Enter a parse tree produced by KoplParser#findAll.
    def enterFindAll(self, ctx:KoplParser.FindAllContext):
        pass

    # Exit a parse tree produced by KoplParser#findAll.
    def exitFindAll(self, ctx:KoplParser.FindAllContext):
        pass


    # Enter a parse tree produced by KoplParser#setOP.
    def enterSetOP(self, ctx:KoplParser.SetOPContext):
        pass

    # Exit a parse tree produced by KoplParser#setOP.
    def exitSetOP(self, ctx:KoplParser.SetOPContext):
        pass


    # Enter a parse tree produced by KoplParser#and.
    def enterAnd(self, ctx:KoplParser.AndContext):
        pass

    # Exit a parse tree produced by KoplParser#and.
    def exitAnd(self, ctx:KoplParser.AndContext):
        pass


    # Enter a parse tree produced by KoplParser#or.
    def enterOr(self, ctx:KoplParser.OrContext):
        pass

    # Exit a parse tree produced by KoplParser#or.
    def exitOr(self, ctx:KoplParser.OrContext):
        pass


    # Enter a parse tree produced by KoplParser#filterAttr.
    def enterFilterAttr(self, ctx:KoplParser.FilterAttrContext):
        pass

    # Exit a parse tree produced by KoplParser#filterAttr.
    def exitFilterAttr(self, ctx:KoplParser.FilterAttrContext):
        pass


    # Enter a parse tree produced by KoplParser#filterStr.
    def enterFilterStr(self, ctx:KoplParser.FilterStrContext):
        pass

    # Exit a parse tree produced by KoplParser#filterStr.
    def exitFilterStr(self, ctx:KoplParser.FilterStrContext):
        pass


    # Enter a parse tree produced by KoplParser#filterNum.
    def enterFilterNum(self, ctx:KoplParser.FilterNumContext):
        pass

    # Exit a parse tree produced by KoplParser#filterNum.
    def exitFilterNum(self, ctx:KoplParser.FilterNumContext):
        pass


    # Enter a parse tree produced by KoplParser#filterYear.
    def enterFilterYear(self, ctx:KoplParser.FilterYearContext):
        pass

    # Exit a parse tree produced by KoplParser#filterYear.
    def exitFilterYear(self, ctx:KoplParser.FilterYearContext):
        pass


    # Enter a parse tree produced by KoplParser#filterDate.
    def enterFilterDate(self, ctx:KoplParser.FilterDateContext):
        pass

    # Exit a parse tree produced by KoplParser#filterDate.
    def exitFilterDate(self, ctx:KoplParser.FilterDateContext):
        pass


    # Enter a parse tree produced by KoplParser#queryRelation.
    def enterQueryRelation(self, ctx:KoplParser.QueryRelationContext):
        pass

    # Exit a parse tree produced by KoplParser#queryRelation.
    def exitQueryRelation(self, ctx:KoplParser.QueryRelationContext):
        pass


    # Enter a parse tree produced by KoplParser#select.
    def enterSelect(self, ctx:KoplParser.SelectContext):
        pass

    # Exit a parse tree produced by KoplParser#select.
    def exitSelect(self, ctx:KoplParser.SelectContext):
        pass


    # Enter a parse tree produced by KoplParser#queryAttributeUnderCondition.
    def enterQueryAttributeUnderCondition(self, ctx:KoplParser.QueryAttributeUnderConditionContext):
        pass

    # Exit a parse tree produced by KoplParser#queryAttributeUnderCondition.
    def exitQueryAttributeUnderCondition(self, ctx:KoplParser.QueryAttributeUnderConditionContext):
        pass


    # Enter a parse tree produced by KoplParser#queryAttribute.
    def enterQueryAttribute(self, ctx:KoplParser.QueryAttributeContext):
        pass

    # Exit a parse tree produced by KoplParser#queryAttribute.
    def exitQueryAttribute(self, ctx:KoplParser.QueryAttributeContext):
        pass


    # Enter a parse tree produced by KoplParser#verify.
    def enterVerify(self, ctx:KoplParser.VerifyContext):
        pass

    # Exit a parse tree produced by KoplParser#verify.
    def exitVerify(self, ctx:KoplParser.VerifyContext):
        pass


    # Enter a parse tree produced by KoplParser#verifyStr.
    def enterVerifyStr(self, ctx:KoplParser.VerifyStrContext):
        pass

    # Exit a parse tree produced by KoplParser#verifyStr.
    def exitVerifyStr(self, ctx:KoplParser.VerifyStrContext):
        pass


    # Enter a parse tree produced by KoplParser#verifyNum.
    def enterVerifyNum(self, ctx:KoplParser.VerifyNumContext):
        pass

    # Exit a parse tree produced by KoplParser#verifyNum.
    def exitVerifyNum(self, ctx:KoplParser.VerifyNumContext):
        pass


    # Enter a parse tree produced by KoplParser#verifyYear.
    def enterVerifyYear(self, ctx:KoplParser.VerifyYearContext):
        pass

    # Exit a parse tree produced by KoplParser#verifyYear.
    def exitVerifyYear(self, ctx:KoplParser.VerifyYearContext):
        pass


    # Enter a parse tree produced by KoplParser#verifyDate.
    def enterVerifyDate(self, ctx:KoplParser.VerifyDateContext):
        pass

    # Exit a parse tree produced by KoplParser#verifyDate.
    def exitVerifyDate(self, ctx:KoplParser.VerifyDateContext):
        pass


    # Enter a parse tree produced by KoplParser#queryAttrQualifier.
    def enterQueryAttrQualifier(self, ctx:KoplParser.QueryAttrQualifierContext):
        pass

    # Exit a parse tree produced by KoplParser#queryAttrQualifier.
    def exitQueryAttrQualifier(self, ctx:KoplParser.QueryAttrQualifierContext):
        pass


    # Enter a parse tree produced by KoplParser#queryRelationQualifier.
    def enterQueryRelationQualifier(self, ctx:KoplParser.QueryRelationQualifierContext):
        pass

    # Exit a parse tree produced by KoplParser#queryRelationQualifier.
    def exitQueryRelationQualifier(self, ctx:KoplParser.QueryRelationQualifierContext):
        pass


    # Enter a parse tree produced by KoplParser#relate.
    def enterRelate(self, ctx:KoplParser.RelateContext):
        pass

    # Exit a parse tree produced by KoplParser#relate.
    def exitRelate(self, ctx:KoplParser.RelateContext):
        pass


    # Enter a parse tree produced by KoplParser#filterQualifier.
    def enterFilterQualifier(self, ctx:KoplParser.FilterQualifierContext):
        pass

    # Exit a parse tree produced by KoplParser#filterQualifier.
    def exitFilterQualifier(self, ctx:KoplParser.FilterQualifierContext):
        pass


    # Enter a parse tree produced by KoplParser#filterStrQualifier.
    def enterFilterStrQualifier(self, ctx:KoplParser.FilterStrQualifierContext):
        pass

    # Exit a parse tree produced by KoplParser#filterStrQualifier.
    def exitFilterStrQualifier(self, ctx:KoplParser.FilterStrQualifierContext):
        pass


    # Enter a parse tree produced by KoplParser#filterNumQualifier.
    def enterFilterNumQualifier(self, ctx:KoplParser.FilterNumQualifierContext):
        pass

    # Exit a parse tree produced by KoplParser#filterNumQualifier.
    def exitFilterNumQualifier(self, ctx:KoplParser.FilterNumQualifierContext):
        pass


    # Enter a parse tree produced by KoplParser#filterYearQualifier.
    def enterFilterYearQualifier(self, ctx:KoplParser.FilterYearQualifierContext):
        pass

    # Exit a parse tree produced by KoplParser#filterYearQualifier.
    def exitFilterYearQualifier(self, ctx:KoplParser.FilterYearQualifierContext):
        pass


    # Enter a parse tree produced by KoplParser#filterDateQualifier.
    def enterFilterDateQualifier(self, ctx:KoplParser.FilterDateQualifierContext):
        pass

    # Exit a parse tree produced by KoplParser#filterDateQualifier.
    def exitFilterDateQualifier(self, ctx:KoplParser.FilterDateQualifierContext):
        pass


    # Enter a parse tree produced by KoplParser#filterConcept.
    def enterFilterConcept(self, ctx:KoplParser.FilterConceptContext):
        pass

    # Exit a parse tree produced by KoplParser#filterConcept.
    def exitFilterConcept(self, ctx:KoplParser.FilterConceptContext):
        pass


    # Enter a parse tree produced by KoplParser#entity.
    def enterEntity(self, ctx:KoplParser.EntityContext):
        pass

    # Exit a parse tree produced by KoplParser#entity.
    def exitEntity(self, ctx:KoplParser.EntityContext):
        pass


    # Enter a parse tree produced by KoplParser#concept.
    def enterConcept(self, ctx:KoplParser.ConceptContext):
        pass

    # Exit a parse tree produced by KoplParser#concept.
    def exitConcept(self, ctx:KoplParser.ConceptContext):
        pass


    # Enter a parse tree produced by KoplParser#predicate.
    def enterPredicate(self, ctx:KoplParser.PredicateContext):
        pass

    # Exit a parse tree produced by KoplParser#predicate.
    def exitPredicate(self, ctx:KoplParser.PredicateContext):
        pass


    # Enter a parse tree produced by KoplParser#key.
    def enterKey(self, ctx:KoplParser.KeyContext):
        pass

    # Exit a parse tree produced by KoplParser#key.
    def exitKey(self, ctx:KoplParser.KeyContext):
        pass


    # Enter a parse tree produced by KoplParser#value.
    def enterValue(self, ctx:KoplParser.ValueContext):
        pass

    # Exit a parse tree produced by KoplParser#value.
    def exitValue(self, ctx:KoplParser.ValueContext):
        pass


    # Enter a parse tree produced by KoplParser#qkey.
    def enterQkey(self, ctx:KoplParser.QkeyContext):
        pass

    # Exit a parse tree produced by KoplParser#qkey.
    def exitQkey(self, ctx:KoplParser.QkeyContext):
        pass


    # Enter a parse tree produced by KoplParser#qvalue.
    def enterQvalue(self, ctx:KoplParser.QvalueContext):
        pass

    # Exit a parse tree produced by KoplParser#qvalue.
    def exitQvalue(self, ctx:KoplParser.QvalueContext):
        pass


    # Enter a parse tree produced by KoplParser#topk.
    def enterTopk(self, ctx:KoplParser.TopkContext):
        pass

    # Exit a parse tree produced by KoplParser#topk.
    def exitTopk(self, ctx:KoplParser.TopkContext):
        pass


    # Enter a parse tree produced by KoplParser#start.
    def enterStart(self, ctx:KoplParser.StartContext):
        pass

    # Exit a parse tree produced by KoplParser#start.
    def exitStart(self, ctx:KoplParser.StartContext):
        pass


    # Enter a parse tree produced by KoplParser#op.
    def enterOp(self, ctx:KoplParser.OpContext):
        pass

    # Exit a parse tree produced by KoplParser#op.
    def exitOp(self, ctx:KoplParser.OpContext):
        pass


    # Enter a parse tree produced by KoplParser#symbolOP.
    def enterSymbolOP(self, ctx:KoplParser.SymbolOPContext):
        pass

    # Exit a parse tree produced by KoplParser#symbolOP.
    def exitSymbolOP(self, ctx:KoplParser.SymbolOPContext):
        pass


    # Enter a parse tree produced by KoplParser#stringOP.
    def enterStringOP(self, ctx:KoplParser.StringOPContext):
        pass

    # Exit a parse tree produced by KoplParser#stringOP.
    def exitStringOP(self, ctx:KoplParser.StringOPContext):
        pass


    # Enter a parse tree produced by KoplParser#direction.
    def enterDirection(self, ctx:KoplParser.DirectionContext):
        pass

    # Exit a parse tree produced by KoplParser#direction.
    def exitDirection(self, ctx:KoplParser.DirectionContext):
        pass


    # Enter a parse tree produced by KoplParser#string.
    def enterString(self, ctx:KoplParser.StringContext):
        pass

    # Exit a parse tree produced by KoplParser#string.
    def exitString(self, ctx:KoplParser.StringContext):
        pass


    # Enter a parse tree produced by KoplParser#date.
    def enterDate(self, ctx:KoplParser.DateContext):
        pass

    # Exit a parse tree produced by KoplParser#date.
    def exitDate(self, ctx:KoplParser.DateContext):
        pass


    # Enter a parse tree produced by KoplParser#year.
    def enterYear(self, ctx:KoplParser.YearContext):
        pass

    # Exit a parse tree produced by KoplParser#year.
    def exitYear(self, ctx:KoplParser.YearContext):
        pass


    # Enter a parse tree produced by KoplParser#number.
    def enterNumber(self, ctx:KoplParser.NumberContext):
        pass

    # Exit a parse tree produced by KoplParser#number.
    def exitNumber(self, ctx:KoplParser.NumberContext):
        pass



del KoplParser