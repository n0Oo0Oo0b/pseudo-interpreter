from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.syntax_tree import Value, BinaryOp, FunctionCall


class ExpressionVisitor(ABC):
    @abstractmethod
    def visit_value(self, expr: 'Value'):
        pass

    @abstractmethod
    def visit_binary_op(self, expr: 'BinaryOp'):
        pass

    # @abstractmethod
    # def visit_unary_op(self, expr: 'UnaryOp'):
    #     pass

    @abstractmethod
    def visit_function_call(self, expr: 'FunctionCall'):
        pass
