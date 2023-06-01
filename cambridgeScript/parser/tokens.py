import re
from dataclasses import dataclass

from ..constants import Keyword, Symbol

Value = str | int | float | bool


@dataclass(frozen=True)
class Token:
    line: int | None
    column: int | None

    @property
    def location(self) -> str:
        return f"Line {self.line} Column {self.column}"


TokenComparable = Token | Keyword | Symbol | str | Value


@dataclass(frozen=True)
class KeywordToken(Token):
    keyword: Keyword

    def __eq__(self, other):
        if isinstance(other, Keyword):
            return self.keyword == other
        return super().__eq__(other)


@dataclass(frozen=True)
class SymbolToken(Token):
    symbol: Symbol

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.symbol == other
        return super().__eq__(other)


@dataclass(frozen=True)
class LiteralToken(Token):
    value: Value

    @property
    def type(self):
        return type(self.value)


@dataclass(frozen=True)
class IdentifierToken(Token):
    value: str

    def __eq__(self, other):
        return self.value == other or super().__eq__(other)


# Regex patterns for tokens
_TOKENS = [
    ("IGNORE", r"/\*.*\*/|(?://|#).*$|[ \t]+"),
    ("NEWLINE", r"\n"),
    ("KEYWORD", "|".join(Keyword)),
    ("LITERAL", r'-?[0-9]+(?:\.[0-9]+)?|".*?"'),
    ("SYMBOL", "|".join("\\" + s for s in Symbol)),
    ("IDENTIFIER", r"[A-Za-z]+"),
    ("INVALID", r"."),
]
_TOKEN_REGEX = "|".join(f"(?P<{name}>{regex})" for name, regex in _TOKENS)


def parse_literal(literal: str) -> Value:
    if literal.startswith('"') and literal.endswith('"'):
        return literal[1:-1]
    try:
        if "." in literal:
            return float(literal)
        else:
            return int(literal)
    except ValueError:
        raise ValueError("Invalid literal")


def parse_token(token_string: str, token_type: str, **token_kwargs) -> Token:
    if token_type == "KEYWORD":
        return KeywordToken(symbol=Keyword(token_string), **token_kwargs)
    elif token_type == "IDENTIFIER":
        return IdentifierToken(value=token_string, **token_kwargs)
    elif token_type == "SYMBOL":
        return SymbolToken(symbol=Symbol(token_string), **token_kwargs)
    else:
        value = parse_literal(token_string)
        return LiteralToken(value=value, **token_kwargs)


def parse_tokens(code: str) -> list[Token]:
    """
    Parse tokens from a program.
    :param code: program to parse.
    :type code: str
    :return: a list containing the tokens in the program.
    :rtype: list[Token]
    """
    code += "\n"
    res: list[Token] = []
    line_number: int = 0
    line_start: int = 0
    for match in re.finditer(_TOKEN_REGEX, code, re.M):
        token_type = match.lastgroup
        if token_type is None:
            raise ValueError("An error occured")
        token_value = str(match.group())
        token_start = match.start()
        if token_type == "IGNORE":
            continue
        elif token_type == "NEWLINE":
            line_number += 1
            line_start = token_start
            continue
        elif token_type == "INVALID":
            raise ValueError(
                f"Invalid token at line {line_number}, column {token_start - line_start}"
            )
        try:
            token = parse_token(
                token_value,
                token_type,
                line=line_number,
                column=token_start - line_start,
            )
        except ValueError:
            print(f"Invalid literal {token_value}")
            raise
        res.append(token)
    return res
