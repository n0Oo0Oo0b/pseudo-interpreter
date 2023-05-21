from ..constants import Keyword, Symbol
from ..syntax_tree import Expression, Literal, Identifier, Statement
from .tokens import Token, TokenComparable, LiteralToken, IdentifierToken


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self._next_index = 0

    # Helpers
    def _is_at_end(self) -> bool:
        """Returns whether the pointer is at the end"""
        return self._next_index == len(self.tokens)

    def _peek(self, offset: int = 0) -> Token | None:
        """Returns the next token without consuming"""
        if self._is_at_end():
            return None
        target = self._next_index + offset
        if not 0 <= target < len(self.tokens):
            return None
        return self.tokens[target]

    def _advance(self) -> Token:
        """Consumes and returns the next token"""
        res = self._peek()
        if not self._is_at_end():
            self._next_index += 1
        return res

    def _check(self, *targets: TokenComparable) -> Token | None:
        """Return the token if the next token matches"""
        next_token = self._peek()
        return next_token if next_token in targets else None

    def _match(self, *targets: TokenComparable) -> Token | None:
        """Consume and return the token if the next token matches"""
        res = self._check(*targets)
        if res:
            self._advance()
        return res

    def _consume(self, *targets: TokenComparable, error_message: str) -> Token:
        """Attempt to match a token, and raise an error if it fails"""
        if not (res := self._match(*targets)):
            raise ParserError(error_message)
        return res

    # Expressions

    def _expression(self) -> Expression:
        return self._assignment()

    def _assignment(self) -> Expression:
        pass

    def _logic_or(self) -> Expression:
        pass

    def _logic_and(self) -> Expression:
        pass

    def _logic_not(self) -> Expression:
        pass

    def _comparison(self) -> Expression:
        pass

    def _term(self) -> Expression:
        pass

    def _factor(self) -> Expression:
        pass

    def _call(self) -> Expression:
        pass

    def _primary(self) -> Expression:
        pass
