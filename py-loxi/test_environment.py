import unittest

from environment import *


class MockToken:
    lexeme: str

class TestEnvironment(unittest.TestCase):
    def test_undefined_var(self):
        env = Environment()
        nameToken = MockToken()
        nameToken.lexeme = "A"
        with self.assertRaises(RuntimeError):
            env.get(nameToken)

    def test_simple_var(self):
        env = Environment()
        nameToken = MockToken()
        nameToken.lexeme = "A"
        env.define(nameToken.lexeme, "B")
        self.assertEqual("B", env.get(nameToken))



if __name__ == '__main__':
    unittest.main()
