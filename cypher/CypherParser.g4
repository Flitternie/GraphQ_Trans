parser grammar CypherParser;

options { tokenVocab = CypherLexer; }

root
    : matchClause+ returnClause orderByClause? limitClause? EOF
    ;

matchClause
    : Match path ( Where constraint )?
    ;

returnClause
    : Return Distinct? ( variable | variableAttribute ) ( As variable )?
    ;

orderByClause
    : OrderBy (variable | variableAttribute)
    ;

limitClause
    : Limit INTEGER
    ;

path
    : node ( ( ( TOLEFT relationship? UND ) | ( UND relationship? UND ) | ( UND relationship? TORIGHT ) ) node )*
    ;

node
    : LP variable? ( COL nodeLabel )+ nodePropertyConstraint? RP
    | LP variable ( COL nodeLabel )* nodePropertyConstraint? RP
    ;

nodeLabel
    : varString
    ;

nodePropertyConstraint
    : LB nodeProperty ( COMMA nodeProperty )* RB
    ;

relationship
    : LSB variable? COL relationshipLabel ( OR COL relationshipLabel )? RSB
    | LSB variable ( COL relationshipLabel ( OR COL relationshipLabel )? )? RSB
    ;

relationshipLabel
    : varString
    ;

constraint
    : ( variable | variableAttribute ) symbolOP value
    ;

symbolOP
    : EQ
    | NEQ
    | GTE
    | GT
    | LTE    
    | LT
    ;

variable
    : varString
    ;

variableAttribute
    : variable DOT variable
    ;

nodeProperty
    : variable COL value
    ;

value
    : string
    | SEP string SEP
    ;

varString
    : ( STRING_LITERAL | INTEGER )+
    ;

string
    : ( STRING_LITERAL | STRING_SYMBOL | INTEGER | DOT )+
    ;
