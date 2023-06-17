__all__ = [
    "ExpressionVisitor",
    "Expression",
    "Assignable",
    "BinaryOp",
    "UnaryOp",
    "FunctionCall",
    "ArrayIndex",
    "Literal",
    "Identifier",
]


from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Any

from cambridgeScript.parser.lexer import Token, Value


class ExpressionVisitor(ABC):
    def visit(self, expr: "Expression") -> Any:
        return expr.accept(self)

    @abstractmethod
    def visit_binary_op(self, expr: "BinaryOp") -> Any:
        pass

    @abstractmethod
    def visit_unary_op(self, expr: "UnaryOp") -> Any:
        pass

    @abstractmethod
    def visit_function_call(self, expr: "FunctionCall") -> Any:
        pass

    @abstractmethod
    def visit_array_index(self, expr: "ArrayIndex") -> Any:
        pass

    @abstractmethod
    def visit_literal(self, expr: "Literal") -> Any:
        pass

    @abstractmethod
    def visit_identifier(self, expr: "Identifier") -> Any:
        pass


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: ExpressionVisitor) -> Any:
        pass


@dataclass
class BinaryOp(Expression):
    operator: Callable[[Value, Value], Value]
    left: Expression
    right: Expression

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOp(Expression):
    operator: Callable[[Value], Value]
    operand: Expression

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class FunctionCall(Expression):
    function: Expression
    params: list[Expression]

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_function_call(self)


@dataclass
class ArrayIndex(Expression):
    array: Expression
    index: list[Expression]

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_array_index(self)


@dataclass
class Literal(Expression):
    token: Token

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_literal(self)


@dataclass
class Identifier(Expression):
    token: Token

    def accept(self, visitor: ExpressionVisitor) -> Any:
        return visitor.visit_identifier(self)


Assignable = ArrayIndex | Identifier
