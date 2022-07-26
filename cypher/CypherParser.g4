parser grammar CypherParser;

options { tokenVocab = CypherLexer; }

root
    : queryBlock (Union queryBlock)* limitClause? EOF
    ;

queryBlock
    : matchClause+ returnClause orderByClause?
    ;

matchClause
    : Match path ( Where constraint )?
    | Match path ( Where LP constraint (logicOP constraint)+ RP )
    ;

returnClause
    : Return Distinct? ( specialQuery | variableAttribute | variable ) ( As alias )?
    ;

specialQuery
    : queryFunction LP ( variableAttribute | variable ) RP
    ;

queryFunction
    : CountFunction
    | IsEmptyFunction
    ;

orderByClause
    : OrderBy (variableAttribute | variable) Desc?
    ;

limitClause
    : Limit INTEGER
    ;

path
    : node ( ( ( TOLEFT relationship? UND ) | ( UND relationship? UND ) | ( UND relationship? TORIGHT ) ) node )*
    ;

node
    : LP variable? ( COL nodeLabel )+ propertyConstraint? RP
    | LP variable ( COL nodeLabel )* propertyConstraint? RP
    ;

nodeLabel
    : varString
    ;

propertyConstraint
    : LB nodeOrRelationshipProperty ( COMMA nodeOrRelationshipProperty )* RB
    ;

relationship
    : LSB variable? COL relationshipLabel ( OR COL relationshipLabel )? propertyConstraint? RSB
    | LSB variable ( COL relationshipLabel ( OR COL relationshipLabel )? propertyConstraint? )? RSB
    ;

relationshipLabel
    : varString
    ;

constraint
    : ( variableAttribute | variable ) symbolOP value
    ;

alias
    : variable
    ;
    
symbolOP
    : EQ
    | NEQ
    | GTE
    | GT
    | LTE    
    | LT
    ;

logicOP
    : And
    | Or
    ;
variable
    : varString
    ;

variableAttribute
    : variable DOT variable
    ;

nodeOrRelationshipProperty
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
