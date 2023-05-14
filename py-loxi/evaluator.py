
from syntax_tree import *
from basics import TokenType

def parenthesize(name, *exprs) -> str:
    pretty_exprs = [f"{name}"] + [print_ast(expr) for expr in exprs]
    return "(" + " ".join(pretty_exprs) + ")"


def eval_ast(node: Expr):
  match node:
    case Binary(left, operator, right):
      ## todo
      return operateOn(operator, eval_ast(left), eval_ast(right))
    case Grouping(expression):
      return eval_ast(expression)
    case Literal(value):
      return value
    case Unary(operator, right):
      # TODO
      return eval_unary(node)
    case _:
      raise ValueError("Unknown type")


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


def eval_unary(node: Unary):
    right = eval_ast(node.right)
    match node.operator.type:
      case TokenType.MINUS:
        checkNumberOperand(None, right)
        return -1*right
      case TokenType.BANG:
        return not isTruthy(right)
    assert False, "Unknown unary operator"

def checkNumberOperand(op, a):
    if not isinstance(a, float):
        raise ValueError("Operand must be a number.")
def checkNumberOperands(op, a, b):
    if not (isinstance(a, float) and isinstance(b, float)):
        raise ValueError("Operands must be numbers.")



def isTruthy(ob) -> bool:
    if ob is None:
        return False
    if isinstance(ob, bool):
        return ob
    return True



