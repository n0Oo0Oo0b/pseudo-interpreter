__all__ = [
    "Keyword",
    "Symbol",
    "Operator",
]


import operator
from enum import StrEnum


# Reserved words
class Keyword(StrEnum):
    PROCEDURE = "PROCEDURE"
    ENDPROCEDURE = "ENDPROCEDURE"
    FUNCTION = "FUNCTION"
    RETURNS = "RETURNS"
    ENDFUNCTION = "ENDFUNCTION"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    ENDIF = "ENDIF"
    CASE_OF = "CASE OF"
    OF = "OF"
    OTHERWISE = "OTHERWISE"
    ENDCASE = "ENDCASE"
    FOR = "FOR"
    TO = "TO"
    STEP = "STEP"
    NEXT = "NEXT"
    REPEAT = "REPEAT"
    UNTIL = "UNTIL"
    WHILE = "WHILE"
    DO = "DO"
    ENDWHILE = "ENDWHILE"
    DECLARE = "DECLARE"
    CONSTANT = "CONSTANT"
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    RETURN = "RETURN"
    OPENFILE = "OPENFILE"
    READFILE = "READFILE"
    WRITEFILE = "WRITEFILE"
    CLOSEFILE = "CLOSEFILE"
    CALL = "CALL"
    ARRAY = "ARRAY"
    INTEGER = "INTEGER"
    REAL = "REAL"
    CHAR = "CHAR"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    READ = "READ"
    WRITE = "WRITE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class Symbol(StrEnum):
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRAKET = "]"
    COMMA = ","
    COLON = ":"
    ASSIGN = "<-"
    EQUAL = "="
    LESS_EQUAL = "<="
    GREAT_EQUAL = ">="
    NOT_EQUAL = "<>"
    LESS = "<"
    GREAT = ">"
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    POW = "^"


def _unary_sub(n):
    return -n


class Operator:
    OR = operator.or_
    AND = operator.and_
    NOT = operator.not_
    NOT_EQUAL = operator.ne
    EQUAL = operator.eq
    LESS_EQUAL = operator.le
    GREAT_EQUAL = operator.ge
    LESS_THAN = operator.lt
    GREATER_THAN = operator.gt
    SUB = operator.sub
    ADD = operator.add
    UNARY_SUB = _unary_sub
    MUL = operator.mul
    DIV = operator.truediv
