import os
import re
from antlr4 import *

from graphq_trans.ir.IRLexer import IRLexer
from graphq_trans.ir.IRParser import IRParser
from graphq_trans.ir.IRParserListener import IRParserListener

from graphq_trans.utils import *

overnight_domains = ['basketball', 'blocks', 'calendar', 'housing', 'publications', 'recipes', 'restaurants', 'socialnetwork']


def read_grammar(file_path):
    grammar = {}
    for domain in overnight_domains:
        domain_grammar = {}
        with open(os.path.join(file_path, domain + '.grammar'), 'r') as f:
            for line in f:
                if line.strip().startswith('#') or line == '\n':
                    continue
                # elif re.match(r'.*for \@x \((.*?)\)', line):
                #     iter_element = re.match(r'.*for \@x \((.*?)\)', line).group(1).split()
                rule = re.findall(r'\(rule \$(.*?) \((.*?)\) \(ConstantFn (.*)\)\)', line)
                if rule:
                    type = re.sub(r'[0-9]', '', rule[0][0]).replace("/", "")
                    abbr = rule[0][1]
                    full = rule[0][2]
                    if type in domain_grammar.keys():
                        # domain_grammar[type][abbr] = full
                        domain_grammar[type].append(full)
                    else:
                        # domain_grammar[type] = {abbr: full}
                        domain_grammar[type] = [full]
            for type in domain_grammar.keys():
                # domain_grammar[type] = dict(sorted(domain_grammar[type].items()))
                domain_grammar[type] = sorted(sorted(domain_grammar[type]), key=len, reverse=False)
            grammar[domain] = domain_grammar
    return grammar



