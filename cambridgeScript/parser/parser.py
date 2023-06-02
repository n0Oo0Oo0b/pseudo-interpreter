from typing import Callable, TypeVar

from ..constants import Keyword, Symbol, Operator
from ..syntax_tree import (
    Expression,
    Literal,
    Identifier,
    FunctionCall,
    ArrayIndex,
    BinaryOp,
    UnaryOp,
    CaseStmt,
    Statement,
    ProcedureDecl,
    FunctionDecl,
    IfStmt,
    ForStmt,
    RepeatUntilStmt,
    WhileStmt,
    VariableDecl,
    ConstantDecl,
    InputStmt,
    OutputStmt,
    Type,
    PrimitiveType,
    ArrayType,
)
from .tokens import (
    Token,
    TokenComparable,
    LiteralToken,
    KeywordToken,
    IdentifierToken,
    Value,
)

T = TypeVar("T")


class ParserError(Exception):
    pass


class _InvalidMatchError(ParserError):
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

    def _advance(self) -> Token | None:
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

    def _primitive_type(self) -> PrimitiveType:
        next_token = self._peek()
        # Primitive types and 'ARRAY' are all keywords
        if not isinstance(next_token, KeywordToken):
            raise _InvalidMatchError
        try:
            type_ = PrimitiveType[next_token.keyword]
        except KeyError:
            raise _InvalidMatchError
        self._advance()
        return type_

    def _array_range(self) -> tuple[Expression, Expression]:
        left = self._expression()
        self._consume(Symbol.COLON, error_message="Missing ':' in array range")
        right = self._expression()
        return left, right

    def _array_type(self) -> ArrayType:
        if not self._match(Keyword.ARRAY):
            raise _InvalidMatchError
        self._consume(Symbol.LBRACKET, error_message="Expected '[' after 'ARRAY'")
        ranges = self._match_multiple(self._array_range)
        self._consume(Symbol.RBRAKET, error_message="Unmatched ']' after array size")
        self._consume(Keyword.OF, error_message="Expected 'OF' after 'ARRAY[...]'")
        try:
            type_ = self._primitive_type()
        except _InvalidMatchError:
            raise ParserError("Expected primitive type for array")
        return ArrayType(type_, ranges)

    def _type(self) -> Type:
        try:
            return self._primitive_type()
        except _InvalidMatchError:
            pass
        try:
            return self._array_type()
        except _InvalidMatchError:
            pass
        raise _InvalidMatchError

    def _parameter(self) -> tuple[Token, Type]:
        name = self._advance()
        self._consume(Symbol.COLON, error_message="Missing ':' in array range")
        type_ = self._type()
        return name, type_

    def _procedure_header(self) -> tuple[Token, list[tuple[Token, Type]]]:
        name = self._advance()  # ensure identifier
        if self._match(Symbol.LPAREN):
            parameters = self._match_multiple(self._parameter)
            self._consume(Symbol.RPAREN, error_message="')' expected")
        else:
            parameters = None
        return name, parameters

    # Generic helpers

    def _match_multiple(
        self,
        getter: Callable[[], T],
        *,
        delimiter: TokenComparable | None = Symbol.COMMA,
    ) -> list[T]:
        # First item
        try:
            result = [getter()]
        except ParserError:
            return []
        # Successive items
        while self._match(delimiter):
            result.append(getter())
        return result

    def _statements_until(
        self, *tokens: TokenComparable, consume_end: bool = True
    ) -> list[Statement]:
        result = []
        while not self._check(*tokens):
            result.append(self._statement())
        if consume_end:
            self._advance()
        return result

    def _binary_op(
        self,
        operand_getter: Callable[[], Expression],
        operator_mapping: dict[TokenComparable, Callable[[Value, Value], Value]],
    ) -> Expression:
        left = operand_getter()
        while op_token := self._match(*operator_mapping):
            op = operator_mapping[op_token]
            right = operand_getter()
            left = BinaryOp(
                operator=op,
                left=left,
                right=right,
            )
        return left

    # Statements

    def _statement(self) -> Statement:
        if self._check(Keyword.PROCEDURE):
            return self._procedure_decl()
        elif self._check(Keyword.FUNCTION):
            return self._function_decl()
        elif self._check(Keyword.IF):
            return self._if_stmt()
        elif self._check(Keyword.CASE_OF):
            return self._case_stmt()
        elif self._check(Keyword.FOR):
            return self._for_loop()
        elif self._check(Keyword.REPEAT):
            return self._repeat_loop()
        elif self._check(Keyword.WHILE):
            return self._while_loop()
        elif self._check(Keyword.DECLARE):
            return self._declare()
        elif self._check(Keyword.CONSTANT):
            return self._declare_constant()
        elif self._check(Keyword.INPUT):
            return self._input()
        elif self._check(Keyword.OUTPUT):
            return self._output()
        raise _InvalidMatchError

    def _procedure_decl(self) -> ProcedureDecl:
        pass

    def _function_decl(self) -> FunctionDecl:
        pass

    def _if_stmt(self) -> IfStmt:
        pass

    def _case_stmt(self) -> CaseStmt:
        identifier = self._expression()
        cases = []
        bodies = []
        otherwise = None
        while True:
            case = self._advance()
            self._consume(Symbol.COLON, error_message="':' expected after case")
            if case == Keyword.OTHERWISE:
                pass
            body = self._statement()
            if case == Keyword.OTHERWISE:
                otherwise = body
                self._consume(
                    Keyword.ENDCASE,
                    error_message="'ENDCASE' expected after OTHERWISE case",
                )
                break
            cases.append(case)
            bodies.append(body)
            if self._match(Keyword.ENDCASE):
                break
        return CaseStmt(identifier, list(zip(cases, bodies)), otherwise)

    def _for_loop(self) -> ForStmt:
        pass

    def _repeat_loop(self) -> RepeatUntilStmt:
        pass

    def _while_loop(self) -> WhileStmt:
        pass

    def _declare(self) -> VariableDecl:
        pass

    def _declare_constant(self) -> ConstantDecl:
        pass

    def _input(self) -> InputStmt:
        pass

    def _output(self) -> OutputStmt:
        pass

    # Expressions

    def _expression(self) -> Expression:
        return self._logic_or()

    def _logic_or(self) -> Expression:
        return self._binary_op(self._logic_and, {Keyword.OR: Operator.OR})

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
        return self._binary_op(
            self._term,
            {
                Symbol.EQUAL: Operator.EQUAL,
                Symbol.NOT_EQUAL: Operator.NOT_EQUAL,
                Symbol.LESS_EQUAL: Operator.LESS_EQUAL,
                Symbol.GREAT_EQUAL: Operator.GREAT_EQUAL,
                Symbol.LESS: Operator.LESS_THAN,
                Symbol.GREAT: Operator.GREATER_THAN,
            },
        )

    def _term(self) -> Expression:
        return self._binary_op(
            self._factor, {Symbol.ADD: Operator.ADD, Symbol.SUB: Operator.SUB}
        )

    def _factor(self) -> Expression:
        return self._binary_op(
            self._call, {Symbol.MUL: Operator.MUL, Symbol.DIV: Operator.DIV}
        )

    def _call(self) -> Expression:
        left = self._primary()
        while start := self._match(Symbol.LPAREN, Symbol.LBRACKET):
            ast_class: type[FunctionCall | ArrayIndex]
            if start == Symbol.LPAREN:
                end_type = Symbol.RPAREN
                ast_class = FunctionCall
            else:
                end_type = Symbol.RBRAKET
                ast_class = ArrayIndex
            arg_list = self._match_multiple(self._expression)
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
