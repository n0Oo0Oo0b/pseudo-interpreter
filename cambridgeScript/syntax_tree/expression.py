from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Callable, Any

from ..parser.tokens import Token

Value = str | int | float | bool
T = TypeVar('T')


class ExpressionVisitor(ABC):
    def visit(self, expr: "Expression") -> T:
        return expr.accept(self)

    @abstractmethod
    def visit_primary(self, expr: "Primary") -> T:
        pass

    @abstractmethod
    def visit_unary_op(self, expr: "UnaryOp") -> T:
        pass

    @abstractmethod
    def visit_binary_op(self, expr: "BinaryOp") -> T:
        pass

    @abstractmethod
    def visit_function_call(self, expr: "FunctionCall") -> T:
        pass

    @abstractmethod
    def visit_assignment(self, expr: "Assignment") -> T:
        pass


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: ExpressionVisitor) -> Any:
        pass


@dataclass
class Primary(Expression):
    token: Token

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_primary(self)


@dataclass
class UnaryOp(Expression):
    operator: Callable[[Value], Value]
    operand: Expression

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class BinaryOp(Expression):
    operator: Callable[[Value, Value], Value]
    left: Expression
    right: Expression

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class FunctionCall(Expression):
    function_name: str
    params: list[Expression]

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_function_call(self)


@dataclass
class Assignment(Expression):
    target: Token
    value: Expression

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_assignment(self)
