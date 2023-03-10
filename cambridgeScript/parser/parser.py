from collections import deque

from cambridgeScript.constants import OPERATORS
from cambridgeScript.parser.syntax_tree import Expression, Value, BinaryOp
from cambridgeScript.parser.tokens import Token


def parse_expression(expr: list[Token]) -> Expression:
    if len(expr) == 1:
        token = expr[0]
        if token.type == 'LITERAL' or token.type == 'IDENTIFIER':
            return Value(expr[0])
        else:
            raise RuntimeError('Invalid token in expression')
    # Resolve parenthesis
    stack = deque([current := []])
    for token in expr:
        if token == Token('SYMBOL', '('):
            stack.append(current := [])
        elif token == Token('SYMBOL', ')'):
            inside = stack.pop()
            current = stack[-1]
            inside = parse_expression(inside)
            current.append(inside)
        else:
            current.append(token)
    # Resolve operations
    expr = stack[0]
    for op in [  # Lower precedence goes first
        'OR', 'AND',
        '=', '<>', '<', '>', '<=', '>=',
        '+', '-', '*', '/', '^',
    ]:
        if Token('OPERATOR', op) in expr:
            operator = OPERATORS[op]
            i = expr.index(Token('OPERATOR', op))
            left = parse_expression(expr[:i])
            right = parse_expression(expr[i + 1:])
            return BinaryOp(operator, left, right)
    raise RuntimeError('Invalid expression', expr)
