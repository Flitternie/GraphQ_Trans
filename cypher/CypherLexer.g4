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

VAR_STRING_LITERAL
    : VAR_CHAR +
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

fragment
DIGIT
    : '0'..'9'
    | [\p{Other_Number}]
    ;

fragment
VAR_CHAR
    : '_'
    | [\p{Uppercase_Letter}\p{Lowercase_Letter}]
    | [\p{Math_Symbol}\p{Currency_Symbol}]
    ;

fragment
CHAR
    : '!' | '/' | '\'' | '?' | '%' | '*' | '¡' | ',' | '_'
    | [\p{Uppercase_Letter}\p{Lowercase_Letter}]
    | [\p{Math_Symbol}\p{Currency_Symbol}]
    ;

WS
    : ( '\t' | '\n' | '\r' | ' ' )+ ->skip
    ;