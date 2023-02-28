from __future__ import annotations

from dataclasses import dataclass
import re

from constants import KEYWORDS, TOKEN_REGEX
from variables import VariableState


Value = str | int | float | bool


@dataclass
class Token:
    type: str
    value: Value | str | None

    def resolve(self, variables: VariableState | None = None) -> Value:
        variables = variables or VariableState.default_state
        if self.type == 'VALUE':
            if '.' in self.value:
                return float(self.value)
            else:
                return int(self.value)
        elif self.type == 'IDENTIFIER':
            return variables[self.value]
        else:
            raise RuntimeError(f'Cannot resolve value of token {self}')


def parse_tokens(code: str) -> list[Token]:
    """
    Parse tokens from a program.
    :param code: program to parse.
    :type code: str
    :return: a list containing the tokens in the program.
    :rtype: list[Token]
    """
    code += '\n'
    res: list[Token] = []
    for match in re.finditer(TOKEN_REGEX, code, re.M):
        if match.lastgroup == 'IGNORE' or match.lastgroup == 'COMMENT':
            continue
        if match.lastgroup == 'IDENTIFIER' and match.group() in KEYWORDS:
            token = Token(str(match.group()), None)
        else:
            token = Token(match.lastgroup, str(match.group()))
        res.append(token)
    return res
