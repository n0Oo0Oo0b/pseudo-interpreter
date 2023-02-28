from __future__ import annotations

from collections import namedtuple, deque, ChainMap
from dataclasses import dataclass, field
import re
from typing import Any

from constants import KEYWORDS, TOKEN_REGEX, OPERATORS


Value = str | int | float | bool
Line = namedtuple('Line', ['operation', 'params'])


class VariableState(ChainMap):
    default_state = None

    def __init__(self, set_as_default: bool = False) -> None:
        super().__init__()
        if set_as_default:
            VariableState.default_state = self

    def __getitem__(self, key) -> Value:
        if key not in self:
            raise RuntimeError(f'{key} not defined')
        return super().__getitem__(key)

    def get(self, key) -> Value | None:
        if key not in self:
            return None
        return self[key]

    def __setitem__(self, key: str, value: Value) -> None:
        if key not in self:
            raise RuntimeError(f'{key} not defined')
        super().__setitem__(key, value)

    def declare(self, key: str, type_: type, value: Value | None = None) -> None:
        super().__setitem__(key, type_(value) if value else type_())


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


@dataclass
class Expression:
    operator: function
    left: Expression | Token
    right: Expression | Token

    @classmethod
    def parse(cls, expr: list[Token]) -> Expression | Token:
        if len(expr) > 1:
            return cls(expr)
        else:
            return expr[0]

    def resolve(self, variables: VariableState | None = None) -> Value:
        variables = variables or VariableState.default_state
        left = self.left.resolve(variables)
        right = self.right.resolve(variables)
        return self.operator(left, right)

    def __init__(self, expr: list[Token]) -> None:
        # Resolve parenthesis
        stack = deque([current := []])
        for token in expr:
            if token == Token('SYMBOL', '('):
                stack.append(current := [])
            elif token == Token('SYMBOL', ')'):
                inside = stack.pop()
                current = stack[-1]
                inside = Expression.parse(inside)
                current.append(inside)
            else:
                current.append(token)
        # Resolve operations
        expr = stack[0]
        for op in [  # Lower precedence goes first
            'OR', 'AND',
            '=', '<>', '<', '>', '<=', '>=',
            '+', '-', '*', '/', '^',
        ]:
            if Token('OPERATOR', op) in expr:
                i = expr.index(Token('OPERATOR', op))
                self.operator = OPERATORS[op]
                self.left = Expression.parse(expr[:i])
                self.right = Expression.parse(expr[i + 1:])
                return
        raise RuntimeError('Invalid expression', expr)


@dataclass
class Block:
    type: str
    meta: Any
    content: list[Line | Block] = field(default_factory=list)

    def add_line(self, line: Line | Block) -> None:
        self.content.append(line)

    def execute(self: Block, variables: VariableState | None = None) -> None:
        variables = variables or VariableState.default_state
        for line in self.content:
            match line:
                case Line('DECLARE', Token('IDENTIFIER', name)):
                    variables.declare(name, int)
                case Line('ASSIGN', (name, expr)):
                    variables[name.value] = expr.resolve()
                case Line('INPUT', name):
                    if name not in variables:
                        raise RuntimeError(f'{name.value} is not defined!')
                    variables[name.value] = int(input())
                case Line('OUTPUT', expr):
                    print(expr.resolve())
                case Block('IF', expr) as block:
                    if expr.resolve():
                        block.execute()
                case Block('WHILE', expr) as block:
                    while expr.resolve():
                        block.execute()
                case Block('UNTIL', expr) as block:
                    while True:
                        block.execute()
                        if expr.resolve():
                            break
                case Block('FOR', (Token('IDENTIFIER', name), a, b)) as block:
                    variables.declare(name, int)
                    for n in range(a.resolve(), b.resolve() + 1):
                        variables[name] = n
                        block.execute()


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


class Program(Block):
    def __init__(self):
        super().__init__('MAIN', None, [])

    @classmethod
    def from_code(cls, code: str) -> cls:
        """
        Parses blocks of a program into a Frame object.
        :param code: Program to parse.
        :type code: str
        :return: Frame containing the parsed code
        :rtype: Block
        """
        # Split into lines
        lines: list[list[Token]] = []
        current_line: list[Token] = []
        for token in parse_tokens(code):
            if token.type == 'NEWLINE':
                lines.append(current_line)
                current_line = []
            else:
                current_line.append(token)
        # Parse each line
        program = cls()
        current_frame = program
        stack: deque[Block] = deque([program])
        for line in lines:
            if not line:
                continue
            match line:
                # Start block
                case Token('IF'), *expr, Token('THEN'):
                    stack.append(current_frame := Block('IF', Expression.parse(expr), []))
                case Token('WHILE'), *expr, Token('DO'):
                    stack.append(current_frame := Block('WHILE', Expression.parse(expr), []))
                case Token('REPEAT'), :
                    stack.append(current_frame := Block('UNTIL', None, []))
                case (
                    Token('FOR'), Token('IDENTIFIER') as name,
                    Token('ASSIGN'),
                    Token('VALUE') as a, Token('TO'), Token('VALUE') as b,
                    Token('DO'),
                ):
                    stack.append(current_frame := Block('FOR', (name, a, b), []))
                case Token('CASE'), Token('OF'), *_:
                    raise NotImplementedError("Case statements are not supported yet")
                # End block
                case Token('ENDIF' | 'ENDWHILE' | 'UNTIL' | 'NEXT' as end_type), *rest:
                    block_type = stack[-1].type
                    # Make sure block end matches block start
                    if (block_type, end_type) not in [
                        ('IF', 'ENDIF'),
                        ('WHILE', 'ENDWHILE'),
                        ('UNTIL', 'UNTIL'),
                        ('FOR', 'NEXT')
                    ]:
                        raise RuntimeError(f'Unexpected token {end_type}')
                    # Block-specific details
                    if block_type == 'UNTIL':
                        current_frame.meta = Expression.parse(rest)
                    elif block_type == 'FOR':
                        if len(rest) > 1:
                            raise RuntimeError('Invalid NEXT')
                        if rest[0] != stack[-1].meta[0]:
                            raise RuntimeError('Incorrect NEXT variable')
                    # End block
                    frame = stack.pop()
                    current_frame = stack[-1]
                    current_frame.add_line(frame)
                # Not a block
                case Token('DECLARE'), Token('IDENTIFIER') as name:
                    current_frame.add_line(Line('DECLARE', name))
                case Token('INPUT'), Token('IDENTIFIER') as name:
                    current_frame.add_line(Line('INPUT', name))
                case Token('OUTPUT'), *expr:
                    current_frame.add_line(Line('OUTPUT', Expression.parse(expr)))
                case Token('IDENTIFIER') as name, Token('ASSIGN'), *expr:
                    current_frame.add_line(Line('ASSIGN', (name, Expression.parse(expr))))
                case _:
                    raise RuntimeError(f'Invalid line {line}')
        return program

    def execute(self: Block, variables: VariableState | None = None) -> None:
        variables = VariableState(set_as_default=True)
        super().execute(variables)
