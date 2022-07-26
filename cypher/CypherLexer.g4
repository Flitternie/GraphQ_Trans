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

Union
    : 'UNION'
    ;

With
    : 'WITH'
    ;

As
    : 'AS'
    ;

And
    : 'AND'
    ;

Or
    : 'OR'
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

CountFunction
    : 'count'
    ;

IsEmptyFunction
    : 'isEmpty'
    ;

Desc
    : 'DESC'
    ;

SEP
    : '\'' | '"'
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

STRING_SYMBOL
    : SYMBOL+
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
SYMBOL
    : '!' | '/' | '?' | '%' | '*' | '¡' | ','
    ;

fragment
CHAR
    : '_'
    | [\p{Uppercase_Letter}\p{Lowercase_Letter}]
    | [\p{Math_Symbol}\p{Currency_Symbol}]
    ;

WS
    : ( '\t' | '\n' | '\r' | ' ' )+ ->skip
    ;