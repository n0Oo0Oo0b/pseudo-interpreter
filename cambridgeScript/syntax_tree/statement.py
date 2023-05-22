__all__ = [
    "StatementVisitor",
    "Statement",
    "ProcedureDecl",
    "FunctionDecl",
    "IfStmt",
    "CaseStmt",
    "ForStmt",
    "RepeatUntilStmt",
    "WhileStmt",
    "VariableDecl",
    "ConstantDecl",
    "InputStmt",
    "OutputStmt",
    "ReturnStmt",
    "FileOpenStmt",
    "FileReadStmt",
    "FileWriteStmt",
    "FileCloseStmt",
    "ProcedureCallStmt",
    "AssignmentStmt",
    "ExprStmt",
]

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar

from .expression import Expression
from ..parser.tokens import Token

T = TypeVar("T")


class StatementVisitor(ABC):
    def visit(self, stmt: "Statement") -> T:
        return stmt.accept(self)

    @abstractmethod
    def visit_proc_decl(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_func_decl(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_if(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_case(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_for_loop(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_repeat_until(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_while(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_variable_decl(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_constant_decl(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_input(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_output(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_return(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_f_open(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_f_read(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_f_write(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_f_close(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_proc_call(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_assign(self, stmt) -> T:
        pass

    @abstractmethod
    def visit_expr_stmt(self, stmt) -> T:
        pass


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor: StatementVisitor) -> Any:
        pass


@dataclass
class ProcedureDecl(Statement):
    name: Token
    params: list[Token]
    body: list[Statement]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_proc_decl(self)


class FunctionDecl(Statement):
    name: Token
    params: list[Token]
    return_type: Token
    body: list[Statement]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_func_decl(self)


@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: list[Statement]
    else_branch: list[Statement]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_if(self)


@dataclass
class CaseStmt(Statement):
    expr: Expression
    cases: list[Token]
    body: list[Statement]
    otherwise: Statement | None = None

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_case(self)


@dataclass
class ForStmt(Statement):
    variable: Token
    start: Expression
    end: Expression
    step: Expression
    body: list[Statement]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_for_loop(self)


@dataclass
class RepeatUntilStmt(Statement):
    body: list[Statement]
    condition: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_repeat_until(self)


@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: list[Statement]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_while(self)


@dataclass
class VariableDecl(Statement):
    name: Token
    type: Token

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_variable_decl(self)


@dataclass
class ConstantDecl(Statement):
    name: Token
    value: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_constant_decl(self)


@dataclass
class InputStmt(Statement):
    variable: Token

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_input(self)


@dataclass
class OutputStmt(Statement):
    values: list[Expression]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_output(self)


@dataclass
class ReturnStmt(Statement):
    value: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_return(self)


@dataclass
class FileOpenStmt(Statement):
    file: Token
    mode: Token

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_f_open(self)


@dataclass
class FileReadStmt(Statement):
    file: Token
    variable: Token

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_f_read(self)


@dataclass
class FileWriteStmt(Statement):
    file: Token
    value: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_f_write(self)


@dataclass
class FileCloseStmt(Statement):
    file: Token

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_f_close(self)


@dataclass
class ProcedureCallStmt(Statement):
    name: Token
    args: list[Expression]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_proc_call(self)


@dataclass
class AssignmentStmt(Statement):
    target: Expression
    value: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_assign(self)


@dataclass
class ExprStmt(Statement):
    expr: Expression

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_expr_stmt(self)
