from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass

from constants import OPERATORS
from tokens import Token
from variables import VariableState


class Expression(ABC):
    @abstractmethod
    def resolve(self, variables: VariableState | None = None) -> Value:
        pass


@dataclass
class Value(Expression):
    token: Token

    def resolve(self, variables: VariableState | None = None) -> Value:
        variables = variables or VariableState.default_state
        if self.token.type == 'LITERAL':
            return self.token.value
        else:
            return variables[self.token.value]


@dataclass
class BinaryOp(Expression):
    operator: function
    left: Expression
    right: Expression

    def resolve(self, variables: VariableState | None = None) -> Value:
        variables = variables or VariableState.default_state
        left = self.left.resolve(variables)
        right = self.right.resolve(variables)
        return self.operator(left, right)


@dataclass
class FunctionCall(Expression):
    function_name: str
    params: list[Expression]

    def resolve(self, variables: VariableState | None = None) -> Value:
        func = variables[self.function_name]
        resolved_params = [item.resolve(variables) for item in self.params]
        return func(*resolved_params)


def parse_expression(expr: list[Token]) -> Expression:
    if len(expr) == 1:
        token = expr[0]
        if token.type == 'LITERAL' or token.type == 'IDENTIFIER':
            return Value(expr[0])
        else:
            raise RuntimeError('Invalid token in expression')
    # Resolve parenthesis
    stack = deque([current := []])
    for token in expr:
        if token == Token('SYMBOL', '('):
            stack.append(current := [])
        elif token == Token('SYMBOL', ')'):
            inside = stack.pop()
            current = stack[-1]
            inside = parse_expression(inside)
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
            operator = OPERATORS[op]
            i = expr.index(Token('OPERATOR', op))
            left = parse_expression(expr[:i])
            right = parse_expression(expr[i + 1:])
            return BinaryOp(operator, left, right)
    raise RuntimeError('Invalid expression', expr)
