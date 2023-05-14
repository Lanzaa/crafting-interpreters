


class Interpreter:

    def pattern_match_example(node: Expr):
        match node:
            case Binary(left, operator, right):
                pass
            case Grouping(expression):
                pass
            case Literal(value):
                pass
            case Unary(operator, right):
                pass
            case _:
                raise ValueError("Unknown type")


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

