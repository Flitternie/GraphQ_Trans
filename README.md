![Icon](./docs/imgs/icon.png)

[![Downloads](https://static.pepy.tech/badge/graphq_trans)](https://pepy.tech/project/graphq_trans)
[![Downloads](https://static.pepy.tech/badge/graphq_trans/month)](https://pepy.tech/project/graphq_trans)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg?style=flat)](https://github.com/flitternie/graphq_trans/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


GraphQ Trans is a source-to-source compiler that supports the transpilation among multiple graph query languages via a unified intermediate representation. You may install this package via pip:

```bash
pip install graphq_trans
```

For our demonstration website, please visit https://graphqtrans.xlore.cn/

## Setup Environment

This package has the following dependencies:

* Python >= 3.6.2

* ANTLR >= 4.9.2

* antlr4-python3-runtime >= 4.9.2

This toolkit relies on [ANTLR4](https://github.com/antlr/antlr4) for front-end analysis, please refer to their [tutorial](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md) for setup. 

## Quick Start

GraphQ Trans provides a set of easy-to-use APIs for transpiling graph query languages. Here's a simple example of how to use the toolkit to convert between two graph query languages:

```python
from graphq_trans.sparql.translator import Translator as SparqlTranslator
from graphq_trans.ir.translator import Translator as IRTranslator

sparql_translator = SparqlTranslator() # Create a SparqlTranslator that translates SPARQL to graphqIR
ir_translator = IRTranslator() # Create a IRTranslator that translates graphqIR to Cypher

# the SPARQL query for "Get all entities that are human"
sparql_query = 'SELECT DISTINCT ?e WHERE { ?e <pred:instance_of> ?c . ?c <pred:name> "human" } '

ir = sparql_translator.to_ir(sparql_query) # translates sparql to ir
cypher_query = ir_translator.to_cypher(ir) # translates ir to cypher
print(cypher_query) 
```

The returned Cypher query will be:

```cypher
MATCH (n1:human)
RETURN n1.name
```


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
For KoPL, we support all styles that satisfy the language grammar. Please refer to their repository for detailed documentation: https://github.com/THU-KEG/KoPL

### Lambda-DCS
For lambda-DCS, please refers to the original paper [(Liang, 2013)](https://arxiv.org/abs/1309.4408) for more specific instructions

## Citation

If you find our work helpful, please cite it as follows:

```
@inproceedings{nie2022graphq,
  title={GraphQ IR: Unifying the Semantic Parsing of Graph Query Languages with One Intermediate Representation},
  author={Nie, Lunyiu and Cao, Shulin and Shi, Jiaxin and Sun, Jiuding and Tian, Qi and Hou, Lei and Li, Juanzi and Zhai, Jidong},
  booktitle={Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing},
  pages={5848--5865},
  year={2022}
}
```

