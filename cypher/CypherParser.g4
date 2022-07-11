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
    : node ( ( ( UND | TOLEFT ) relation? ( UND | TORIGHT ) ) node )*
    ;

node
    : LP string? COL string nodePropertyConstraint? RP
    | LP string ( COL string )? nodePropertyConstraint? RP
    ;

nodePropertyConstraint
    : ( LB attribute ( COMMA attribute )* RB )
    ;

relation
    : LSB string? COL string ( OR COL string )? RSB
    | LSB string ( COL string ( OR COL string )? )? RSB
    ;

constraint
    : var symbolOP SEP string SEP
    | var symbolOP string
    ;

symbolOP
    : EQ
    | NEQ
    | GTE
    | GT
    | LTE    
    | LT
    ;

var
    : string # variable
    | string DOT string # variableAttribute
    ;

attribute
    : string COL string
    ;

string
    : ( STRING_LITERAL | INTEGER | UND )+
    ;
