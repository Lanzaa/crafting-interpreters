from typing import List

#from evaluator import eval_ast

from basics import *
from syntax_tree import *
from environment import Environment
from evaluator import operateOn

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def interpret(self, stmts: List[Stmt]) -> None:
        try:
            for stmt in stmts:
                self.visitStmt(stmt)
        except Exception as e:
            print("RUNTIME ERROR: ", e)  # TODO better runtime error


    def visitStmt(self, node: Stmt):
        match node:
            case Expression(expression):
                self.eval_ast(expression)
            case Print(expression):
                print(self.eval_ast(expression))
            case Var(name, initializer):
                value = self.eval_ast(initializer) if initializer else None
                self.env.define(name, value)
            case _:
                raise NotImplementedError("Unknown statement type")  #ValueError("Unknown type")
    def eval_ast(self, node: Expr):
        match node:
            case Binary(left, operator, right):
                ## todo
                return operateOn(operator, self.eval_ast(left), self.eval_ast(right))
            case Grouping(expression):
                return self.eval_ast(expression)
            case Literal(value):
                return value
            case Unary(operator, right):
                return self.eval_unary(node)
            case Variable(name):
                return self.env.get(name)
            case _:
                raise ValueError(f"Unable to evaluate unknown type '{node}'.")

    def eval_unary(self, node: Unary):
        right = self.eval_ast(node.right)
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

eval_ast_helper = Interpreter().eval_ast

