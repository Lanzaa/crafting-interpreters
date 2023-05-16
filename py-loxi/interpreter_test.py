
import unittest

import loxi
from loxi import TokenType, Token, Scanner
from syntax_tree import *
from evaluator import *
from parser import Parser

# Pull TokenType members into namespace
globals().update(TokenType.__members__)


class TestInterpret(unittest.TestCase):
    pass  # TODO add tests for the interpreter

if __name__ == '__main__':
    unittest.main()
