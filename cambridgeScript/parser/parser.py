from typing import Callable, TypeVar

from cambridgeScript.constants import Keyword, Symbol, Operator
from cambridgeScript.syntax_tree import (
    # Expressions
    Expression,
    Assignable,
    Literal,
    Identifier,
    FunctionCall,
    ArrayIndex,
    BinaryOp,
    UnaryOp,
    # Statements
    Statement,
    ProcedureDecl,
    FunctionDecl,
    IfStmt,
    CaseStmt,
    ForStmt,
    RepeatUntilStmt,
    WhileStmt,
    VariableDecl,
    ConstantDecl,
    InputStmt,
    OutputStmt,
    ReturnStmt,
    FileOpenStmt,
    FileReadStmt,
    FileWriteStmt,
    FileCloseStmt,
    ProcedureCallStmt,
    AssignmentStmt,
    Program,
    # Types
    Type,
    PrimitiveType,
    ArrayType,
)
from cambridgeScript.parser.lexer import (
    Token,
    TokenComparable,
    LiteralToken,
    KeywordToken,
    IdentifierToken,
    Value,
    EOF,
)

T = TypeVar("T")


class ParserError(Exception):
    """Base exception class for errors from the parser"""


class _InvalidMatch(ParserError):
    # Raised when the first token of a match is invalid
    # Indicates that no tokens were consumed
    pass


class UnexpectedToken(ParserError):
    """Raised when the parser encounters an unexpected token"""
    expected: TokenComparable
    actual: Token

    def __init__(self, expected: TokenComparable, actual: Token):
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return (
            f"Expected '{self.expected}' at {self.actual.location}, "
            f"found '{self.actual}' instead"
        )


