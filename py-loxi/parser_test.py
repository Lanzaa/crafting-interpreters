
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
        print(tokens)
        r = Parser(tokens).parse()
        self.assertEqual(r, [Expression(expression=Literal(value=2.0))])
        e = r[0].expression
        o = eval_ast(e)
        self.assertEqual(o, 2.0)



if __name__ == '__main__':
    unittest.main()