class OvernightEmitter(IRParserListener):
    def __init__(self, ungrounded=False):
        self.output = ""
        self.domain = None
        self.ungrounded = ungrounded
        
        PREFIX = "call SW"
        self.func = {
            "listValue":                PREFIX + ".listValue",
            "size":                     "call .size",
            "domain":                   PREFIX + ".domain",
            "singleton":                PREFIX + ".singleton",
            "filter":                   PREFIX + ".filter",
            "getProperty":              PREFIX + ".getProperty",
            "superlative":              PREFIX + ".superlative",
            "countSuperlative":         PREFIX + ".countSuperlative",
            "countComparative":         PREFIX + ".countComparative",
            "aggregate":                PREFIX + ".aggregate",
            "concat":                   PREFIX + ".concat",
            "reverse":                  PREFIX + ".reverse",
            "ensureNumericProperty":    PREFIX + ".ensureNumericProperty",
            "ensureNumericEntity":      PREFIX + ".ensureNumericEntity",
            "and":                      PREFIX + ".and",
            "or":                       PREFIX + ".or",
        }
        if ungrounded:
            self.grammar = None
        else:
            self.grammar = read_grammar(os.path.join(os.path.dirname(__file__), "../overnight/grammar/"))
        
    
    def initialize(self):
        self.output = ""
    
    def set_domain(self, domain):
        self.domain = domain

    def emit(self, ctx):
        return self.output

    def get_full_name(self, abbr, datatype, domain):
        datatype = [datatype] if isinstance(datatype, str) else datatype
        if self.ungrounded:
            abbr = abbr.replace(" ", "_")
            if datatype[0] in ["VP", "VPNP", "RelNP"]:
                return "( string {} )".format(abbr)
            elif datatype[0] == "TypeNP":
                return "en.{}".format(abbr)
            elif datatype[0] == "EntityNP":
                return "en.entity.{}".format(abbr)
            else:
                raise NotImplementedError("Unsupported datatype {}.".format(datatype))
        if domain:
            domain_datatype = [i for i in datatype if i in self.grammar[domain].keys()]
            for i in domain_datatype:
                # for name in self.grammar[domain][i].values():
                for name in self.grammar[domain][i]:
                    if abbr in name or abbr.replace(" ", "_") in name:
                        return name
        else:
            for domain in self.grammar.keys():
                domain_datatype = [i for i in datatype if i in self.grammar[domain].keys()]
                for i in domain_datatype:
                    # for name in self.grammar[domain][i].values():
                    for name in self.grammar[domain][i]:
                        if abbr in name or abbr.replace(" ", "_") in name:
                            return name
        return None
    
    def get_full_name_and_type(self, abbr, domain):
        results = {}
        if self.ungrounded:
            return {"TypeNP": "{}".format(abbr), "RelNP": "( string {} )".format(abbr)}
        if domain:
            for datatype in self.grammar[domain].keys():
                # for name in self.grammar[domain][datatype].values():
                for name in self.grammar[domain][datatype]:
                    if abbr in name or abbr.replace(" ", "_") in name:
                        results[datatype] = name
                        break
        else:
            for domain in self.grammar.keys():
                for datatype in self.grammar[domain].keys():
                    # for name in self.grammar[domain][datatype].values():
                    for name in self.grammar[domain][datatype]:
                        if abbr in name or abbr.replace(" ", "_") in name:
                            results[datatype] = name
                            break
        return results
    
    def process_value(self, value_type, value):
        value = value.replace(" : ", " ") if value_type == "time" else value
        return "( {} {} )".format(value_type, value) if value_type != "" else value



    def enterRoot(self, ctx: IRParser.RootContext):
        self.initialize()
        ctx.slots = strictDict({"LF": ""})
        return super().enterRoot(ctx)

    def exitRoot(self, ctx: IRParser.RootContext):
        self.output = ctx.slots["LF"]
        return super().exitRoot(ctx)    
    
    def enterEntityQuery(self, ctx: IRParser.EntityQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet()})
        return super().enterEntityQuery(ctx)
    
    def exitEntityQuery(self, ctx: IRParser.EntityQueryContext):
        ctx.parentCtx.slots["LF"] = "( {} {} )".format(self.func["listValue"], ctx.slots["entitySet"])
        return super().exitEntityQuery(ctx)
    
    def enterAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "attribute": ""})
        return super().enterAttributeQuery(ctx)
    
    def exitAttributeQuery(self, ctx: IRParser.AttributeQueryContext):
        subquery = "( {} {} {} )".format(self.func["getProperty"], ctx.slots["entitySet"], ctx.slots["attribute"])
        ctx.parentCtx.slots["LF"] = "( {} {} )".format(self.func["listValue"], subquery)
        return super().exitAttributeQuery(ctx)
    
    def enterCountQuery(self, ctx: IRParser.CountQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet()})
        return super().enterCountQuery(ctx)
    
    def exitCountQuery(self, ctx: IRParser.CountQueryContext):
        subquery = "( {} {} )".format(self.func["size"], ctx.slots["entitySet"])
        ctx.parentCtx.slots["LF"] = "( {} {} )".format(self.func["listValue"], subquery)
        return super().exitCountQuery(ctx)
    
    def enterSelectQuery(self, ctx: IRParser.SelectQueryContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "attribute": "", "op": ""})
        return super().enterSelectQuery(ctx)
    
    def exitSelectQuery(self, ctx: IRParser.SelectQueryContext):
        if ctx.slots["entitySet"].is_pop:
            subquery = "( lambda s ( {} ( var s ) {} {} ) )".format(self.func["superlative"], ctx.slots["op"], ctx.slots["attribute"])
        else:
            subquery = "( {} {} {} {} )".format(self.func["superlative"], ctx.slots["entitySet"], ctx.slots["op"], ctx.slots["attribute"])
        ctx.parentCtx.slots["LF"] = "( {} {} )".format(self.func["listValue"], subquery)
        return super().exitSelectQuery(ctx)

    def enterValueQuery(self, ctx: IRParser.ValueQueryContext):
        ctx.slots = strictDict({"value": ""})
        return super().enterValueQuery(ctx)
    
    def exitValueQuery(self, ctx: IRParser.ValueQueryContext):
        ctx.parentCtx.slots["LF"] = "( {} {} )".format(self.func["listValue"], ctx.slots["value"])
        return super().exitValueQuery(ctx)
    
    def enterEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        ctx.slots = strictDict({"entitySet": [], "setOP": ""})
        return super().enterEntitySetGroup(ctx)
    
    def exitEntitySetGroup(self, ctx: IRParser.EntitySetGroupContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        if ctx.slots["setOP"] == "or":    
            insert(ctx.parentCtx, "( {} {} {} )".format(self.func["concat"], ctx.slots["entitySet"][0], ctx.slots["entitySet"][1]))
        elif ctx.slots["setOP"] == "and":
            insert(ctx.parentCtx, "( {} {} {} )".format(self.func["and"], ctx.slots["entitySet"][0], ctx.slots["entitySet"][1]))
        else:
            raise NotImplementedError("Unsupported set operator {}.".format(ctx.slots["setOP"]))
        return super().exitEntitySetGroup(ctx)
    
    def enterEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        ctx.slots = strictDict({"entitySet": []})
        return super().enterEntitySetIntersect(ctx)
    
    def exitEntitySetIntersect(self, ctx: IRParser.EntitySetIntersectContext):
        assert isinstance(ctx.slots["entitySet"], list) and len(ctx.slots["entitySet"]) == 2
        insert(ctx.parentCtx, "( {} {} {} )".format(self.func["and"], ctx.slots["entitySet"][0], ctx.slots["entitySet"][1]))
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
        insert(ctx.parentCtx, ctx.slots["entity"], is_atom=True)
        return super().exitEntitySetAtom(ctx)
    
    def exitEntitySetPlaceholder(self, ctx: IRParser.EntitySetPlaceholderContext):
        insert(ctx.parentCtx, "", is_pop=True)
        return super().exitEntitySetPlaceholder(ctx)
    
    def enterEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        ctx.slots = strictDict({"concept":"", "entitySet": entitySet(), "attribute": "", "op": "", "value": ""})
        return super().enterEntitySetByAttribute(ctx)
    
    def exitEntitySetByAttribute(self, ctx: IRParser.EntitySetByAttributeContext):
        if ctx.slots["entitySet"].is_pop:
            assert ctx.slots["concept"] == ""
            subquery = "( lambda s ( {} ( var s ) {} {} {} ) )".format(self.func["filter"], ctx.slots["attribute"], ctx.slots["op"], ctx.slots["value"])
        elif ctx.slots["concept"] == "":
            subquery = "( {} {} {} {} {} )".format(self.func["filter"], ctx.slots["entitySet"], ctx.slots["attribute"], ctx.slots["op"], ctx.slots["value"])
        else:
            subquery = "( {} ( {} ( {} {} ) ( string ! type ) ) {} {} {} )".format(self.func["filter"], self.func["getProperty"], self.func["singleton"], ctx.slots["concept"], ctx.slots["attribute"], ctx.slots["op"], ctx.slots["value"])
        insert(ctx.parentCtx, subquery)
        return super().exitEntitySetByAttribute(ctx)
    
    def enterFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        ctx.slots = strictDict({"attribute": "", "op": "", "value": ""})
        return super().enterFilterByAttribute(ctx)
    
    def exitFilterByAttribute(self, ctx: IRParser.FilterByAttributeContext):
        ctx.parentCtx.slots["attribute"] = ctx.slots["attribute"]
        ctx.parentCtx.slots["op"] = ctx.slots["op"]
        # can be further restricted by ( call SW.ensureNumericProperty {} )
        ctx.parentCtx.slots["value"] = ctx.slots["value"]
        return super().exitFilterByAttribute(ctx)
    

    
    def enterEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        ctx.slots = strictDict({"entitySet": entitySet(), "op": "", "attribute": ""})
        return super().enterEntitySetByRank(ctx)
    
    def exitEntitySetByRank(self, ctx: IRParser.EntitySetByRankContext):
        if ctx.slots["entitySet"].is_pop:
            subquery = "( lambda s ( {} ( var s ) {} {} ) )".format(self.func["superlative"], ctx.slots["op"], ctx.slots["attribute"])
        else:
            subquery = "( {} {} {} {} )".format(self.func["superlative"], ctx.slots["entitySet"], ctx.slots["op"], ctx.slots["attribute"])
        insert(ctx.parentCtx, subquery)
        return super().exitEntitySetByRank(ctx)
    
    def enterFilterByRank(self, ctx: IRParser.FilterByRankContext):
        ctx.slots = strictDict({"op": "", "attribute": ""})
        return super().enterFilterByRank(ctx)
    
    def exitFilterByRank(self, ctx: IRParser.FilterByRankContext):
        ctx.parentCtx.slots["op"] = ctx.slots["op"]
        ctx.parentCtx.slots["attribute"] = ctx.slots["attribute"]
        return super().exitFilterByRank(ctx)
    


    def enterEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        ctx.slots = strictDict({"concept": "", "entitySet": [], "gate": True, "predicate": "", "op": "", "value": ""})
        return super().enterEntitySetByPredicate(ctx)
    
    def exitEntitySetByPredicate(self, ctx: IRParser.EntitySetByPredicateContext):
        if ctx.slots["entitySet"][0].is_pop:
            ctx.slots["entitySet"][0] = ctx.slots["entitySet"][0].reassign("( var s )")
        if ctx.slots["op"] == "" and ctx.slots["value"] == "":
            ctx.slots["gate"] = "=" if ctx.slots["gate"] else "! ="
            if len(ctx.slots["entitySet"]) == 1:
                if ctx.slots["concept"]:
                    subquery = entitySet("( {} ( {} {} ) ( string ! type ) )".format(self.func["getProperty"], self.func["singleton"], ctx.slots["concept"]))
                    ctx.slots["entitySet"].insert(0, subquery)
                # LB filterFunc constraintNP predicate RB
                if ctx.slots["entitySet"][1].is_pop:
                    subquery = "( {} {} {} )".format(self.func["filter"], ctx.slots["entitySet"][0], ctx.slots["predicate"])
                else:
                    subquery = "( {} {} {} ( string {} ) {} )".format(self.func["filter"], ctx.slots["entitySet"][0], ctx.slots["predicate"], ctx.slots["gate"], ctx.slots["entitySet"][1])
            else:
                if ctx.slots["concept"]:
                    ctx.slots["entitySet"][0] = ctx.slots["entitySet"][0].reassign("( {} {} ( {} {} ) )".format(self.func["getProperty"], ctx.slots["entitySet"][0], self.func["reverse"], ctx.slots["concept"]))
                # LB filterFunc constraintNP predicate op np RB
                # LB filterFunc constraintNP reversePredicate op np RB
                if ctx.slots["entitySet"][1].is_pop:
                    subquery = "( {} {} {} )".format(self.func["filter"], ctx.slots["entitySet"][0], ctx.slots["predicate"])
                else:
                    subquery = "( {} {} {} ( string {} ) {} )".format(self.func["filter"], ctx.slots["entitySet"][0], ctx.slots["predicate"], ctx.slots["gate"], ctx.slots["entitySet"][1])
        
        elif "min" in ctx.slots["op"] or "max" in ctx.slots["op"] and ctx.slots["value"] == "":
            if ctx.slots["concept"]:
                    ctx.slots["entitySet"][0] = ctx.slots["entitySet"][0].reassign("( {} {} ( {} {} ) )".format(self.func["getProperty"], ctx.slots["entitySet"][0], self.func["reverse"], ctx.slots["concept"]))
            
            if len(ctx.slots["entitySet"]) == 1:
                # LB countSuperlative constraintNP op relNP RB
                subquery = "( {} {} {} {} )".format(self.func["countSuperlative"], ctx.slots["entitySet"][0], ctx.slots["op"], ctx.slots["predicate"])
            else:
                # LB countSuperlative constraintNP op predicate np RB
                if ctx.slots["entitySet"][1].is_pop:
                    subquery = "( {} {} {} {} )".format(self.func["countSuperlative"], ctx.slots["entitySet"][0], ctx.slots["op"], ctx.slots["predicate"])
                else:
                    subquery = "( {} {} {} {} {} )".format(self.func["countSuperlative"], ctx.slots["entitySet"][0], ctx.slots["op"], ctx.slots["predicate"], ctx.slots["entitySet"][1])
               
        elif ctx.slots["value"] != "":
            ctx.slots["op"] = "( string = )" if ctx.slots["op"] == "" else ctx.slots["op"]
            if ctx.slots["concept"]:
                    ctx.slots["entitySet"][0] = ctx.slots["entitySet"][0].reassign("( {} {} ( {} {} ) )".format(self.func["getProperty"], ctx.slots["entitySet"][0], self.func["reverse"], ctx.slots["concept"]))
                    
            if len(ctx.slots["entitySet"]) == 1:
                # LB countComparative constraintNP relNP op value RB
                subquery = "( {} {} {} {} {} )".format(self.func["countComparative"], ctx.slots["entitySet"][0], ctx.slots["predicate"], ctx.slots["op"], ctx.slots["value"])
            else:
                # LB countComparative constraintNP predicate op value np RB
                # LB countComparative constraintNP reversePredicate op value np RB
                if ctx.slots["entitySet"][1].is_pop:
                    subquery = "( {} {} {} {} {} )".format(self.func["countComparative"], ctx.slots["entitySet"][0], ctx.slots["predicate"], ctx.slots["op"], ctx.slots["value"])
                else:
                    subquery = "( {} {} {} {} {} {} )".format(self.func["countComparative"], ctx.slots["entitySet"][0], ctx.slots["predicate"], ctx.slots["op"], ctx.slots["value"], ctx.slots["entitySet"][1])
        else:
            raise NotImplementedError("Unsupported operator or value format.")
        
        if ctx.slots["entitySet"][0].is_pop:
            subquery = "( lambda s {} )".format(subquery)
        
        insert(ctx.parentCtx, subquery)
        return super().exitEntitySetByPredicate(ctx)
    
    def enterFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        ctx.slots = strictDict({"gate": True, "predicate": "", "direction": "", "op": "", "value": ""})
        return super().enterFilterByPredicate(ctx)
    
    def exitFilterByPredicate(self, ctx: IRParser.FilterByPredicateContext):
        ctx.parentCtx.slots["gate"] = ctx.slots["gate"] 
        ctx.parentCtx.slots["predicate"] = ctx.slots["predicate"] if ctx.slots["direction"] == "forward" else "( {} {} )".format(self.func["reverse"], ctx.slots["predicate"])
        ctx.parentCtx.slots["op"] = ctx.slots["op"]
        ctx.parentCtx.slots["value"] = ctx.slots["value"]
        return super().exitFilterByPredicate(ctx)



    def enterEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        ctx.slots = strictDict({"concept":"", "entitySet": entitySet()})
        return super().enterEntitySetByConcept(ctx)

    def exitEntitySetByConcept(self, ctx: IRParser.EntitySetByConceptContext):
        concept = self.get_full_name_and_type(ctx.slots["concept"], domain=self.domain)
        if ctx.slots["entitySet"] == "":
                # type + CP (through typeConstraintNP)
                assert "TypeNP" in concept.keys()
                subquery = "( {} ( {} {} ) ( string ! type ) )".format(self.func["getProperty"], self.func["singleton"], concept["TypeNP"])
        else:
            assert "RelNP" in concept.keys()
            if ctx.slots["entitySet"].is_atom:
                subquery = "( {} {} ( {} {} ) )".format(self.func["getProperty"], ctx.slots["entitySet"], self.func["reverse"], concept["RelNP"])
            elif isinstance(ctx.parentCtx.parentCtx, (IRParser.AttributeQueryContext, IRParser.EntitySetByAttributeContext, IRParser.ValueByAttributeContext)):
                # reversePredicate + CP (through eventConstraintNP)
                subquery = "( {} {} ( {} {} ) )".format(self.func["getProperty"], ctx.slots["entitySet"], self.func["reverse"], concept["RelNP"])
            elif isinstance(ctx.parentCtx, IRParser.EntitySetByPredicateContext):
                if ctx.parentCtx.slots["entitySet"][0] != "":
                    # reversePredicate + CP (through eventConstraintNP)
                    subquery = "( {} {} ( {} {} ) )".format(self.func["getProperty"], ctx.slots["entitySet"], self.func["reverse"], concept["RelNP"])
                else:
                    # relNP + CP (through domainCPNP)
                    subquery = "( {} ( {} ( {} {} ) ) {} )".format(self.func["getProperty"], ctx.slots["entitySet"], self.func["domain"], concept["RelNP"], concept["RelNP"])
            else:
                # relNP + CP (through domainCPNP)
                subquery = "( {} ( {} ( {} {} ) ) {} )".format(self.func["getProperty"], ctx.slots["entitySet"], self.func["domain"], concept["RelNP"], concept["RelNP"])
        insert(ctx.parentCtx, subquery)
        return super().exitEntitySetByConcept(ctx)

    
    def enterFilterByQualifier(self, ctx: IRParser.FilterByQualifierContext):
        raise NotImplementedError("Qualifier constraints not supported by Lambda-DCS.")



    def enterValueByAttribute(self, ctx: IRParser.ValueByAttributeContext):
        ctx.slots = strictDict({"attribute": "", "entitySet": entitySet()})
        return super().enterValueByAttribute(ctx)
    
    def exitValueByAttribute(self, ctx: IRParser.ValueByAttributeContext):
        # can be further restricted by ( call SW.ensureNumericEntity {} )
        ctx.parentCtx.slots["value"] = "( {} {} {} )".format(self.func["getProperty"], ctx.slots["entitySet"], ctx.slots["attribute"])
        return super().exitValueByAttribute(ctx)
    
    def enterValueByAggregate(self, ctx: IRParser.ValueByAggregateContext):
        ctx.slots = strictDict({"aggregate": "", "value": ""})
        return super().enterValueByAggregate(ctx)
    
    def exitValueByAggregate(self, ctx: IRParser.ValueByAggregateContext):
        ctx.parentCtx.slots["value"] = "( {} {} {} )".format(self.func["aggregate"], ctx.slots["aggregate"], ctx.slots["value"])
        return super().exitValueByAggregate(ctx)
    
    def enterValueByUnion(self, ctx: IRParser.ValueByUnionContext):
        ctx.slots = strictDict({"valueType": "", "value": []})
        return super().enterValueByUnion(ctx)
    
    def exitValueByUnion(self, ctx: IRParser.ValueByUnionContext):
        assert isinstance(ctx.slots["value"], list) and len(ctx.slots["value"]) == 2
        for i in range(len(ctx.slots["value"])):
            ctx.slots["value"][i] = self.process_value(ctx.slots["valueType"], ctx.slots["value"][i])
        ctx.parentCtx.slots["value"] = "( {} {} {} )".format(self.func["concat"], ctx.slots["value"][0], ctx.slots["value"][1])
        return super().exitValueByUnion(ctx)

    def enterValueAtom(self, ctx: IRParser.ValueAtomContext):
        ctx.slots = strictDict({"valueType": "", "value": ""})
        return super().enterValueAtom(ctx)
    
    def exitValueAtom(self, ctx: IRParser.ValueAtomContext):
        if len(ctx.slots["value"].split()) > 1:
            if len(ctx.slots["value"].split()) == 2:
                processed_value = " en.".join(ctx.slots["value"].split())
            else: 
                processed_value = ctx.slots["value"].split(maxsplit=1)
                processed_value = [processed_value[0], processed_value[1].replace(" ", "_")]
                processed_value = " en.".join(processed_value)
            full_value = self.get_full_name(processed_value, datatype=("EntityNP", "Value"), domain=self.domain) 
            ctx.slots["value"] = re.findall(r"\(.* ([0-9]* .*)\)", full_value)[0] if full_value and not self.ungrounded else ctx.slots["value"]

        value = self.process_value(ctx.slots["valueType"], ctx.slots["value"])
        if isinstance(ctx.parentCtx.slots["value"], list):
            ctx.parentCtx.slots["value"].append(value)
        else:
            ctx.parentCtx.slots["value"] = value
        return super().exitValueAtom(ctx)



    def enterEntity(self, ctx: IRParser.EntityContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterEntity(ctx)
    
    def exitEntity(self, ctx: IRParser.EntityContext):
        ctx.parentCtx.slots["entity"] = self.get_full_name(ctx.slots["string"], datatype="EntityNP", domain=self.domain)
        return super().exitEntity(ctx)
    
    def enterAttribute(self, ctx: IRParser.AttributeContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterAttribute(ctx)
    
    def exitAttribute(self, ctx: IRParser.AttributeContext):
        ctx.parentCtx.slots["attribute"] = self.get_full_name(ctx.slots["string"], datatype="RelNP", domain=self.domain)
        return super().exitAttribute(ctx)
    
    def enterConcept(self, ctx: IRParser.ConceptContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterConcept(ctx)
    
    def exitConcept(self, ctx: IRParser.ConceptContext):
        ctx.parentCtx.slots["concept"] = ctx.slots["string"]
        if self.domain is None and not ctx.slots["string"].startswith(".en"):
            ctx.parentCtx.slots["concept"] = self.get_full_name(ctx.slots["string"], datatype="TypeNP", domain=self.domain)
        return super().exitConcept(ctx)
    
    def enterPredicate(self, ctx: IRParser.PredicateContext):
        ctx.slots = strictDict({"string": ""})
        return super().enterPredicate(ctx)
    
    def exitPredicate(self, ctx: IRParser.PredicateContext):
        ctx.parentCtx.slots["predicate"] = self.get_full_name(ctx.slots["string"], datatype=("VP", "VPNP", "RelNP"), domain=self.domain)
        return super().exitPredicate(ctx)
    
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
    
    def exitNot(self, ctx: IRParser.NotContext):
        ctx.parentCtx.slots["gate"] = False
        return super().exitNot(ctx)
    
    def exitSum(self, ctx: IRParser.SumContext):
        ctx.parentCtx.slots["aggregate"] = "( string sum )"
        return super().exitSum(ctx)
    
    def exitAverage(self, ctx: IRParser.AverageContext):
        ctx.parentCtx.slots["aggregate"] = "( string avg )"
        return super().exitAverage(ctx)
    
    def exitLargest(self, ctx: IRParser.LargestContext):
        ctx.parentCtx.slots["op"] = "( string max )"
        return super().exitLargest(ctx)
    
    def exitSmallest(self, ctx: IRParser.SmallestContext):
        ctx.parentCtx.slots["op"] = "( string min )"
        return super().exitSmallest(ctx)

    def exitEqual(self, ctx: IRParser.EqualContext):
        ctx.parentCtx.slots["op"] = "( string = )"
        return super().exitEqual(ctx)
    
    def exitNotEqual(self, ctx: IRParser.NotEqualContext):
        ctx.parentCtx.slots["op"] = "( string ! = )"
        return super().exitNotEqual(ctx)
    
    def exitLarger(self, ctx: IRParser.LargerContext):
        ctx.parentCtx.slots["op"] = "( string > )"
        return super().exitLarger(ctx)
    
    def exitSmaller(self, ctx: IRParser.SmallerContext):
        ctx.parentCtx.slots["op"] = "( string < )"
        return super().exitSmaller(ctx)
    
    def exitLargerEqual(self, ctx: IRParser.LargerEqualContext):
        ctx.parentCtx.slots["op"] = "( string >= )"
        return super().exitLargerEqual(ctx)
    
    def exitSmallerEqual(self, ctx: IRParser.SmallerEqualContext):
        ctx.parentCtx.slots["op"] = "( string <= )"
        return super().exitSmallerEqual(ctx)
    
    def exitText(self, ctx: IRParser.TextContext):
        ctx.parentCtx.slots["valueType"] = "string"
        return super().exitText(ctx)
    
    def exitQuantity(self, ctx: IRParser.QuantityContext):
        ctx.parentCtx.slots["valueType"] = "number"
        return super().exitQuantity(ctx)

    def exitDate(self, ctx: IRParser.DateContext):
        ctx.parentCtx.slots["valueType"] = "date"
        return super().exitDate(ctx)
    
    def exitYear(self, ctx: IRParser.YearContext):
        ctx.parentCtx.slots["valueType"] = "year"
        return super().exitYear(ctx)
    
    def exitTime(self, ctx: IRParser.TimeContext):
        ctx.parentCtx.slots["valueType"] = "time"
        return super().exitTime(ctx)
    

    def enterString(self, ctx: IRParser.StringContext):
        if not isinstance(ctx.parentCtx, IRParser.StringContext):
            ctx.parentCtx.slots["string"] = str(ctx.getText()).strip()

    def enterNumber(self, ctx: IRParser.NumberContext):
        if not isinstance(ctx.parentCtx, IRParser.NumberContext):
            ctx.parentCtx.slots["number"] = str(ctx.getText()).strip()