from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass

from constants import OPERATORS
from tokens import Token
from variables import VariableState


class Expression(ABC):
    @classmethod
    def parse(cls, expr: list[Token]) -> Expression | Token:
        if len(expr) == 1:
            return expr[0]
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
                operator = OPERATORS[op]
                i = expr.index(Token('OPERATOR', op))
                left = Expression.parse(expr[:i])
                right = Expression.parse(expr[i + 1:])
                return BinaryOp(operator, left, right)
        raise RuntimeError('Invalid expression', expr)

    @abstractmethod
    def resolve(self, variables: VariableState | None = None) -> Value:
        pass


@dataclass
class BinaryOp(Expression):
    operator: function
    left: Expression | Token
    right: Expression | Token

    def resolve(self, variables: VariableState | None = None) -> Value:
        variables = variables or VariableState.default_state
        left = self.left.resolve(variables)
        right = self.right.resolve(variables)
        return self.operator(left, right)
