"""
A Python implementation of a Lox interpreter.


Requires at least python 3.10
"""


import sys
from enum import Enum, auto
from typing import *

def main(args: list[str]):
    print("ok...", args)
    match args:
        case [_, filename]:
            return runFile(filename)
        case [_]:
            return runPrompt();
    print("Usage: python loxi.py [script]");
    return 64;

def runFile(filename: str):
    with open(filename) as f:
        run(f.read())
    return 0


def runPrompt():
    try:
        while True:
            line = input("> ")
            run(line)
    except EOFError:
        print()
        pass


def run(source: str) -> str:
    raise NotImplementedError("No runFile yet")


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


class Scanner:

    def __init__(self, source: str):
        self.hadError = False
        self.start = 0
        self.current = 0
        self.line = 1
        self.source = source
        self.tokens = []

    def scanTokens(self) -> list[Token]:
        while not self.atEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        add = self.addToken
        match = self.match
        c = self.advance()
        match c:
            case '(': add(TokenType.LEFT_PAREN)
            case ')': add(TokenType.RIGHT_PAREN)
            case '{': add(TokenType.LEFT_BRACE)
            case '}': add(TokenType.RIGHT_BRACE)
            case ',': add(TokenType.COMMA)
            case '.': add(TokenType.DOT)
            case '-': add(TokenType.MINUS)
            case '+': add(TokenType.PLUS)
            case ';': add(TokenType.SEMICOLON)
            case '*': add(TokenType.STAR)
            case '!': add(TokenType.BANG if not match('=') else TokenType.BANG_EQUAL)
            case '=': add(TokenType.EQUAL if not match('=') else TokenType.EQUAL_EQUAL)
            case '<': add(TokenType.LESS if not match('=') else TokenType.LESS_EQUAL)
            case '>': add(TokenType.GREATER if not match('=') else TokenType.GREATER_EQUAL)
            case '/':
                if match('/'):
                    while self.peek() != '\n' and not self.atEnd():
                        self.advance()
                else:
                    add(TokenType.SLASH)
            case ' ' | "\r" | "\t": pass  # ignore whitespace
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.number()
            case _:
                if isAlpha(c):
                    self.identifier()
                else:
                    self.error("Unexpected character.")
        return

    def addToken(self, type_: TokenType, literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def atEnd(self) -> bool:
        return self.current >= len(self.source)

    def match(self, c: str) -> bool:
        if self.peek() != c:
            return False
        self.advance()
        return True

    def peek(self, lookAhead = 1):
        if self.atEnd():
            return '\0'
        if lookAhead == 1:
            return self.source[self.current]
        if self.current + lookAhead > len(self.source):
            return '\0'
        return self.source[self.current + lookAhead - 1]

    def string(self):
        while not self.peek() == '"' and not self.atEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.atEnd():
            self.error("Unterminated string.")
            return
        self.advance()
        b = self.start + 1
        e = self.current - 1
        value = self.source[b:e]
        self.addToken(TokenType.STRING, value)

    def number(self):
        while isDigit(self.peek()):
            self.advance()
        if self.peek() == '.' and isDigit(self.peek(2)):
            self.advance()  # Consume '.'
            while isDigit(self.peek()):
                self.advance()
        value = self.source[self.start:self.current]
        self.addToken(TokenType.NUMBER, float(value))
    
    def identifier(self):
        while isAlpha(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        type_ = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.addToken(type_)

    def error(self, msg: str):
        report(self.line, "", msg)
        self.hadError = True

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



def printScanner(source: str) -> str:
    """
    Scan a source string and lex, then print one token per line.
    """
    scanner = Scanner(source)
    tokens: list[Token] = scanner.scanTokens()

    for token in tokens:
        print(token)
    return 0

run = printScanner

if __name__ == "__main__":
    exit(main(sys.argv))



