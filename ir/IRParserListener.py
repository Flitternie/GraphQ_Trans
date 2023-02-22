# Generated from IRParser.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .IRParser import IRParser
else:
    from IRParser import IRParser

# This class defines a complete listener for a parse tree produced by IRParser.
class IRParserListener(ParseTreeListener):

    # Enter a parse tree produced by IRParser#root.
    def enterRoot(self, ctx:IRParser.RootContext):
        pass

    # Exit a parse tree produced by IRParser#root.
    def exitRoot(self, ctx:IRParser.RootContext):
        pass


    # Enter a parse tree produced by IRParser#entityQuery.
    def enterEntityQuery(self, ctx:IRParser.EntityQueryContext):
        pass

    # Exit a parse tree produced by IRParser#entityQuery.
    def exitEntityQuery(self, ctx:IRParser.EntityQueryContext):
        pass


    # Enter a parse tree produced by IRParser#attributeQuery.
    def enterAttributeQuery(self, ctx:IRParser.AttributeQueryContext):
        pass

    # Exit a parse tree produced by IRParser#attributeQuery.
    def exitAttributeQuery(self, ctx:IRParser.AttributeQueryContext):
        pass


    # Enter a parse tree produced by IRParser#predicateQuery.
    def enterPredicateQuery(self, ctx:IRParser.PredicateQueryContext):
        pass

    # Exit a parse tree produced by IRParser#predicateQuery.
    def exitPredicateQuery(self, ctx:IRParser.PredicateQueryContext):
        pass


    # Enter a parse tree produced by IRParser#qualifierQuery.
    def enterQualifierQuery(self, ctx:IRParser.QualifierQueryContext):
        pass

    # Exit a parse tree produced by IRParser#qualifierQuery.
    def exitQualifierQuery(self, ctx:IRParser.QualifierQueryContext):
        pass


    # Enter a parse tree produced by IRParser#countQuery.
    def enterCountQuery(self, ctx:IRParser.CountQueryContext):
        pass

    # Exit a parse tree produced by IRParser#countQuery.
    def exitCountQuery(self, ctx:IRParser.CountQueryContext):
        pass


    # Enter a parse tree produced by IRParser#verifyQuery.
    def enterVerifyQuery(self, ctx:IRParser.VerifyQueryContext):
        pass

    # Exit a parse tree produced by IRParser#verifyQuery.
    def exitVerifyQuery(self, ctx:IRParser.VerifyQueryContext):
        pass


    # Enter a parse tree produced by IRParser#selectQuery.
    def enterSelectQuery(self, ctx:IRParser.SelectQueryContext):
        pass

    # Exit a parse tree produced by IRParser#selectQuery.
    def exitSelectQuery(self, ctx:IRParser.SelectQueryContext):
        pass


    # Enter a parse tree produced by IRParser#valueQuery.
    def enterValueQuery(self, ctx:IRParser.ValueQueryContext):
        pass

    # Exit a parse tree produced by IRParser#valueQuery.
    def exitValueQuery(self, ctx:IRParser.ValueQueryContext):
        pass


    # Enter a parse tree produced by IRParser#verifyByAttribute.
    def enterVerifyByAttribute(self, ctx:IRParser.VerifyByAttributeContext):
        pass

    # Exit a parse tree produced by IRParser#verifyByAttribute.
    def exitVerifyByAttribute(self, ctx:IRParser.VerifyByAttributeContext):
        pass


    # Enter a parse tree produced by IRParser#verifyByPredicate.
    def enterVerifyByPredicate(self, ctx:IRParser.VerifyByPredicateContext):
        pass

    # Exit a parse tree produced by IRParser#verifyByPredicate.
    def exitVerifyByPredicate(self, ctx:IRParser.VerifyByPredicateContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetGroup.
    def enterEntitySetGroup(self, ctx:IRParser.EntitySetGroupContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetGroup.
    def exitEntitySetGroup(self, ctx:IRParser.EntitySetGroupContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetIntersect.
    def enterEntitySetIntersect(self, ctx:IRParser.EntitySetIntersectContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetIntersect.
    def exitEntitySetIntersect(self, ctx:IRParser.EntitySetIntersectContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetFilter.
    def enterEntitySetFilter(self, ctx:IRParser.EntitySetFilterContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetFilter.
    def exitEntitySetFilter(self, ctx:IRParser.EntitySetFilterContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetAtom.
    def enterEntitySetAtom(self, ctx:IRParser.EntitySetAtomContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetAtom.
    def exitEntitySetAtom(self, ctx:IRParser.EntitySetAtomContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetPlaceholder.
    def enterEntitySetPlaceholder(self, ctx:IRParser.EntitySetPlaceholderContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetPlaceholder.
    def exitEntitySetPlaceholder(self, ctx:IRParser.EntitySetPlaceholderContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetByAttribute.
    def enterEntitySetByAttribute(self, ctx:IRParser.EntitySetByAttributeContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetByAttribute.
    def exitEntitySetByAttribute(self, ctx:IRParser.EntitySetByAttributeContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetByPredicate.
    def enterEntitySetByPredicate(self, ctx:IRParser.EntitySetByPredicateContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetByPredicate.
    def exitEntitySetByPredicate(self, ctx:IRParser.EntitySetByPredicateContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetByConcept.
    def enterEntitySetByConcept(self, ctx:IRParser.EntitySetByConceptContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetByConcept.
    def exitEntitySetByConcept(self, ctx:IRParser.EntitySetByConceptContext):
        pass


    # Enter a parse tree produced by IRParser#entitySetByRank.
    def enterEntitySetByRank(self, ctx:IRParser.EntitySetByRankContext):
        pass

    # Exit a parse tree produced by IRParser#entitySetByRank.
    def exitEntitySetByRank(self, ctx:IRParser.EntitySetByRankContext):
        pass


    # Enter a parse tree produced by IRParser#filterByRank.
    def enterFilterByRank(self, ctx:IRParser.FilterByRankContext):
        pass

    # Exit a parse tree produced by IRParser#filterByRank.
    def exitFilterByRank(self, ctx:IRParser.FilterByRankContext):
        pass


    # Enter a parse tree produced by IRParser#filterByAttribute.
    def enterFilterByAttribute(self, ctx:IRParser.FilterByAttributeContext):
        pass

    # Exit a parse tree produced by IRParser#filterByAttribute.
    def exitFilterByAttribute(self, ctx:IRParser.FilterByAttributeContext):
        pass


    # Enter a parse tree produced by IRParser#filterByPredicate.
    def enterFilterByPredicate(self, ctx:IRParser.FilterByPredicateContext):
        pass

    # Exit a parse tree produced by IRParser#filterByPredicate.
    def exitFilterByPredicate(self, ctx:IRParser.FilterByPredicateContext):
        pass


    # Enter a parse tree produced by IRParser#filterByQualifier.
    def enterFilterByQualifier(self, ctx:IRParser.FilterByQualifierContext):
        pass

    # Exit a parse tree produced by IRParser#filterByQualifier.
    def exitFilterByQualifier(self, ctx:IRParser.FilterByQualifierContext):
        pass


    # Enter a parse tree produced by IRParser#forward.
    def enterForward(self, ctx:IRParser.ForwardContext):
        pass

    # Exit a parse tree produced by IRParser#forward.
    def exitForward(self, ctx:IRParser.ForwardContext):
        pass


    # Enter a parse tree produced by IRParser#backward.
    def enterBackward(self, ctx:IRParser.BackwardContext):
        pass

    # Exit a parse tree produced by IRParser#backward.
    def exitBackward(self, ctx:IRParser.BackwardContext):
        pass


    # Enter a parse tree produced by IRParser#and.
    def enterAnd(self, ctx:IRParser.AndContext):
        pass

    # Exit a parse tree produced by IRParser#and.
    def exitAnd(self, ctx:IRParser.AndContext):
        pass


    # Enter a parse tree produced by IRParser#or.
    def enterOr(self, ctx:IRParser.OrContext):
        pass

    # Exit a parse tree produced by IRParser#or.
    def exitOr(self, ctx:IRParser.OrContext):
        pass


    # Enter a parse tree produced by IRParser#not.
    def enterNot(self, ctx:IRParser.NotContext):
        pass

    # Exit a parse tree produced by IRParser#not.
    def exitNot(self, ctx:IRParser.NotContext):
        pass


    # Enter a parse tree produced by IRParser#notEqual.
    def enterNotEqual(self, ctx:IRParser.NotEqualContext):
        pass

    # Exit a parse tree produced by IRParser#notEqual.
    def exitNotEqual(self, ctx:IRParser.NotEqualContext):
        pass


    # Enter a parse tree produced by IRParser#equal.
    def enterEqual(self, ctx:IRParser.EqualContext):
        pass

    # Exit a parse tree produced by IRParser#equal.
    def exitEqual(self, ctx:IRParser.EqualContext):
        pass


    # Enter a parse tree produced by IRParser#larger.
    def enterLarger(self, ctx:IRParser.LargerContext):
        pass

    # Exit a parse tree produced by IRParser#larger.
    def exitLarger(self, ctx:IRParser.LargerContext):
        pass


    # Enter a parse tree produced by IRParser#smaller.
    def enterSmaller(self, ctx:IRParser.SmallerContext):
        pass

    # Exit a parse tree produced by IRParser#smaller.
    def exitSmaller(self, ctx:IRParser.SmallerContext):
        pass


    # Enter a parse tree produced by IRParser#largerEqual.
    def enterLargerEqual(self, ctx:IRParser.LargerEqualContext):
        pass

    # Exit a parse tree produced by IRParser#largerEqual.
    def exitLargerEqual(self, ctx:IRParser.LargerEqualContext):
        pass


    # Enter a parse tree produced by IRParser#smallerEqual.
    def enterSmallerEqual(self, ctx:IRParser.SmallerEqualContext):
        pass

    # Exit a parse tree produced by IRParser#smallerEqual.
    def exitSmallerEqual(self, ctx:IRParser.SmallerEqualContext):
        pass


    # Enter a parse tree produced by IRParser#largest.
    def enterLargest(self, ctx:IRParser.LargestContext):
        pass

    # Exit a parse tree produced by IRParser#largest.
    def exitLargest(self, ctx:IRParser.LargestContext):
        pass


    # Enter a parse tree produced by IRParser#smallest.
    def enterSmallest(self, ctx:IRParser.SmallestContext):
        pass

    # Exit a parse tree produced by IRParser#smallest.
    def exitSmallest(self, ctx:IRParser.SmallestContext):
        pass


    # Enter a parse tree produced by IRParser#sum.
    def enterSum(self, ctx:IRParser.SumContext):
        pass

    # Exit a parse tree produced by IRParser#sum.
    def exitSum(self, ctx:IRParser.SumContext):
        pass


    # Enter a parse tree produced by IRParser#average.
    def enterAverage(self, ctx:IRParser.AverageContext):
        pass

    # Exit a parse tree produced by IRParser#average.
    def exitAverage(self, ctx:IRParser.AverageContext):
        pass


    # Enter a parse tree produced by IRParser#valueByUnion.
    def enterValueByUnion(self, ctx:IRParser.ValueByUnionContext):
        pass

    # Exit a parse tree produced by IRParser#valueByUnion.
    def exitValueByUnion(self, ctx:IRParser.ValueByUnionContext):
        pass


    # Enter a parse tree produced by IRParser#valueByAggregate.
    def enterValueByAggregate(self, ctx:IRParser.ValueByAggregateContext):
        pass

    # Exit a parse tree produced by IRParser#valueByAggregate.
    def exitValueByAggregate(self, ctx:IRParser.ValueByAggregateContext):
        pass


    # Enter a parse tree produced by IRParser#valueByAttribute.
    def enterValueByAttribute(self, ctx:IRParser.ValueByAttributeContext):
        pass

    # Exit a parse tree produced by IRParser#valueByAttribute.
    def exitValueByAttribute(self, ctx:IRParser.ValueByAttributeContext):
        pass


    # Enter a parse tree produced by IRParser#valueAtom.
    def enterValueAtom(self, ctx:IRParser.ValueAtomContext):
        pass

    # Exit a parse tree produced by IRParser#valueAtom.
    def exitValueAtom(self, ctx:IRParser.ValueAtomContext):
        pass


    # Enter a parse tree produced by IRParser#text.
    def enterText(self, ctx:IRParser.TextContext):
        pass

    # Exit a parse tree produced by IRParser#text.
    def exitText(self, ctx:IRParser.TextContext):
        pass


    # Enter a parse tree produced by IRParser#quantity.
    def enterQuantity(self, ctx:IRParser.QuantityContext):
        pass

    # Exit a parse tree produced by IRParser#quantity.
    def exitQuantity(self, ctx:IRParser.QuantityContext):
        pass


    # Enter a parse tree produced by IRParser#date.
    def enterDate(self, ctx:IRParser.DateContext):
        pass

    # Exit a parse tree produced by IRParser#date.
    def exitDate(self, ctx:IRParser.DateContext):
        pass


    # Enter a parse tree produced by IRParser#Month.
    def enterMonth(self, ctx:IRParser.MonthContext):
        pass

    # Exit a parse tree produced by IRParser#Month.
    def exitMonth(self, ctx:IRParser.MonthContext):
        pass


    # Enter a parse tree produced by IRParser#year.
    def enterYear(self, ctx:IRParser.YearContext):
        pass

    # Exit a parse tree produced by IRParser#year.
    def exitYear(self, ctx:IRParser.YearContext):
        pass


    # Enter a parse tree produced by IRParser#time.
    def enterTime(self, ctx:IRParser.TimeContext):
        pass

    # Exit a parse tree produced by IRParser#time.
    def exitTime(self, ctx:IRParser.TimeContext):
        pass


    # Enter a parse tree produced by IRParser#entity.
    def enterEntity(self, ctx:IRParser.EntityContext):
        pass

    # Exit a parse tree produced by IRParser#entity.
    def exitEntity(self, ctx:IRParser.EntityContext):
        pass


    # Enter a parse tree produced by IRParser#attribute.
    def enterAttribute(self, ctx:IRParser.AttributeContext):
        pass

    # Exit a parse tree produced by IRParser#attribute.
    def exitAttribute(self, ctx:IRParser.AttributeContext):
        pass


    # Enter a parse tree produced by IRParser#concept.
    def enterConcept(self, ctx:IRParser.ConceptContext):
        pass

    # Exit a parse tree produced by IRParser#concept.
    def exitConcept(self, ctx:IRParser.ConceptContext):
        pass


    # Enter a parse tree produced by IRParser#predicate.
    def enterPredicate(self, ctx:IRParser.PredicateContext):
        pass

    # Exit a parse tree produced by IRParser#predicate.
    def exitPredicate(self, ctx:IRParser.PredicateContext):
        pass


    # Enter a parse tree produced by IRParser#qualifier.
    def enterQualifier(self, ctx:IRParser.QualifierContext):
        pass

    # Exit a parse tree produced by IRParser#qualifier.
    def exitQualifier(self, ctx:IRParser.QualifierContext):
        pass


    # Enter a parse tree produced by IRParser#value.
    def enterValue(self, ctx:IRParser.ValueContext):
        pass

    # Exit a parse tree produced by IRParser#value.
    def exitValue(self, ctx:IRParser.ValueContext):
        pass


    # Enter a parse tree produced by IRParser#number.
    def enterNumber(self, ctx:IRParser.NumberContext):
        pass

    # Exit a parse tree produced by IRParser#number.
    def exitNumber(self, ctx:IRParser.NumberContext):
        pass


    # Enter a parse tree produced by IRParser#string.
    def enterString(self, ctx:IRParser.StringContext):
        pass

    # Exit a parse tree produced by IRParser#string.
    def exitString(self, ctx:IRParser.StringContext):
        pass



del IRParser