
import unittest

import loxi
from loxi import TokenType, Token, Scanner
from syntax_tree import *
from evaluator import *
from parser import Parser

# Pull TokenType members into namespace
globals().update(TokenType.__members__)


class TestParse(unittest.TestCase):
    def test_literal(self):
        tokens: list[Token] = Scanner("2;").scanTokens()
        r = Parser(tokens).parse()
        self.assertEqual(r, [Expression(expression=Literal(value=2.0))])
        e = r[0].expression
        o = eval_ast(e)
        self.assertEqual(o, 2.0)

    def test_print_statement(self):
        tokens: list[Token] = Scanner("print \"Hello World\";").scanTokens()
        r = Parser(tokens).parse()
        self.assertEqual(r, [Print(expression=Literal(value="Hello World"))])
        e = r[0].expression
        o = eval_ast(e)
        self.assertEqual(o, "Hello World")

    def test_expression_statement(self):
        tokens: list[Token] = Scanner("2+3;").scanTokens()
        r = Parser(tokens).parse()
        PLUS = Token(TokenType.PLUS, None, None, None)
        e = r[0].expression
        o = eval_ast(e)
        self.assertEqual(o, 5.0)

    def test_declaration(self):
        tokens = Scanner("var x = 1;").scanTokens()
        r = Parser(tokens).parse()
        name = r[0].name
        self.assertEqual(IDENTIFIER, name.type)
        self.assertEqual("x", name.lexeme)
        expr = r[0].initializer
        self.assertEqual(Literal(value=1.0), expr)
        self.assertEqual(1.0, eval_ast(expr))
    def test_empty_declaration(self):
        tokens = Scanner("var x;").scanTokens()
        r = Parser(tokens).parse()
        name = r[0].name
        self.assertEqual(IDENTIFIER, name.type)
        self.assertEqual("x", name.lexeme)
        expr = r[0].initializer
        self.assertEqual(None, expr)






if __name__ == '__main__':
    unittest.main()
