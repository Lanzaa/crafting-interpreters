from syntax_tree import *
from basics import Token, error_parse
from basics import TokenType


# Pull TokenType members into namespace
globals().update(TokenType.__members__)

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.statement())
        return statements

    def statement(self) -> Stmt:
        if self.match(PRINT):
            return self.printStatement()
        return self.expressionStatement()

    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(SEMICOLON, "Expect ';' after value.");
        return Print(value)

    def expressionStatement(self) -> Stmt:
        pass # TODO


    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        e = self.comparison()
        while self.match(BANG_EQUAL, EQUAL_EQUAL):
            op = self.previous()
            e_right = self.comparison()
            e = Binary(e, op, e_right)
        return e

    def match(self, *types) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def check(self, type_) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type_

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self) -> bool:
        return self.peek().type == EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def comparison(self) -> Expr:
        e = self.term()
        while self.match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL):
            op = self.previous()
            e_right = self.term()
            e = Binary(e, op, e_right)
        return e

    def term(self) -> Expr:
        e = self.factor()
        while self.match(MINUS, PLUS):
            op = self.previous()
            e_right = self.factor()
            e = Binary(e, op, e_right)
        return e

    def factor(self) -> Expr:
        e = self.unary()
        while self.match(SLASH, STAR):
            op = self.previous()
            e_right = self.factor()
            e = Binary(e, op, e_right)
        return e

    def unary(self) -> Expr:
        if self.match(BANG, MINUS):
            op = self.previous()
            e_right = self.unary()
            return Unary(op, e_right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(FALSE):
            return Literal(False)
        if self.match(TRUE):
            return Literal(True)
        if self.match(NIL):
            return Literal(None)
        if self.match(NUMBER, STRING):
            return Literal(self.previous().literal)
        if self.match(LEFT_PAREN):
            e = self.expression()
            self.consume(RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(e)
        raise self.error(self.peek(), "Expect expression.")

    def consume(self, type_: TokenType, message) -> Token:
        if self.check(type_):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token, message):
        error_parse(token, message)
        return ParseError()

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == SEMICOLON:
                return
            if self.peek().type in [CLASS,FUN,VAR,FOR,IF,WHILE,PRINT,RETURN]:
                return
            self.advance()
        pass  # Can reach end of tokens


class ParseError(ValueError):
    pass
