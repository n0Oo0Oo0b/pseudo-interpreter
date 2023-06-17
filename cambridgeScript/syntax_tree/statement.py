__all__ = [
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
    # "ExprStmt",
    "Program",
]

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cambridgeScript.syntax_tree.visitors import StatementVisitor

from cambridgeScript.parser.lexer import IdentifierToken, LiteralToken, KeywordToken
from cambridgeScript.syntax_tree.expression import Expression, Assignable
from cambridgeScript.syntax_tree.types import Type


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor: "StatementVisitor") -> Any:
        pass


@dataclass
class ProcedureDecl(Statement):
    name: IdentifierToken
    params: list[tuple[IdentifierToken, "Type"]] | None
    body: list[Statement]

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_proc_decl(self)


@dataclass
class FunctionDecl(Statement):
    name: IdentifierToken
    params: list[tuple[IdentifierToken, "Type"]] | None
    return_type: "Type"
    body: list[Statement]

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_func_decl(self)


@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: list[Statement]
    else_branch: list[Statement] | None

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_if(self)


@dataclass
class CaseStmt(Statement):
    expr: Expression
    cases: list[tuple[IdentifierToken | LiteralToken, Statement]]
    otherwise: Statement | None

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_case(self)


@dataclass
class ForStmt(Statement):
    variable: Assignable
    start: Expression
    end: Expression
    step: Expression | None
    body: list[Statement]

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_for_loop(self)


@dataclass
class RepeatUntilStmt(Statement):
    body: list[Statement]
    condition: Expression

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_repeat_until(self)


@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: list[Statement]

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_while(self)


@dataclass
class VariableDecl(Statement):
    name: IdentifierToken
    type: "Type"

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_variable_decl(self)


@dataclass
class ConstantDecl(Statement):
    name: IdentifierToken
    value: LiteralToken

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_constant_decl(self)


@dataclass
class InputStmt(Statement):
    variable: Assignable

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_input(self)


@dataclass
class OutputStmt(Statement):
    values: list[Expression]

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_output(self)


@dataclass
class ReturnStmt(Statement):
    value: Expression

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_return(self)


@dataclass
class FileOpenStmt(Statement):
    file: LiteralToken
    mode: KeywordToken

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_f_open(self)


@dataclass
class FileReadStmt(Statement):
    file: LiteralToken
    target: Assignable

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_f_read(self)


@dataclass
class FileWriteStmt(Statement):
    file: LiteralToken
    value: Expression

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_f_write(self)


@dataclass
class FileCloseStmt(Statement):
    file: LiteralToken

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_f_close(self)


@dataclass
class ProcedureCallStmt(Statement):
    name: IdentifierToken
    args: list[Expression] | None

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_proc_call(self)


@dataclass
class AssignmentStmt(Statement):
    target: Assignable
    value: Expression

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_assign(self)


# @dataclass
# class ExprStmt(Statement):
#     expr: Expression
#
#     def accept(self, visitor: "StatementVisitor") -> Any:
#         return visitor.visit_expr_stmt(self)


@dataclass
class Program(Statement):
    statements: list[Statement]

    def accept(self, visitor: "StatementVisitor") -> Any:
        return visitor.visit_program(self)
