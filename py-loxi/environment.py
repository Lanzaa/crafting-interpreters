
from basics import Token
class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value):
        print(f"defining '{name}'")
        self.values[name] = value

    def get(self, nameToken: Token):
        lexeme = nameToken.lexeme
        if lexeme in self.values:
            return self.values[lexeme]
        if self.enclosing:
            return self.enclosing.get(nameToken)
        raise RuntimeError(f"Undefined variable '{lexeme}'.")

    def assign(self, name: Token, value):
        lexeme = name.lexeme
        if lexeme in self.values:
            self.values[lexeme] = value
        elif self.enclosing:
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError(f"Undefined variable '{lexeme}'.")
