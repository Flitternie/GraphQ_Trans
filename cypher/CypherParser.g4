parser grammar CypherParser;

options { tokenVocab = CypherLexer; }

root
    : matchClause+ Return Distinct? var orderByClause? limitClause? EOF
    ;

matchClause
    : Match path ( Where constraint )?
    ;

orderByClause
    : OrderBy var
    ;

limitClause
    : Limit INTEGER
    ;

path
    : node ( (UND relation? TORIGHT | TOLEFT relation? UND | UND relation? UND) node )*
    ;

node
    : LP string? C string (LB attribute (COMMA attribute)* RB)? RP
    | LP string (C string )? (LB attribute (COMMA attribute)* RB)? RP
    ;

relation
    : LSB string? C string (OR C string)? RSB
    | LSB string (C string (OR C string)? )? RSB
    ;

constraint
    : var symbolOP SEP string SEP
    | var symbolOP string
    ;

symbolOP
    : EQUAL
    | INEQUAL
    | LESS
    | GREATER
    | LOE
    | GOE
    ;


var
    : string # variable
    | string DOT string # variableAttribute
    ;

attribute
    : string C string
    ;

string
    : ( STRING_LITERAL | INTEGER | UND )+
    ;
