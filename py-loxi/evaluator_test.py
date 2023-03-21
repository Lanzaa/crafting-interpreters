
import unittest

import loxi
from loxi import TokenType, Token
from syntax_tree import *
from evaluator import *


class TestEval(unittest.TestCase):

    def test_literal(self):
        e = Literal("ok")
        o = eval_ast(e)
        self.assertEqual(o, "ok")
        e = Literal(None)
        o = eval_ast(e)
        self.assertEqual(o, None)

    def test_truth(self):
        e = Literal(False)
        o = eval_ast(e)
        self.assertEqual(o, False)
        e = Literal(True)
        o = eval_ast(e)
        self.assertEqual(o, True)

    def test_unary_negative(self):
        # todo
        TokenNegate = Token(TokenType.MINUS, "-", None, 1)
        e = Unary(TokenNegate, Literal(2.0))
        o = eval_ast(e)
        self.assertEqual(o, -2.0)
        e = Unary(TokenNegate, Literal(-3.0))
        o = eval_ast(e)
        self.assertEqual(o, 3.0)

    def test_unary_not(self):
        TokenNot = Token(TokenType.BANG, "!", None, 1)
        e = Unary(TokenNot, Literal(True))
        o = eval_ast(e)
        self.assertEqual(o, False)
        e = Unary(TokenNot, Literal(False))
        o = eval_ast(e)
        self.assertEqual(o, True)


    """
    def test_small_expr(self):
        e = Binary(
              Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
              Token(TokenType.STAR, "*", None, 1),
              Grouping(Literal(45.67))
            )
        o = print_ast(e)
        self.assertEqual(o, "(* (- 123) (group 45.67))")
        """


if __name__ == '__main__':
    unittest.main()
