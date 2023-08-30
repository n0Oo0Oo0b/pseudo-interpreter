from cambridgeScript.interpreter.variables import VariableState
from cambridgeScript.parser.lexer import LiteralToken, Value
from cambridgeScript.syntax_tree import (
    Expression,
    Identifier,
    Literal,
    ArrayIndex,
    FunctionCall,
    UnaryOp,
    BinaryOp,
    Statement,
    AssignmentStmt,
    ProcedureCallStmt,
    FileCloseStmt,
    FileWriteStmt,
    FileReadStmt,
    FileOpenStmt,
    ReturnStmt,
    OutputStmt,
    InputStmt,
    ConstantDecl,
    VariableDecl,
    WhileStmt,
    RepeatUntilStmt,
    ForStmt,
    CaseStmt,
    IfStmt,
    FunctionDecl,
    ProcedureDecl,
    Program,
)
from cambridgeScript.syntax_tree.visitors import ExpressionVisitor, StatementVisitor


class InterpreterError(Exception):
    pass


class InvalidNode(InterpreterError):
    node: Statement | Expression

    def __init__(self, node: Statement | Expression):
        self.node = node


class Interpreter(ExpressionVisitor, StatementVisitor):
    variable_state: VariableState

    def __init__(self, vairable_state: VariableState):
        self.variable_state = vairable_state

    def visit(self, thing: Expression | Statement):
        if isinstance(thing, Expression):
            return ExpressionVisitor.visit(self, thing)
        else:
            return StatementVisitor.visit(self, thing)

    def visit_statements(self, statements: list[Statement]):
        for stmt in statements:
            self.visit(stmt)

    def visit_binary_op(self, expr: BinaryOp) -> Value:
        left = self.visit(expr.left)
        right = self.visit(expr.right)
        return expr.operator(left, right)

    def visit_unary_op(self, expr: UnaryOp) -> Value:
        operand = self.visit(expr.operand)
        return expr.operator(operand)

    def visit_function_call(self, expr: FunctionCall) -> Value:
        raise NotImplementedError

    def visit_array_index(self, expr: ArrayIndex) -> Value:
        raise NotImplementedError

    def visit_literal(self, expr: Literal) -> Value:
        if not isinstance(expr.token, LiteralToken):
            raise InvalidNode
        return expr.token.value

    def visit_identifier(self, expr: Identifier) -> Value:
        name = expr.token.value
        if name not in self.variable_state.variables:
            raise InterpreterError(f"Name {name} isn't defined")
        value = self.variable_state.variables[name]
        if value is None:
            raise InterpreterError(f"Name {name} has no value")
        return value

    def visit_proc_decl(self, stmt: ProcedureDecl) -> None:
        raise NotImplementedError

    def visit_func_decl(self, stmt: FunctionDecl) -> None:
        raise NotImplementedError

    def visit_if(self, stmt: IfStmt) -> None:
        condition = self.visit(stmt.condition)
        if condition:
            self.visit_statements(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.visit_statements(stmt.else_branch)

    def visit_case(self, stmt: CaseStmt) -> None:
        raise NotImplementedError

    def visit_for_loop(self, stmt: ForStmt) -> None:
        if isinstance(stmt, ArrayIndex):
            raise NotImplemented
        name = stmt.variable.token.value
        current_value = self.visit(stmt.start)
        end_value = self.visit(stmt.end)
        if stmt.step is not None:
            step_value = self.visit(stmt.step)
        else:
            step_value = 1
        while current_value <= end_value:
            self.variable_state.variables[name] = current_value
            self.visit_statements(stmt.body)
            current_value += step_value

    def visit_repeat_until(self, stmt: RepeatUntilStmt) -> None:
        raise NotImplementedError

    def visit_while(self, stmt: WhileStmt) -> None:
        raise NotImplementedError

    def visit_variable_decl(self, stmt: VariableDecl) -> None:
        self.variable_state.variables[stmt.name.value] = None

    def visit_constant_decl(self, stmt: ConstantDecl) -> None:
        raise NotImplementedError

    def visit_input(self, stmt: InputStmt) -> None:
        raise NotImplementedError

    def visit_output(self, stmt: OutputStmt) -> None:
        values = []
        for expr in stmt.values:
            values.append(self.visit(expr))
        print("".join(map(str, values)))

    def visit_return(self, stmt: ReturnStmt) -> None:
        raise NotImplementedError

    def visit_f_open(self, stmt: FileOpenStmt) -> None:
        raise NotImplementedError

    def visit_f_read(self, stmt: FileReadStmt) -> None:
        raise NotImplementedError

    def visit_f_write(self, stmt: FileWriteStmt) -> None:
        raise NotImplementedError

    def visit_f_close(self, stmt: FileCloseStmt) -> None:
        raise NotImplementedError

    def visit_proc_call(self, stmt: ProcedureCallStmt) -> None:
        raise NotImplementedError

    def visit_assign(self, stmt: AssignmentStmt) -> None:
        if isinstance(stmt.target, ArrayIndex):
            raise NotImplemented
        name = stmt.target.token.value
        if name not in self.variable_state.variables:
            raise InterpreterError(f"{name} was not declared")
        self.variable_state.variables[name] = self.visit(stmt.value)

    def visit_program(self, stmt: Program) -> None:
        self.visit_statements(stmt.statements)
