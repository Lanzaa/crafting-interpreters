
import unittest
from typing import List

import loxi
from basics import TokenType, Token
from interpreter import Interpreter
from syntax_tree import *
from evaluator import *
from parser import Parser

# Pull TokenType members into namespace
globals().update(TokenType.__members__)


class TestInterpret(unittest.TestCase):
    def test_basic_var_definition(self):
        a = "var a = 1;"
        e: List[Stmt] = loxi.parseStatements(a)
        i = Interpreter()
        i.interpret(e)
        result = i.eval_ast(loxi.parseExpression("a"))
        self.assertEqual(1.0, result)

    def test_basic_var_assignment(self):
        a = "var a = 1; a = 2;"
        e: List[Stmt] = loxi.parseStatements(a)
        i = Interpreter()
        i.interpret(e)
        result = i.eval_ast(loxi.parseExpression("a"))
        self.assertEqual(2.0, result)

    def test_basic_blocks(self):
        a = "var a = 1; { var a = 1; a = 2; print(a); } print(a);"
        e: List[Stmt] = loxi.parseStatements(a)
        self.assertEqual(3, len(e))
        i = Interpreter()
        i.interpret(e[:1])
        result = i.eval_ast(loxi.parseExpression("a"))
        self.assertEqual(1.0, result)
        i.interpret(e[1:])
        result = i.eval_ast(loxi.parseExpression("a"))
        self.assertEqual(1.0, result)


if __name__ == '__main__':
    unittest.main()
