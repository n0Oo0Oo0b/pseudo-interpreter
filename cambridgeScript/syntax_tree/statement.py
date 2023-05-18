from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, TypeVar

from .expression import Expression
from ..parser.tokens import Token

T = TypeVar('T')


class StatementVisitor(ABC):
    def visit(self, stmt: "Statement") -> T:
        return stmt.accept(self)

    @abstractmethod
    def visit_expr(self, stmt: "ExpressionStmt") -> T:
        pass

    @abstractmethod
    def visit_input(self, stmt: "InputStmt") -> T:
        pass

    @abstractmethod
    def visit_output(self, stmt: "OutputStmt") -> T:
        pass

    @abstractmethod
    def visit_declare(self, stmt: "DeclareStmt") -> T:
        pass

    @abstractmethod
    def visit_if(self, stmt: "IfStmt") -> T:
        pass

    @abstractmethod
    def visit_while(self, stmt: "WhileStmt") -> T:
        pass


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


@dataclass
class DeclareStmt(Statement):
    variable: Token
    type_: type
    value: Any | None = None

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_declare(self)


@dataclass
class IfStmt(Statement):
    condition: Expression
    true_branch: list[Statement]
    false_branch: list[Statement] = field(default_factory=list)

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_if(self)


@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: list[Statement]

    def accept(self, visitor: StatementVisitor) -> Any:
        return visitor.visit_while(self)
