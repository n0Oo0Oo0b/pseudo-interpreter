from enum import Enum
import operator


# Reserved words
KEYWORDS = {
    # General command words
    'DECLARE', 'INPUT', 'OUTPUT',
    # Selection
    'IF', 'THEN', 'ELSE', 'DO', 'ENDIF',
    'CASE', 'OF', 'OTHERWISE', 'ENDCASE',
    # Iteration
    'FOR', 'TO', 'DO', 'NEXT',  # Count controlled
    'WHILE', 'DO', 'ENDWHILE',  # Conditional (pre-condition)
    'REPEAT', 'UNTIL',  # Conditional (post-condition)
}


# Variable types
TYPES = {
    'INTEGER': int,
    'REAL': float,
    'CHAR': str,
    'STRING': str,
    'BOOLEAN': bool,
}


# Regex patterns for tokens
TOKENS = [
    ('COMMENT', r'/\*.*\*/|(?://|#).*$'),
    ('NEWLINE', r'\n'),
    ('LITERAL', r'[0-9]+(?:\.[0-9]+)?|".*?(?<=[^\\])(?:\\\\)*+"'),
    ('ASSIGN', r'<-'),
    ('OPERATOR', r'[=<>+\-*/^]|<>|<=|>='),
    ('SYMBOL', r'[():]'),
    ('IDENTIFIER', r'[A-Za-z]+'),
    ('IGNORE', r'[ \t]+'),
    ('INVALID', r'.'),
]
TOKEN_REGEX = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKENS)


OPERATORS = {
    'OR': lambda a, b: (bool(a) or bool(b)),
    'AND': lambda a, b: (bool(a) and bool(b)),
    '=': operator.eq,
    '<>': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '^': operator.pow,
    '*': operator.mul,
    '/': operator.truediv,
    '+': operator.add,
    '-': operator.sub,
}
