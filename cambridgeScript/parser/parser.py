from ..constants import Keyword, Symbol, Operator
from ..syntax_tree import (
    Expression,
    Literal,
    Identifier,
    FunctionCall,
    ArrayIndex,
    BinaryOp,
    UnaryOp,
    Statement,
)
from .tokens import Token, TokenComparable, LiteralToken, IdentifierToken


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self._next_index = 0

    @classmethod
    def parse_expression(cls, tokens: list[Token]) -> Expression:
        """
        Parses a list of tokens as an expression
        :param tokens: tokens to parse
        :return: an Expression
        """
        instance = cls(tokens)
        result = instance._expression()
        if not instance._is_at_end():
            next_token = instance._peek()
            raise ParserError(f"Extra token {next_token} found")
        return result

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

    # Helper rules

    def _arguments(
        self, delimiter: TokenComparable = Symbol.COMMA, allow_empty: bool = True
    ) -> list[Expression]:
        # Get the first argument
        try:
            result = [self._expression()]
        except ParserError:
            if allow_empty:
                return []
            else:
                raise
        # Get successive arguments
        while self._match(delimiter):
            result.append(self._expression())
        return result

    # Expressions

    def _expression(self) -> Expression:
        return self._logic_or()

    def _logic_or(self) -> Expression:
        left = self._logic_and()
        while self._match(Keyword.OR):
            right = self._logic_and()
            left = BinaryOp(
                operator=Operator.OR,
                left=left,
                right=right,
            )
        return left

    def _logic_and(self) -> Expression:
        left = self._logic_not()
        while self._match(Keyword.AND):
            right = self._logic_not()
            left = BinaryOp(
                operator=Operator.AND,
                left=left,
                right=right,
            )
        return left

    def _logic_not(self) -> Expression:
        if not self._match(Keyword.NOT):
            return self._comparison()
        return UnaryOp(Operator.NOT, self._logic_not())

    def _comparison(self) -> Expression:
        left = self._term()
        while op := self._match(
            Symbol.EQUAL,
            Symbol.NOT_EQUAL,
            Symbol.LESS_EQUAL,
            Symbol.GREAT_EQUAL,
            Symbol.LESS,
            Symbol.GREAT,
        ):
            if op == Symbol.EQUAL:
                op = Operator.EQUAL
            elif op == Symbol.NOT_EQUAL:
                op = Operator.NOT_EQUAL
            elif op == Symbol.LESS_EQUAL:
                op = Operator.LESS_EQUAL
            elif op == Symbol.GREAT_EQUAL:
                op = Operator.GREAT_EQUAL
            elif op == Symbol.LESS:
                op = Operator.LESS_THAN
            else:
                op = Operator.GREATER_THAN
            right = self._term()
            left = BinaryOp(
                operator=op,
                left=left,
                right=right,
            )
        return left

    def _term(self) -> Expression:
        left = self._factor()
        while op := self._match(Symbol.ADD, Symbol.SUB):
            if op == Symbol.ADD:
                op = Operator.ADD
            else:
                op = Operator.SUB
            right = self._factor()
            left = BinaryOp(
                operator=op,
                left=left,
                right=right,
            )
        return left

    def _factor(self) -> Expression:
        left = self._call()
        while op := self._match(Symbol.DIV, Symbol.MUL):
            if op == Symbol.DIV:
                op = Operator.DIV
            else:
                op = Operator.MUL
            right = self._call()
            left = BinaryOp(
                operator=op,
                left=left,
                right=right,
            )
        return left

    def _call(self) -> Expression:
        left = self._primary()
        while start := self._match(Symbol.LPAREN, Symbol.LBRACKET):
            if start == Symbol.LPAREN:
                end_type = Symbol.RPAREN
                ast_class = FunctionCall
            else:
                end_type = Symbol.RBRAKET
                ast_class = ArrayIndex
            arg_list = self._arguments()
            self._consume(end_type, error_message=f"Unmatched '(' at {start.location}")
            left = ast_class(left, arg_list)
        return left

    def _primary(self) -> Expression:
        if start := self._match(Symbol.LPAREN):
            res = self._expression()
            self._consume(
                Symbol.RPAREN, error_message=f"Unmatched '(' at {start.location}"
            )
            return res
        next_token = self._peek()
        if isinstance(next_token, LiteralToken):
            self._advance()
            return Literal(next_token)
        elif isinstance(next_token, IdentifierToken):
            self._advance()
            return Identifier(next_token)
        else:
            raise ParserError(f"Expected expression, found {next_token} instead")
