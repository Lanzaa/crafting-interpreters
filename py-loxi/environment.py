
from basics import Token
class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value):
        print(f"defining '{name}'")
        self.values[name] = value

    def get(self, nameToken: Token):
        lexeme = nameToken.lexeme
        if lexeme in self.values:
            return self.values[lexeme]
        raise RuntimeError(f"Undefined variable '{lexeme}'.")
