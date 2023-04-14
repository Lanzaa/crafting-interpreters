import unittest

import loxi
from loxi import TokenType, Token
from syntax_tree import *
from evaluator import *

from loxi import parseExpression

class TestEval(unittest.TestCase):

    def test_literal(self):
        e = Literal("ok")
        o = eval_ast(e)
        self.assertEqual(o, "ok")
        e = Literal(None)
        o = eval_ast(e)
        self.assertEqual(o, None)
        e = Literal(3.2)
        o = eval_ast(e)
        self.assertEqual(o, 3.2)

    def test_truth(self):
        e = Literal(False)
        o = eval_ast(e)
        self.assertEqual(o, False)
        e = Literal(True)
        o = eval_ast(e)
        self.assertEqual(o, True)

    def test_unary_negative(self):
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

    def test_truthy(self):
        TokenNot = Token(TokenType.BANG, "!", None, 1)
        e = Unary(TokenNot, Literal(3.2))
        o = eval_ast(e)
        self.assertEqual(o, False)
        e = Unary(TokenNot, Literal(None))
        o = eval_ast(e)
        self.assertEqual(o, True)
        e = Unary(TokenNot, Literal("ok"))
        o = eval_ast(e)
        self.assertEqual(o, False)

    def test_binary_numerics(self):
        TokenMinus = Token(TokenType.MINUS, "-", None, 1)
        e = Binary(Literal(3.0), TokenMinus, Literal(0.1))
        o = eval_ast(e)
        self.assertAlmostEqual(o, 2.9)

        TokenSlash = Token(TokenType.SLASH, "/", None, 1)
        e = Binary(Literal(3.0), TokenSlash, Literal(0.1))
        o = eval_ast(e)
        self.assertAlmostEqual(o, 30.0)

        TokenStar = Token(TokenType.STAR, "*", None, 1)
        e = Binary(Literal(3.0), TokenStar, Literal(0.1))
        o = eval_ast(e)
        self.assertAlmostEqual(o, 0.3)

    def test_binary_plus(self):
        TokenPlus = Token(TokenType.PLUS, "+", None, 1)
        e = Binary(Literal(3.0), TokenPlus, Literal(0.1))
        o = eval_ast(e)
        self.assertAlmostEqual(o, 3.1)
        e = Binary(Literal("hello"), TokenPlus, Literal("world"))
        o = eval_ast(e)
        self.assertEqual(o, "helloworld")

    def test_binary_comparison(self):
        TokenGreater = Token(TokenType.GREATER, ">", None, 1)
        TokenGreaterEqual = Token(TokenType.GREATER_EQUAL, ">=", None, 1)
        TokenLess = Token(TokenType.LESS, "<", None, 1)
        TokenLessEqual = Token(TokenType.LESS_EQUAL, "<=", None, 1)

        e = Binary(Literal(3.0), TokenGreater, Literal(0.1))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal(3.0), TokenGreater, Literal(4.1))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal(3.0), TokenGreater, Literal(3.0))
        self.assertEqual(eval_ast(e), False)

        e = Binary(Literal(3.0), TokenGreaterEqual, Literal(0.1))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal(3.0), TokenGreaterEqual, Literal(4.1))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal(3.0), TokenGreaterEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), True)

        e = Binary(Literal(3.0), TokenLess, Literal(0.1))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal(3.0), TokenLess, Literal(4.1))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal(3.0), TokenLess, Literal(3.0))
        self.assertEqual(eval_ast(e), False)

        e = Binary(Literal(3.0), TokenLessEqual, Literal(0.1))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal(3.0), TokenLessEqual, Literal(4.1))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal(3.0), TokenLessEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), True)

    def test_equality(self):
        TokenEqualEqual = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
        e = Binary(Literal(3.0), TokenEqualEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal(3.1), TokenEqualEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal("a"), TokenEqualEqual, Literal("a"))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal("a"), TokenEqualEqual, Literal("b"))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal("3.0"), TokenEqualEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal(None), TokenEqualEqual, Literal(None))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal(0.0), TokenEqualEqual, Literal(None))
        self.assertEqual(eval_ast(e), False)

        TokenBangEqual = Token(TokenType.BANG_EQUAL, "!=", None, 1)
        e = Binary(Literal(3.0), TokenBangEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal(3.1), TokenBangEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal("a"), TokenBangEqual, Literal("a"))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal("a"), TokenBangEqual, Literal("b"))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal("3.0"), TokenBangEqual, Literal(3.0))
        self.assertEqual(eval_ast(e), True)
        e = Binary(Literal(None), TokenBangEqual, Literal(None))
        self.assertEqual(eval_ast(e), False)
        e = Binary(Literal(0.0), TokenBangEqual, Literal(None))
        self.assertEqual(eval_ast(e), True)


    def test_runtime_errors(self):
        expr = '2 * (3 / -"muffin")'
        e = parseExpression(expr)
        self.assertEqual(eval_ast(e), True)


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
