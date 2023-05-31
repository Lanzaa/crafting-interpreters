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

    def test_simple_enclosing(self):
        base = Environment()
        a = Environment(base)
        m_A = MockToken()
        m_A.lexeme = "A"
        m_B = MockToken()
        m_B.lexeme = "B"
        base.define(m_A.lexeme, 1.0)
        a.assign(m_A, 2.0)
        self.assertEqual(2.0, a.get(m_A))
        self.assertEqual(2.0, base.get(m_A))
        a.define(m_B.lexeme, 3.0)
        self.assertEqual(3.0, a.get(m_B))
        with self.assertRaises(RuntimeError):
            self.assertEqual(None, base.get(m_B))




if __name__ == '__main__':
    unittest.main()
