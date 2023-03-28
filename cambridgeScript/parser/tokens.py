from dataclasses import dataclass
import re

from cambridgeScript.constants import KEYWORDS, TOKEN_REGEX


Value = str | int | float | bool


@dataclass(frozen=True)
class Token:
    type: str
    value: Value | str | None
    line: int
    column: int
    meta: str | None = None

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value


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
            if token_value.startswith('"') and token_value.endswith('"'):
                token_value = (
                    token_value[1:-1]
                    .replace(r"\"", '"')
                    .replace(r"\n", "\n")
                    .replace(r"\\", "\\")
                )
                literal_type = "STRING"
            elif "." in token_value:
                token_value = float(token_value)
                literal_type = "REAL"
            else:
                token_value = int(token_value)
                literal_type = "INTEGER"
            token = Token(token_type, token_value, line_number, token_start - line_start, literal_type)
        else:
            if token_type == "NEWLINE":
                line_number += 1
                line_start = token_start
            token = Token(token_type, token_value, line_number, token_start - line_start)
        res.append(token)
    return res
