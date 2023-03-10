from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

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
