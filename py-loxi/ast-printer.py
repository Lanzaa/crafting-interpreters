

def parenthesize(name, exprs: list) -> str:
    pretty_exprs = [f"{name}"] + [print_ast(expr) for expr in exprs]
    return "(" + " ".join(pretty_exprs) + ")"


def print_ast(node: Expr):
  match node:
    case Binary(left: Expr, operator: Token, right: Expr):
      pass
    case Grouping(expression: Expr):
      pass
    case Literal(value: Object):
      pass
    case Unary(operator: Token, right: Expr):
      pass
    case _:
      raise ValueError("Unknown type")

