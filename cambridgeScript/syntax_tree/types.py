__all__ = [
    "PrimitiveType",
    "ArrayType",
    "Type",
]


from dataclasses import dataclass
from enum import Enum


class PrimitiveType(Enum):
    INTEGER = int
    REAL = float
    CHAR = str
    STRING = str
    BOOLEAN = bool


@dataclass(frozen=True)
class ArrayType:
    type: PrimitiveType
    ranges: list[tuple[int, int]]


Type = PrimitiveType | ArrayType
