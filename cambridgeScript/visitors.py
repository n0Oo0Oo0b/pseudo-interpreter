from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from interpreter.variables import VariableState

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
    def __init__(self, variables: VariableState):
        self._variables = variables

    def visit_primary(self, expr: 'Primary') -> Value:
        if expr.token.type == 'LITERAL':
            return expr.token.value
        else:
            return self._variables[expr.token.value]

    def visit_unary_op(self, expr: 'UnaryOp') -> Value:
        operand = expr.operand.accept(self)
        return expr.operator(operand)

    def visit_binary_op(self, expr: 'BinaryOp') -> Value:
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        return expr.operator(left, right)

    def visit_function_call(self, expr: 'FunctionCall') -> Value:
        pass
