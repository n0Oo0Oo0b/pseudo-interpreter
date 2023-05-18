import re
from dataclasses import dataclass

from ..constants import Keywords, TOKEN_REGEX, Symbols

Value = str | int | float | bool


@dataclass(frozen=True)
class Token:
    line: int | None
    column: int | None

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return super().__eq__(other)


@dataclass(frozen=True)
class KeywordToken(Token):
    value: Keywords

    def __eq__(self, other):
        if isinstance(other, Keywords):
            return self.value == other
        return super().__eq__(other)


@dataclass(frozen=True)
class SymbolToken(Token):
    value: Symbols

    def __eq__(self, other):
        if isinstance(other, Symbols):
            return self.value == other
        return super().__eq__(other)


@dataclass(frozen=True)
class Literal(Token):
    value: Value

    @property
    def type(self):
        return type(self.value)


@dataclass(frozen=True)
class Identifier(Token):
    value: str

    def __eq__(self, other):
        return self.value == other


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
    if token_type == "IDENTIFIER":
        try:
            return KeywordToken(value=Keywords(token_string), **token_kwargs)
        except ValueError:
            return Identifier(value=token_string, **token_kwargs)
    elif token_type == "SYMBOL":
        return SymbolToken(value=Symbols(token_string), **token_kwargs)
    elif token_type == "LITERAL":
        value = parse_literal(token_string)
        return Literal(value=value, **token_kwargs)


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
    for match in re.finditer(TOKEN_REGEX, code, re.M):
        token_type = match.lastgroup
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
