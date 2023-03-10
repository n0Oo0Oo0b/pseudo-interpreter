from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from parser.syntax_tree import Primary, UnaryOp, BinaryOp, FunctionCall


Value = str | int | float | bool


class ExpressionVisitor(ABC):
    @abstractmethod
    def visit_primary(self, expr: 'Primary') -> Any:
        pass

    @abstractmethod
    def visit_unary_op(self, expr: 'UnaryOp') -> Any:
        pass

    @abstractmethod
    def visit_binary_op(self, expr: 'BinaryOp') -> Any:
        pass

    @abstractmethod
    def visit_function_call(self, expr: 'FunctionCall') -> Any:
        pass


class ExpressionResolver(ExpressionVisitor):
    def visit_primary(self, expr: 'Primary') -> Value:
        pass

    def visit_unary_op(self, expr: 'UnaryOp') -> Value:
        pass

    def visit_binary_op(self, expr: 'BinaryOp') -> Value:
        pass

    def visit_function_call(self, expr: 'FunctionCall') -> Value:
        pass
