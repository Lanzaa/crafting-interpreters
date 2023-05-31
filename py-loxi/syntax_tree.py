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

@dataclass
class Variable(Expr):
  name: Token

@dataclass
class Assign(Expr):
  name: Token
  value: Expr


"""
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
    case Variable(name):
      pass
    case Assign(name, value):
      pass
    case _:
      raise ValueError("Unknown type")
"""


class Stmt:
  pass

@dataclass
class Expression(Stmt):
  expression: Expr

@dataclass
class Print(Stmt):
  expression: Expr

@dataclass
class Var(Stmt):
  name: Token
  initializer: Expr

"""
def pattern_match_example(node: Stmt):
  match node:
    case Expression(expression):
      pass
    case Print(expression):
      pass
    case Var(name, initializer):
      pass
    case _:
      raise ValueError("Unknown type")
"""
