from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

from cambridgeScript.parser.tokens import Token
from cambridgeScript.visitors import ExpressionVisitor
from cambridgeScript.interpreter.variables import VariableState


Value = str | int | float | bool


class Expression(ABC):
    @abstractmethod
    def resolve(self, variables: VariableState | None = None) -> Value:
        pass

    @abstractmethod
    def accept(self, visitor: ExpressionVisitor) -> Any:
        pass


@dataclass
class Primary(Expression):
    token: Token

    def resolve(self, variables: VariableState | None = None) -> Value:
        variables = variables or VariableState.default_state
        if self.token.type == 'LITERAL':
            return self.token.value
        else:
            return variables[self.token.value]

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_value(self)


@dataclass
class UnaryOp(Expression):
    operator: Callable[[Value], Value]
    operand: Expression

    def resolve(self, variables: VariableState | None = None) -> Value:
        variables = variables or VariableState.default_state
        return self.operator(self.operand.resolve(variables))

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class BinaryOp(Expression):
    operator: Callable
    left: Expression
    right: Expression

    def resolve(self, variables: VariableState | None = None) -> Primary:
        variables = variables or VariableState.default_state
        left = self.left.resolve(variables)
        right = self.right.resolve(variables)
        return self.operator(left, right)

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class FunctionCall(Expression):
    function_name: str
    params: list[Expression]

    def resolve(self, variables: VariableState | None = None) -> Primary:
        func = variables[self.function_name]
        resolved_params = [item.resolve(variables) for item in self.params]
        return func(*resolved_params)

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_function_call(self)
