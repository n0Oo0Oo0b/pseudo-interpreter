__all__ = [
    "ExpressionVisitor",
    "StatementVisitor",
]

from abc import ABC, abstractmethod
from typing import Any

from cambridgeScript.syntax_tree.expression import *
from cambridgeScript.syntax_tree.statement import *


class ExpressionVisitor(ABC):
    def visit(self, expr: Expression) -> Any:
        return expr.accept(self)

    @abstractmethod
    def visit_binary_op(self, expr: BinaryOp) -> Any:
        pass

    @abstractmethod
    def visit_unary_op(self, expr: UnaryOp) -> Any:
        pass

    @abstractmethod
    def visit_function_call(self, expr: FunctionCall) -> Any:
        pass

    @abstractmethod
    def visit_array_index(self, expr: ArrayIndex) -> Any:
        pass

    @abstractmethod
    def visit_literal(self, expr: Literal) -> Any:
        pass

    @abstractmethod
    def visit_identifier(self, expr: Identifier) -> Any:
        pass


class StatementVisitor(ABC):
    def visit(self, stmt: Statement) -> Any:
        return stmt.accept(self)

    @abstractmethod
    def visit_proc_decl(self, stmt: ProcedureDecl) -> Any:
        pass

    @abstractmethod
    def visit_func_decl(self, stmt: FunctionDecl) -> Any:
        pass

    @abstractmethod
    def visit_if(self, stmt: IfStmt) -> Any:
        pass

    @abstractmethod
    def visit_case(self, stmt: CaseStmt) -> Any:
        pass

    @abstractmethod
    def visit_for_loop(self, stmt: ForStmt) -> Any:
        pass

    @abstractmethod
    def visit_repeat_until(self, stmt: RepeatUntilStmt) -> Any:
        pass

    @abstractmethod
    def visit_while(self, stmt: WhileStmt) -> Any:
        pass

    @abstractmethod
    def visit_variable_decl(self, stmt: VariableDecl) -> Any:
        pass

    @abstractmethod
    def visit_constant_decl(self, stmt: ConstantDecl) -> Any:
        pass

    @abstractmethod
    def visit_input(self, stmt: InputStmt) -> Any:
        pass

    @abstractmethod
    def visit_output(self, stmt: OutputStmt) -> Any:
        pass

    @abstractmethod
    def visit_return(self, stmt: ReturnStmt) -> Any:
        pass

    @abstractmethod
    def visit_f_open(self, stmt: FileOpenStmt) -> Any:
        pass

    @abstractmethod
    def visit_f_read(self, stmt: FileReadStmt) -> Any:
        pass

    @abstractmethod
    def visit_f_write(self, stmt: FileWriteStmt) -> Any:
        pass

    @abstractmethod
    def visit_f_close(self, stmt: FileCloseStmt) -> Any:
        pass

    @abstractmethod
    def visit_proc_call(self, stmt: ProcedureCallStmt) -> Any:
        pass

    @abstractmethod
    def visit_assign(self, stmt: AssignmentStmt) -> Any:
        pass

    # @abstractmethod
    # def visit_expr_stmt(self, stmt) -> Any:
    #     pass

    @abstractmethod
    def visit_program(self, stmt: Program) -> Any:
        pass
