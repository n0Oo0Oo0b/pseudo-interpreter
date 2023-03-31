from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from .interpreter.variables import VariableState

if TYPE_CHECKING:
    from .parser.syntax_tree import (
        Expression,
        Primary,
        UnaryOp,
        BinaryOp,
        FunctionCall,
        Assignment,
        Statement,
        InputStmt,
        OutputStmt,
        ExpressionStmt,
        DeclareStmt,
    )


Value = str | int | float | bool


class ExpressionVisitor(ABC):
    def visit(self, expr: "Expression") -> Any:
        return expr.accept(self)

    @abstractmethod
    def visit_primary(self, expr: "Primary") -> Any:
        pass

    @abstractmethod
    def visit_unary_op(self, expr: "UnaryOp") -> Any:
        pass

    @abstractmethod
    def visit_binary_op(self, expr: "BinaryOp") -> Any:
        pass

    @abstractmethod
    def visit_function_call(self, expr: "FunctionCall") -> Any:
        pass

    @abstractmethod
    def visit_assignment(self, expr: "Assignment") -> Any:
        pass


class ExpressionResolver(ExpressionVisitor):
    def __init__(self, variables: VariableState):
        self._variables = variables

    def visit_primary(self, expr: "Primary") -> Value:
        if expr.token.type == "LITERAL":
            return expr.token.value
        else:
            return self._variables[expr.token.value]

    def visit_unary_op(self, expr: "UnaryOp") -> Value:
        operand = self.visit(expr.operand)
        return expr.operator(operand)

    def visit_binary_op(self, expr: "BinaryOp") -> Value:
        left = self.visit(expr.left)
        right = self.visit(expr.right)
        return expr.operator(left, right)

    def visit_function_call(self, expr: "FunctionCall") -> Value:
        pass

    def visit_assignment(self, expr: "Assignment") -> Any:
        raise NotImplementedError


class StatementVisitor(ABC):
    def visit(self, stmt: Statement) -> Any:
        return stmt.accept(self)

    @abstractmethod
    def visit_expr(self, stmt: "ExpressionStmt") -> Any:
        pass

    @abstractmethod
    def visit_input(self, stmt: "InputStmt") -> Any:
        pass

    @abstractmethod
    def visit_output(self, stmt: "OutputStmt") -> Any:
        pass

    @abstractmethod
    def visit_declare(self, stmt: "DeclareStmt") -> Any:
        pass
