# GraphQ Trans

![Icon](./docs/imgs/icon.png)

<p> GraphQ Trans is an integrated system that supports the translation from natural language to graph query language as well as the transpilation among different query languages. Specifically, GraphQ Trans provides a user-friendly interface that automati- cally translates natural language questions  into various graph query languages in order to ease end-user interaction with heterogeneous graph database backend. </p>

For our demonstration website, please visit https://graphqtrans.xlore.cn/index

## Setup Environment

This toolkit relies on [ANTLR4](https://github.com/antlr/antlr4) for parse tree generation. The Python package has the following dependencies:

* Python >= 3.6.2

* Java >= 11

* ANTLR >= 4.9.2

* antlr4-python3-runtime >= 4.9.2

## Quick Start

GraphQ Trans provides a set of easy-to-use translators for converting graph query languages. Here's a simple example of how to use the toolkit to convert between two graph query languages:

```python
from graphq_ir.sparql.translator import Translator as SparqlTranslator
from graphq_ir.ir.translator import Translator as IRTranslator

sparql_translator = SparqlTranslator() # Create a SparqlTranslator that translates SPARQL to graphqIR
ir_translator = IRTranslator() # Create a IRTranslator that translates graphqIR to Cypher

# the SPARQL query for "Get all entities that are human"
sparql_query = 'SELECT DISTINCT ?e WHERE { ?e <pred:instance_of> ?c . ?c <pred:name> "human" } '

ir = sparql_translator.to_ir(sparql_query)
print(ir)

cypher_query = ir_translator.to_cypher(ir)
print(cypher_query) 
```

The returned Cypher query will be:

```cypher
MATCH (n1:human)
RETURN n1.name
```

## Supported Features
To see the exact features in each graph query languages that we support, you may check out the .md file for each language.

## Style Requirement
### SPARQL

Our SPARQL naming rules are adopted from KBQA dataset [KQA Pro](http://thukeg.gitee.io/kqa-pro/). For variables, we have

| Schema    | Naming Style        | Example                         |
|-----------|---------------------|---------------------------------|
| Entity    | ?e, ?e_1, ?e_2, ... | ?e_1 \<nationality> "British" . |
| Concept   | ?c, ?c_1, ?c_2, ... | ?c \<pred:name> "human" .       |
| Predicate | ?r, ?r_1, ?r_2, ... | ?e ?r ?e_1 .                    |
| Attribute | ?pv, ?pv_1, ...     | ?e_2 \<duration> ?pv_3 .        |
| Value     | ?v, ?v_1, ?v_2, ... | ?pv \<pred:value>  ?v_1 .       |

For common predicates, we have

| Predicate   | Format              | Example                             |
|-------------|---------------------|-------------------------------------|
| Label       | \<pred:name>        | ?e_1 \<nationality> "British" .     |
| Instance of | \<pred:instance_of> | ?c \<pred:name> "human" .           |
| Value is    | \<pred:value>       | ?pv \<pred:value> "42"^^xsd:double. |
| Unit        | \<pred:unit>        | ?pv \<pred:unit> "month" .          |

### Cypher
For convenience of KBQA, we design the transpiler based on the need of getting the labels directly. Therefore, to query variable _**x**_, please use

```cypher
...
RETURN x.name
...
```


### KoPL
For KoPL, we support all styles that satisfy the language grammar. To see more specific instrution, please refer to their public repository https://github.com/THU-KEG/KoPL

### Lambda-DCS
For lambda-DCS, please refers to the original paper [(Liang, 2013)](https://arxiv.org/abs/1309.4408) for more specific instructions
