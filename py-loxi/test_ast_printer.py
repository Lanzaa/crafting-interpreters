

import unittest

import loxi
from basics import TokenType, Token
from syntax_tree import *
from ast_printer import print_ast


class TestAstPrinter(unittest.TestCase):

    def test_literal(self):
        e = Literal("ok")
        o = print_ast(e)
        self.assertEqual(o, "ok")
        e = Literal(None)
        o = print_ast(e)
        self.assertEqual(o, "nil")

    def test_small_expr(self):
        e = Binary(
              Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
              Token(TokenType.STAR, "*", None, 1),
              Grouping(Literal(45.67))
            )
        o = print_ast(e)
        self.assertEqual(o, "(* (- 123) (group 45.67))")


if __name__ == '__main__':
    unittest.main()
