from dataclasses import dataclass
import re

from cambridgeScript.constants import KEYWORDS, TOKEN_REGEX


Value = str | int | float | bool


@dataclass
class Token:
    type: str
    value: Value | str | None
    meta: str | None = None


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
    for match in re.finditer(TOKEN_REGEX, code, re.M):
        token_type = match.lastgroup
        token_value = str(match.group())
        if token_type == "IGNORE" or token_type == "COMMENT":
            continue
        elif token_type == "IDENTIFIER" and token_value in KEYWORDS:
            token = Token(token_value, None)
        elif token_type == "LITERAL":
            if token_value.startswith('"') and token_value.endswith('"'):
                token_value = (
                    token_value[1:-1]
                    .replace(r"\"", '"')
                    .replace(r"\n", "\n")
                    .replace(r"\\", "\\")
                )
                token = Token(token_type, token_value, "STRING")
            elif "." in token_value:
                token = Token(token_type, float(token_value), "REAL")
            else:
                token = Token(token_type, int(token_value), "INTEGER")
        else:
            token = Token(token_type, token_value)
        res.append(token)
    return res
