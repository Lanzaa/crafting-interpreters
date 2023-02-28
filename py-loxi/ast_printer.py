
from syntax_tree import *

def parenthesize(name, *exprs) -> str:
    pretty_exprs = [f"{name}"] + [print_ast(expr) for expr in exprs]
    return "(" + " ".join(pretty_exprs) + ")"


def print_ast(node: Expr) -> str:
  match node:
    case Binary(left, operator, right):
      return parenthesize(operator.lexeme, left, right)
    case Grouping(expression):
      return parenthesize("group", expression)
    case Literal(value):
      return f"{value}" if value is not None else "nil"
    case Unary(operator, right):
      return parenthesize(operator.lexeme, right)
    case _:
      raise ValueError("Unknown type")

