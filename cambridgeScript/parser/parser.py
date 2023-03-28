from collections import deque

from cambridgeScript.constants import OPERATORS
from cambridgeScript.parser.syntax_tree import Expression, UnaryOp, BinaryOp, Primary
from cambridgeScript.parser.tokens import Token


class ExpressionParser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self._next_index = 0

    def expression(self) -> Expression:
        return self._comparison()

    # Helpers
    def _peek(self) -> Token | None:
        # Returns the next token without consuming
        return self.tokens[min(self._next_index, len(self.tokens) - 1)]

    def _advance(self) -> Token:
        # Consume the next token
        res = self._peek()
        self._next_index += 1
        return res

    def _check(self, *targets) -> Token | None:
        # Check if the next token matches specific operators
        next_token = self._peek()
        return next_token if next_token.value in targets else None

    def _match(self, *targets) -> Token | None:
        # Consume the next token if the next token matches specific operators
        res = self._check(*targets)
        if res:
            self._next_index += 1
        return res

    # Recursive descent
    def _comparison(self) -> Expression:
        expr = self._term()
        while op := self._match("=", "<>", "<", "<=", ">", ">="):
            right = self._term()
            expr = BinaryOp(OPERATORS[op.value], expr, right)
        return expr

    def _term(self) -> Expression:
        expr = self._factor()
        while op := self._match("+", "-"):
            right = self._factor()
            expr = BinaryOp(OPERATORS[op.value], expr, right)
        return expr

    def _factor(self) -> Expression:
        expr = self._unary()
        while op := self._match("*", "/"):
            right = self._unary()
            expr = BinaryOp(OPERATORS[op.value], expr, right)
        return expr

    def _unary(self) -> Expression:
        if op := self._match("+", "-"):
            operand = self._unary()
            op = (lambda x: -x) if op.value == "-" else (lambda x: +x)  # bodge
            return UnaryOp(op, operand)
        return self._primary()

    def _primary(self) -> Expression:
        token = self._advance()
        if token.type == "LITERAL" or token.type == "IDENTIFIER":
            return Primary(token)
        elif token == Token("SYMBOL", "("):
            expr = self.expression()
            next_token = self._advance()
            if next_token != Token("SYMBOL", ")"):
                raise RuntimeError("'(' was never closed")
            return expr


def parse_expression(tokens: list[Token]) -> Expression:
    parser = ExpressionParser(tokens)
    return parser.expression()
