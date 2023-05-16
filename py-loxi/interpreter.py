from typing import List

from evaluator import eval_ast
from syntax_tree import *

class Interpreter:

    """
    def interpret(self, expr: Expr) -> None:  # Prints the results of an Expression
        try:
            result = eval_ast(expr)
            print(stringify(result))
        except RuntimeError:
            print("RUNTIME ERROR")  # TODO better error message
    """

    def interpret(self, stmts: List[Stmt]) -> None:
        try:
            for stmt in stmts:
                visitStmt(stmt)
        except:
            print("RUNTIME ERROR")  # TODO better runtime error


def visitStmt(node: Stmt):
  match node:
    case Expression(expression):
        eval_ast(expression)
    case Print(expression):
        print(eval_ast(expression))
    case _:
      raise ValueError("Unknown type")

def stringify(o) -> str:
    if o is None:
        return "nil"
    # TODO truncate integers, ie "2.0" -> "2"
    return str(o)

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

