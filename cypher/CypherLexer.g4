lexer grammar CypherLexer;

Call
    : 'CALL'
    ;
    
Match
    : 'MATCH'
    ;

Where
    : 'WHERE'
    ;

Return
    : 'RETURN'
    ;

With
    : 'WITH'
    ;

As
    : 'AS'
    ;

OrderBy
    : 'ORDER BY'
    ;

Limit
    : 'LIMIT'
    ;

Distinct
    : 'DISTINCT'
    ;

WS
    : ( '\t' | '\n' | '\r' )+ ->skip
    ;

SEP
    : '"' | '\''
    ;

LP
    : '('
    ;

RP
    : ')'
    ;

LB
    : '{'
    ;

COL
    : ':'
    ;

TORIGHT
    : '->'
    ;

TOLEFT
    : '<-'
    ;

UND
    : '-'
    ;

RB
    : '}'
    ;

LSB
    : '['
    ;

RSB
    : ']'
    ;

EQ
    : '='
    ;

NEQ
    : '<>'
    ;

GTE
    : '>='
    ;

GT
    : '>'
    ;

LTE
    : '<='
    ;

LT
    : '<'
    ;

DOT
    : '.'
    ;

INTEGER
    : DIGIT+
    ;

STRING_LITERAL
    : CHAR+
    ;

OR
    : '|'
    ;

COMMA
    : ','
    ;

SPACE
    : ' ' ->skip
    ;

fragment
DIGIT
    : '0'..'9'
    | [\p{Other_Number}]
    ;

fragment
CHAR
    : '!' | '/' | '\'' | '?' | '%' | '*' | '¡' | ',' | '_' 
    | [\p{Uppercase_Letter}\p{Lowercase_Letter}]
    | [\p{Math_Symbol}\p{Currency_Symbol}]
    ;