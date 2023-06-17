from dataclasses import dataclass

from cambridgeScript.parser.lexer import Value
from cambridgeScript.syntax_tree import FunctionDecl, ProcedureDecl


@dataclass
class VariableState:
    variables: dict[str, Value | None]
    constants: dict[str, Value]
    functions: dict[str, FunctionDecl]
    procedures: dict[str, ProcedureDecl]
