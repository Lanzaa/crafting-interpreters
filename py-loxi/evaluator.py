
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
    return -9


def eval_unary(node: Unary):
    right = eval_ast(node.right)
    node.right
    node.operator
    match node.operator.type:
      case TokenType.MINUS:
        return -1*right
      case TokenType.BANG:
        return not isTruthy(right)
    assert False, "Unknown unary operator"


def isTruthy(ob) -> bool:
    if ob is None:
        return False
    if isinstance(ob, bool):
        return ob
    return True



