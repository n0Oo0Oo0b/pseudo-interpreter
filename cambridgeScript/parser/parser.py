from .syntax_tree import (
    Expression,
    UnaryOp,
    BinaryOp,
    Primary,
    Statement,
    ExpressionStmt,
    InputStmt,
    OutputStmt,
    DeclareStmt,
    Assignment,
)
from .tokens import Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self._next_index = 0

    # Helpers
    def _is_at_end(self) -> bool:
        """Returns whether the pointer is at the end"""
        return self._next_index == len(self.tokens)

    def _peek(self) -> Token | None:
        """Returns the next token without consuming"""
        if self._is_at_end():
            return None
        return self.tokens[self._next_index]

    def _advance(self) -> Token:
        """Consumes and returns the next token"""
        res = self._peek()
        if not self._is_at_end():
            self._next_index += 1
        return res

    def _check(self, *targets: Token | str) -> Token | None:
        """Return the token if the next token matches"""
        next_token = self._peek()
        return next_token if next_token in targets else None

    def _match(self, *targets: Token | str) -> Token | None:
        """Consume and return the token if the next token matches"""
        res = self._check(*targets)
        if res:
            self._advance()
        return res
