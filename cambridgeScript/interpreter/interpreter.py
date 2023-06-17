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

    def visit_binary_op(self, expr: BinaryOp) -> Value:
        left = self.visit(expr.left)
        right = self.visit(expr.right)
        return expr.operator(left, right)

    def visit_unary_op(self, expr: UnaryOp) -> Value:
        operand = self.visit(expr.operand)
        return expr.operator(operand)

    def visit_function_call(self, expr: FunctionCall) -> Value:
        raise NotImplemented

    def visit_array_index(self, expr: ArrayIndex) -> Value:
        raise NotImplemented

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
        pass

    def visit_func_decl(self, stmt: FunctionDecl) -> None:
        pass

    def visit_if(self, stmt: IfStmt) -> None:
        pass

    def visit_case(self, stmt: CaseStmt) -> None:
        pass

    def visit_for_loop(self, stmt: ForStmt) -> None:
        pass

    def visit_repeat_until(self, stmt: RepeatUntilStmt) -> None:
        pass

    def visit_while(self, stmt: WhileStmt) -> None:
        pass

    def visit_variable_decl(self, stmt: VariableDecl) -> None:
        self.variable_state.variables[stmt.name.value] = None

    def visit_constant_decl(self, stmt: ConstantDecl) -> None:
        pass

    def visit_input(self, stmt: InputStmt) -> None:
        pass

    def visit_output(self, stmt: OutputStmt) -> None:
        values = []
        for expr in stmt.values:
            values.append(self.visit(expr))
        print("".join(map(str, values)))

    def visit_return(self, stmt: ReturnStmt) -> None:
        pass

    def visit_f_open(self, stmt: FileOpenStmt) -> None:
        pass

    def visit_f_read(self, stmt: FileReadStmt) -> None:
        pass

    def visit_f_write(self, stmt: FileWriteStmt) -> None:
        pass

    def visit_f_close(self, stmt: FileCloseStmt) -> None:
        pass

    def visit_proc_call(self, stmt: ProcedureCallStmt) -> None:
        pass

    def visit_assign(self, stmt: AssignmentStmt) -> None:
        if isinstance(stmt.target, ArrayIndex):
            raise NotImplemented
        name = stmt.target.token.value
        if name not in self.variable_state.variables:
            raise InterpreterError(f"{name} was not declared")
        self.variable_state.variables[name] = self.visit(stmt.value)

    def visit_program(self, stmt: Program) -> None:
        for s in stmt.statements:
            self.visit(s)
