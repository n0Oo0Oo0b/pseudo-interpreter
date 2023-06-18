__all__ = [
    "PrimitiveType",
    "ArrayType",
    "Type",
]


from dataclasses import dataclass
from enum import Enum

from cambridgeScript.syntax_tree import Expression


class PrimitiveType(Enum):
    INTEGER = int
    REAL = float
    CHAR = str
    STRING = str
    BOOLEAN = bool


@dataclass(frozen=True)
class ArrayType:
    type: PrimitiveType
    ranges: list[tuple[Expression, Expression]]


Type = PrimitiveType | ArrayType
