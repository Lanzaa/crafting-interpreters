from enum import Enum, auto

class TokenType(Enum):
  # Single-character tokens.
  LEFT_PAREN = auto()
  RIGHT_PAREN = auto()
  LEFT_BRACE = auto()
  RIGHT_BRACE = auto()
  COMMA = auto()
  DOT = auto()
  MINUS = auto()
  PLUS = auto()
  SEMICOLON = auto()
  SLASH = auto()
  STAR = auto()

  # One or two character tokens.
  BANG = auto()
  BANG_EQUAL = auto()
  EQUAL = auto()
  EQUAL_EQUAL = auto()
  GREATER = auto()
  GREATER_EQUAL = auto()
  LESS = auto()
  LESS_EQUAL = auto()

  # Literals.
  IDENTIFIER = auto()
  STRING = auto()
  NUMBER = auto()

  # Keywords.
  AND = auto()
  CLASS = auto()
  ELSE = auto()
  FALSE = auto()
  FUN = auto()
  FOR = auto()
  IF = auto()
  NIL = auto()
  OR = auto()
  PRINT = auto()
  RETURN = auto()
  SUPER = auto()
  THIS = auto()
  TRUE = auto()
  VAR = auto()
  WHILE = auto()

  EOF = auto()



class Token:
    def __init__(self, type_: TokenType, lexeme: str, literal, line: int):
        self.type: TokenType = type_
        self.lexeme: str = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

"""Simple mapping from keyword to TokenType."""
KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


def isDigit(c) -> bool:
    match c:
        case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
            return True
    return False

def isAlpha(c) -> bool:
    return ((c >= 'a' and c <= 'z') or
           (c >= 'A' and c <= 'Z') or
           c == '_')

def error(line: int, msg: str):
    report(line, "", msg)

def report(line: int, where: str, msg: str):
    print(f"[{line}] Error{where}: {msg}")

def error_parse(token, message):
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)
