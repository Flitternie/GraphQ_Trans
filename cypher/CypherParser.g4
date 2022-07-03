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
    : node ( (UND relationship? TORIGHT |TOLEFT relationship? UND | UND relationship? UND) node )*
    ;

node
    : LP string? C string (LB attribute RB)? RP
    | LP string (C string )? (LB attribute RB)? RP
    ;

relationship
    : LSB string? C string (OR C string)? RSB
    | LSB string (C string (OR C string)? )? RSB
    ;

constraint
    : attribute EQUAL SEP string SEP
    | attribute EQUAL string
    ;

attribute
    : var DOT string
    ;

var
    : string
    ;


string
    : ( STRING_LITERAL | INTEGER | DOT | UND )+
    ;
