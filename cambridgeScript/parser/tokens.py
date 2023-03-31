from dataclasses import dataclass
import re

from ..constants import KEYWORDS, TOKEN_REGEX


Value = str | int | float | bool


@dataclass(frozen=True)
class Token:
    type: str
    value: Value | str | None
    line: int | None = None
    column: int | None = None
    meta: str | None = None

    def __eq__(self, other):
        if isinstance(other, str):
            return self.type == other
        elif isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        else:
            return False


def parse_literal(literal: str) -> tuple[Value, str]:
    """
    Parse a literal value.
    :param literal: literal to parse
    :type literal: str
    :return: a tuple containing the value of the literal and the datatype as a string
    :rtype: tuple[Value, str]
    """
    if literal.startswith('"') and literal.endswith('"'):
        value = (
            literal[1:-1].replace(r"\"", '"').replace(r"\n", "\n").replace(r"\\", "\\")
        )
        return value, "STRING"
    elif "." in literal:
        return float(literal), "REAL"
    else:
        return int(literal), "INTEGER"


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
        if token_type == "IGNORE" or token_type == "COMMENT":
            continue
        elif token_type == "IDENTIFIER" and token_value in KEYWORDS:
            token = Token(token_value, None, line_number, token_start - line_start)
        elif token_type == "LITERAL":
            token_value, literal_type = parse_literal(token_value)
            token = Token(
                token_type,
                token_value,
                line_number,
                token_start - line_start,
                literal_type,
            )
        else:
            if token_type == "NEWLINE":
                line_number += 1
                line_start = token_start
            token = Token(
                token_type, token_value, line_number, token_start - line_start
            )
        res.append(token)
    return res
