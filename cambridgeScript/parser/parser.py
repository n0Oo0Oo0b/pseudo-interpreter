from ..constants import OPERATORS
from .syntax_tree import Expression, UnaryOp, BinaryOp, Primary
from .tokens import Token


class Parser:
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

    def _check(self, *targets: Token | str) -> Token | None:
        # Return the next token if the next token is in targets
        next_token = self._peek()
        return next_token if next_token in targets else None

    def _match(self, *targets: Token | str) -> Token | None:
        # Consume and return the next token if the next token is in targets
        res = self._check(*targets)
        if res:
            self._next_index += 1
        return res

    def _consume(self, target: Token | str, fail_message: str) -> Token:
        # Attempts to match a token or token type, raises error if fail
        if not (res := self._match(target)):
            raise RuntimeError(fail_message)
        return res

    def _match_operator(self, *operators: str) -> Token | None:
        # Match certain operators
        return self._match(*[Token("OPERATOR", op) for op in operators])

    # Recursive descent
    def _comparison(self) -> Expression:
        expr = self._term()
        while op := self._match_operator("=", "<>", "<", "<=", ">", ">="):
            right = self._term()
            expr = BinaryOp(OPERATORS[op.value], expr, right)
        return expr

    def _term(self) -> Expression:
        expr = self._factor()
        while op := self._match_operator("+", "-"):
            right = self._factor()
            expr = BinaryOp(OPERATORS[op.value], expr, right)
        return expr

    def _factor(self) -> Expression:
        expr = self._unary()
        while op := self._match_operator("*", "/"):
            right = self._unary()
            expr = BinaryOp(OPERATORS[op.value], expr, right)
        return expr

    def _unary(self) -> Expression:
        if op := self._match_operator("+", "-"):
            operand = self._unary()
            op = (lambda x: -x) if op.value == "-" else (lambda x: +x)  # bodge
            return UnaryOp(op, operand)
        return self._primary()

    def _primary(self) -> Expression:
        token = self._advance()
        if token == "LITERAL" or token == "IDENTIFIER":
            return Primary(token)
        elif token == Token("SYMBOL", "("):
            expr = self.expression()
            self._consume(Token("SYMBOL", ")"), "'(' was never closed")
            return expr
        raise RuntimeError(f"Unexpected token {token}")


def parse_expression(tokens: list[Token]) -> Expression:
    parser = Parser(tokens)
    return parser.expression()
