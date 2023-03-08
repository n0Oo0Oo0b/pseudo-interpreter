from dataclasses import dataclass

from constants import TYPES


Value = str | int | float | bool


@dataclass
class Variable:
    type: type
    _value: Value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.type(value)


class VariableState:
    default_state = None

    def __init__(self, set_as_default: bool = False) -> None:
        self._variables: dict[str, Variable] = {}
        if set_as_default:
            VariableState.default_state = self

    def __getitem__(self, key) -> Value:
        return self._variables[key].value

    def __setitem__(self, key: str, value: Value) -> None:
        if key not in self._variables:
            raise RuntimeError(f'{key} not defined')
        self._variables[key].value = value

    def declare(self, name: str, type_: type, value: Value | None = None) -> None:
        value = type_(value) if value else type_()
        self._variables[name] = Variable(type_, value)
