

import unittest

import loxi
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


if __name__ == '__main__':
    unittest.main()
