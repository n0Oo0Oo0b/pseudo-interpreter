__all__ = [
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
from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cambridgeScript.syntax_tree.visitors import ExpressionVisitor

from cambridgeScript.parser.lexer import Token, Value


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: "ExpressionVisitor") -> Any:
        pass


@dataclass
class BinaryOp(Expression):
    operator: Callable[[Value, Value], Value]
    left: Expression
    right: Expression

    def accept(self, visitor: "ExpressionVisitor") -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOp(Expression):
    operator: Callable[[Value], Value]
    operand: Expression

    def accept(self, visitor: "ExpressionVisitor") -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class FunctionCall(Expression):
    function: Expression
    params: list[Expression]

    def accept(self, visitor: "ExpressionVisitor") -> Any:
        return visitor.visit_function_call(self)


@dataclass
class ArrayIndex(Expression):
    array: Expression
    index: list[Expression]

    def accept(self, visitor: "ExpressionVisitor") -> Any:
        return visitor.visit_array_index(self)


@dataclass
class Literal(Expression):
    token: Token

    def accept(self, visitor: "ExpressionVisitor") -> Any:
        return visitor.visit_literal(self)


@dataclass
class Identifier(Expression):
    token: Token

    def accept(self, visitor: "ExpressionVisitor") -> Any:
        return visitor.visit_identifier(self)


Assignable = ArrayIndex | Identifier
