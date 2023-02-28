from collections import ChainMap


Value = str | int | float | bool


class VariableState(ChainMap):
    default_state = None

    def __init__(self, set_as_default: bool = False) -> None:
        super().__init__()
        if set_as_default:
            VariableState.default_state = self

    def __getitem__(self, key) -> Value:
        if key not in self:
            raise RuntimeError(f'{key} not defined')
        return super().__getitem__(key)

    def get(self, key) -> Value | None:
        if key not in self:
            return None
        return self[key]

    def __setitem__(self, key: str, value: Value) -> None:
        if key not in self:
            raise RuntimeError(f'{key} not defined')
        super().__setitem__(key, value)

    def declare(self, key: str, type_: type, value: Value | None = None) -> None:
        super().__setitem__(key, type_(value) if value else type_())
