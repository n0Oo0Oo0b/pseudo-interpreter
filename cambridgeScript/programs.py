from __future__ import annotations

from collections import namedtuple, deque
from dataclasses import dataclass, field
from typing import Any

from constants import TYPES
from tokens import Token, parse_tokens
from expressions import parse_expression
from variables import VariableState


Value = str | int | float | bool
Line = namedtuple('Line', ['operation', 'params'])


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
                case Line('DECLARE', (Token('IDENTIFIER', name), Token('IDENTIFIER', type_))):
                    variables.declare(name, TYPES[type_])
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
                    stack.append(current_frame := Block('IF', parse_expression(expr), []))
                case Token('WHILE'), *expr, Token('DO'):
                    stack.append(current_frame := Block('WHILE', parse_expression(expr), []))
                case Token('REPEAT'), :
                    stack.append(current_frame := Block('UNTIL', None, []))
                case (
                    Token('FOR'), Token('IDENTIFIER') as name,
                    Token('ASSIGN'),
                    Token('LITERAL') as a, Token('TO'), Token('LITERAL') as b,
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
                        current_frame.meta = parse_expression(rest)
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
                case Token('DECLARE'), Token('IDENTIFIER') as name, Token('SYMBOL', ':'), Token('IDENTIFIER') as type_:
                    current_frame.add_line(Line('DECLARE', (name, type_)))
                case Token('INPUT'), Token('IDENTIFIER') as name:
                    current_frame.add_line(Line('INPUT', name))
                case Token('OUTPUT'), *expr:
                    current_frame.add_line(Line('OUTPUT', parse_expression(expr)))
                case Token('IDENTIFIER') as name, Token('ASSIGN'), *expr:
                    current_frame.add_line(Line('ASSIGN', (name, parse_expression(expr))))
                case _:
                    raise RuntimeError(f'Invalid line {line}')
        return program

    def execute(self: Block, variables: VariableState | None = None) -> None:
        variables = VariableState(set_as_default=True)
        super().execute(variables)
