from basics import Token
from dataclasses import dataclass

class Expr:
  pass

@dataclass
class Binary(Expr):
  left: Expr
  operator: Token
  right: Expr

@dataclass
class Grouping(Expr):
  expression: Expr

@dataclass
class Literal(Expr):
    value: object

@dataclass
class Unary(Expr):
  operator: Token
  right: Expr


"""
def pattern_match_example(node: Expr):
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

"""
