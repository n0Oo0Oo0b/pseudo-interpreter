from dataclasses import dataclass

from cambridgeScript.parser.lexer import Value
from cambridgeScript.syntax_tree import FunctionDecl, ProcedureDecl


class _MissingValueSentinel:
    pass


MissingValue = _MissingValueSentinel()


@dataclass
class VariableState:
    variables: dict[str, Value | _MissingValueSentinel]
    constants: dict[str, Value]
    functions: dict[str, FunctionDecl]
    procedures: dict[str, ProcedureDecl]
