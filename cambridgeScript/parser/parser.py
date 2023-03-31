from ..constants import OPERATORS, TYPES
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
    IfStmt,
)
from .tokens import Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self._next_index = 0

    def block(self) -> list[Statement]:
        res: list[Statement] = []
        while stmt := self._statement():
            res.append(stmt)
        return res

    def expression(self) -> Expression:
        return self._comparison()

    # Helpers
    def _is_at_end(self):
        return self._next_index == len(self.tokens)

    def _peek(self) -> Token | None:
        # Returns the next token without consuming
        if self._is_at_end():
            return Token("EOF", None)
        return self.tokens[self._next_index]

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

    # Statements
    def _statement(self) -> Statement | None:
        while self._check("NEWLINE"):
            self._advance()
        if self._match("EOF"):
            return None
        elif self._match("INPUT"):
            stmt = InputStmt(self._advance())
            self._consume("NEWLINE", "Expected newline after INPUT statement")
            return stmt
        elif self._match("OUTPUT"):
            stmt = OutputStmt(self.expression())
            self._consume("NEWLINE", "Expected newline after OUTPUT statement")
            return stmt
        elif self._match("DECLARE"):
            name = self._consume("IDENTIFIER", "Expected identifier for DECLARE")
            self._consume(Token("SYMBOL", ":"), "Expected ':' after variable name")
            type_ = self._consume("IDENTIFIER", "Expected variable type after ':'")
            if type_ not in TYPES:
                raise RuntimeError(f"Invalid type name {type_.value}")
            stmt = DeclareStmt(name, TYPES[type_])
            self._consume("NEWLINE", "Expected newline after DECLARE statement")
            return stmt
        elif token := self._match("IF") or self._match("WHILE"):
            if token == "IF":
                condition_end, block_end = "THEN", "ENDIF"
            else:
                condition_end, block_end = "DO", "ENDWHILE"
            # Start
            condition = self.expression()
            self._consume(
                condition_end,
                f"{condition_end} expected after condition in if statement",
            )
            self._consume("NEWLINE", f"Newline expected after {condition_end}")
            # Body
            body: list[Statement] = []
            while not self._match(block_end):
                body.append(self._statement())
            stmt = IfStmt(condition, body)
            # Return
            self._consume("NEWLINE", f"Newline expected after {block_end}")
            return stmt
        else:
            return ExpressionStmt(self.expression())

    # Expressions
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
