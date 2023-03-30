from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

from .tokens import Token
from ..visitors import ExpressionVisitor, StatementVisitor

Value = str | int | float | bool


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


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor: StatementVisitor) -> Any:
        pass


@dataclass
class ExpressionStmt(Statement):
    expr: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_expr(self)


@dataclass
class InputStmt(Statement):
    variable: Token

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_input(self)


@dataclass
class OutputStmt(Statement):
    expr: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_output(self)
