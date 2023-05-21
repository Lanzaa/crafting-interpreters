
from syntax_tree import *
from basics import TokenType

def parenthesize(name, *exprs) -> str:
    pretty_exprs = [f"{name}"] + [print_ast(expr) for expr in exprs]
    return "(" + " ".join(pretty_exprs) + ")"

def operateOn(op: Token, left, right):
    match op.type:
        case TokenType.MINUS:
            return left - right
        case TokenType.SLASH:
            return left / right
        case TokenType.STAR:
            return left * right
        case TokenType.PLUS:
            return left + right
        case TokenType.GREATER:
            return left > right
        case TokenType.GREATER_EQUAL:
            return left >= right
        case TokenType.LESS:
            return left < right
        case TokenType.LESS_EQUAL:
            return left <= right
        case TokenType.EQUAL_EQUAL:
            return left == right
        case TokenType.BANG_EQUAL:
            return left != right
        case _:
            assert False, "invalid binary op"
    assert False, "invalid binary op"