class UnexpectedTokenType(ParserError):
    """Raised when the parser encounters an unexpected token type"""
    expected_type: type[Token]
    actual: Token

    def __init__(self, expected: type[Token], actual: Token):
        self.expected_type = expected
        self.actual = actual

    def __str__(self):
        return (
            f"Expected {self.expected_type.__name__.lower()} at {self.actual.location}, "
            f"found '{self.actual}' instead"
        )


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

    @classmethod
    def parse_statement(cls, tokens: list[Token]) -> Statement:
        """
        Parses a list of tokens as a single statement
        :param tokens: tokens to parse
        :return: a Statement
        """
        instance = cls(tokens)
        result = instance._statement()
        if not instance._is_at_end():
            next_token = instance._peek()
            raise ParserError(f"Extra token {next_token} found")
        return result

    @classmethod
    def parse_program(cls, tokens: list[Token]) -> Program:
        """
        Parses a list of tokens as a program (series of statements)
        :param tokens: tokens to parse
        :return: list of Statemnets
        """
        statements = cls(tokens)._statements_until(EOF)
        return Program(statements)

    # Helpers

    def _peek(self) -> Token:
        # Returns the next token without consuming
        return self.tokens[self._next_index]

    def _is_at_end(self) -> bool:
        # Returns whether the pointer is at the end
        return self._peek() == EOF

    def _advance(self) -> Token:
        # Consumes and returns the next token
        res = self._peek()
        if not self._is_at_end():
            self._next_index += 1
        return res

    def _check(self, *targets: TokenComparable) -> Token | None:
        # Return the token if the next token matches
        next_token = self._peek()
        return next_token if next_token in targets else None

    def _match(self, *targets: TokenComparable) -> Token | None:
        # Consume and return the token if the next token matches
        res = self._check(*targets)
        if res:
            self._advance()
        return res

    def _consume(self, target: TokenComparable) -> Token:
        # Attempt to match a token, and raise an error if it fails
        if not (res := self._match(target)):
            raise UnexpectedToken(target, self._peek())
        return res

    def _consume_first(self, target: TokenComparable) -> Token:
        # Variant of _consume() that raises _InvalidMatch instead
        if not (res := self._match(target)):
            raise _InvalidMatch
        return res

    def _consume_type(self, type_: type[Token]) -> Token:
        # Attempt to match a token type, throw error if fail
        next_token = self._peek()
        if not isinstance(next_token, type_):
            raise UnexpectedTokenType(type_, next_token)
        return self._advance()

    # Helper rules

    def _primitive_type(self) -> PrimitiveType:
        if not (res := self._match(Keyword.INTEGER, Keyword.REAL, Keyword.CHAR, Keyword.STRING, Keyword.BOOLEAN)):
            raise _InvalidMatch
        assert isinstance(res, KeywordToken)
        type_ = PrimitiveType[res.keyword]
        return type_

    def _array_range(self) -> tuple[Expression, Expression]:
        left = self._expression()
        self._consume(Symbol.COLON)
        right = self._expression()
        return left, right

    def _array_type(self) -> ArrayType:
        self._consume_first(Keyword.ARRAY)
        self._consume(Symbol.LBRACKET)
        ranges = self._match_multiple(self._array_range)
        self._consume(Symbol.RBRAKET)
        self._consume(Keyword.OF)
        try:
            type_ = self._primitive_type()
        except _InvalidMatch:
            raise ParserError("Expected primitive type for array")
        return ArrayType(type_, ranges)

    def _type(self) -> Type:
        try:
            return self._primitive_type()
        except _InvalidMatch:
            pass
        try:
            return self._array_type()
        except _InvalidMatch:
            pass
        raise _InvalidMatch

    def _parameter(self) -> tuple[Token, Type]:
        name = self._advance()
        self._consume(Symbol.COLON)
        type_ = self._type()
        return name, type_

    def _procedure_header(self) -> tuple[Token, list[tuple[Token, Type]]]:
        name = self._consume_type(IdentifierToken)
        if self._match(Symbol.LPAREN):
            parameters = self._match_multiple(self._parameter)
            self._consume(Symbol.RPAREN)
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
        except _InvalidMatch:
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
            return self._declare_variable()
        elif self._check(Keyword.CONSTANT):
            return self._declare_constant()
        elif self._check(Keyword.INPUT):
            return self._input()
        elif self._check(Keyword.OUTPUT):
            return self._output()
        elif self._check(Keyword.RETURN):
            return self._return()
        elif self._check(Keyword.OPENFILE):
            return self._file_open()
        elif self._check(Keyword.READFILE):
            return self._file_read()
        elif self._check(Keyword.WRITEFILE):
            return self._file_write()
        elif self._check(Keyword.CLOSEFILE):
            return self._file_close()
        elif self._check(Keyword.CALL):
            return self._procedure_call()
        else:
            return self._assignment()

    def _procedure_decl(self) -> ProcedureDecl:
        self._consume_first(Keyword.PROCEDURE)
        name, parameters = self._procedure_header()
        body = self._statements_until(Keyword.ENDPROCEDURE)
        return ProcedureDecl(name, parameters, body)

    def _function_decl(self) -> FunctionDecl:
        self._consume_first(Keyword.FUNCTION)
        name, parameters = self._procedure_header()
        self._consume(Keyword.RETURNS)
        type_ = self._type()
        body = self._statements_until(Keyword.ENDFUNCTION)
        return FunctionDecl(name, parameters, type_, body)

    def _if_stmt(self) -> IfStmt:
        self._consume_first(Keyword.IF)
        condition = self._expression()
        self._consume(Keyword.THEN)
        then_branch = self._statements_until(
            Keyword.ELSE, Keyword.ENDIF, consume_end=False
        )
        if self._match(Keyword.ELSE):
            else_branch = self._statements_until(Keyword.ENDIF)
        else:
            else_branch = None
            self._consume(Keyword.ENDIF)
        return IfStmt(condition, then_branch, else_branch)

    def _case_stmt(self) -> CaseStmt:
        self._consume_first(Keyword.CASE_OF)
        identifier = self._expression()
        cases = []
        bodies = []
        otherwise = None
        while True:
            case = self._advance()
            self._consume(Symbol.COLON)
            if case == Keyword.OTHERWISE:
                pass
            body = self._statement()
            if case == Keyword.OTHERWISE:
                otherwise = body
                self._consume(Keyword.ENDCASE)
                break
            cases.append(case)
            bodies.append(body)
            if self._match(Keyword.ENDCASE):
                break
        return CaseStmt(identifier, list(zip(cases, bodies)), otherwise)

    def _for_loop(self) -> ForStmt:
        self._consume_first(Keyword.FOR)
        identifier = self._assignable()
        start_value = self._expression()
        self._consume(Keyword.TO)
        end_value = self._expression()
        if self._match(Keyword.STEP):
            step_value = self._expression()
        else:
            step_value = None
        body = self._statements_until(Keyword.NEXT)
        # TODO optional variable after NEXT
        return ForStmt(identifier, start_value, end_value, step_value, body)

    def _repeat_loop(self) -> RepeatUntilStmt:
        self._consume_first(Keyword.REPEAT)
        body = self._statements_until(Keyword.UNTIL)
        condition = self._expression()
        return RepeatUntilStmt(body, condition)

    def _while_loop(self) -> WhileStmt:
        self._consume_first(Keyword.WHILE)
        condition = self._expression()
        self._consume(Keyword.DO)
        body = self._statements_until(Keyword.ENDWHILE)
        return WhileStmt(condition, body)

    def _declare_variable(self) -> VariableDecl:
        self._consume_first(Keyword.DECLARE)
        name = self._consume_type(IdentifierToken)
        self._consume(Symbol.COLON)
        type_ = self._type()
        return VariableDecl(name, type_)

    def _declare_constant(self) -> ConstantDecl:
        self._consume_first(Keyword.CONSTANT)
        name = self._consume_type(IdentifierToken)
        self._consume(Symbol.ASSIGN)
        value = self._consume_type(LiteralToken)
        return ConstantDecl(name, value)

    def _input(self) -> InputStmt:
        self._consume_first(Keyword.INPUT)
        identifier = self._assignable()
        return InputStmt(identifier)

    def _output(self) -> OutputStmt:
        self._consume_first(Keyword.OUTPUT)
        values = self._match_multiple(self._expression)
        return OutputStmt(values)

    def _return(self) -> ReturnStmt:
        self._consume_first(Keyword.RETURN)
        expr = self._expression()
        return ReturnStmt(expr)

    def _file_open(self) -> FileOpenStmt:
        self._consume_first(Keyword.OPENFILE)
        identifier = self._consume_type(LiteralToken)
        self._consume(Keyword.FOR)
        if self._peek() not in [Keyword.READ, Keyword.WRITE]:
            raise UnexpectedToken("File mode", self._peek())
        file_mode = self._advance()
        return FileOpenStmt(identifier, file_mode)

    def _file_read(self) -> FileReadStmt:
        self._consume_first(Keyword.READFILE)
        file = self._consume_type(LiteralToken)
        self._consume(Symbol.COMMA)
        target = self._assignable()
        return FileReadStmt(file, target)

    def _file_write(self) -> FileWriteStmt:
        self._consume_first(Keyword.WRITEFILE)
        file = self._consume_type(LiteralToken)
        self._consume(Symbol.COMMA)
        value = self._expression()
        return FileWriteStmt(file, value)

    def _file_close(self) -> FileCloseStmt:
        self._consume_first(Keyword.CLOSEFILE)
        file = self._consume_type(LiteralToken)
        return FileCloseStmt(file)

    def _procedure_call(self) -> ProcedureCallStmt:
        self._consume_first(Keyword.CALL)
        name = self._consume_type(IdentifierToken)
        if self._match(Symbol.LPAREN):
            arg_list = self._match_multiple(self._expression)
            self._consume(Symbol.RPAREN)
        else:
            arg_list = None
        return ProcedureCallStmt(name, arg_list)

    def _assignment(self) -> AssignmentStmt:
        target = self._assignable()
        self._consume(Symbol.ASSIGN)
        value = self._expression()
        return AssignmentStmt(target, value)

    # Expressions

    def _expression(self) -> Expression:
        return self._logic_or()

    def _assignable(self) -> Assignable:
        result = self._call()
        if not isinstance(result, Assignable):
            raise ParserError("Expected identifier or array index")
        return result

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
            self._consume(end_type)
            left = ast_class(left, arg_list)
        return left

    def _primary(self) -> Expression:
        if self._match(Symbol.LPAREN):
            res = self._expression()
            self._consume(Symbol.RPAREN)
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
