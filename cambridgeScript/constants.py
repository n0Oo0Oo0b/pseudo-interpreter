from enum import Enum, StrEnum


# Reserved words
class Keywords(StrEnum):
    PROCEDURE = "PROCEDURE"
    ENDPROCEDURE = "ENDPROCEDURE"
    FUNCTION = "FUNCTION"
    RETURNS = "RETURNS"
    ENDFUNCTION = "ENDFUNCTION"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    ENDIF = "ENDIF"
    CASE = "CASE"
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


class Symbols(Enum):
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRAKET = "]"
    COLON = ":"
    ASSIGN = "<-"
    EQUAL = "="
    NOT_EQUAL = "<>"
    LESS = "<"
    LESS_EQUAL = "<="
    GREAT = ">"
    GREAT_EQUAL = ">="
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    POW = "^"
    NEWLINE = "\n"


# Variable types
class TYPES(Enum):
    INTEGER = int
    REAL = float
    CHAR = str
    STRING = str
    BOOLEAN = bool


# Regex patterns for tokens
_TOKENS = [
    ("IGNORE", r"/\*.*\*/|(?://|#).*$|[ \t]+"),
    ("NEWLINE", r"\n"),
    ("LITERAL", r'[0-9]+(?:\.[0-9]+)?|".*?(?<=[^\\])(?:\\\\)*+"'),
    ("SYMBOL", r"<-|<>|<=|>=|[=<>+\-*/^():]"),
    ("IDENTIFIER", r"[A-Za-z]+"),
    ("INVALID", r"."),
]
TOKEN_REGEX = "|".join(f"(?P<{name}>{regex})" for name, regex in _TOKENS)
