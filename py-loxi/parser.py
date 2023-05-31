from typing import List

from syntax_tree import *
from basics import Token, error_parse
from basics import TokenType


# Pull TokenType members into namespace
globals().update(TokenType.__members__)

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[Stmt]:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    def declaration(self) -> Stmt:
        try:
            if self.match(VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError as e:
            print("Parse error")
            self.synchronize()
            return None

    def varDeclaration(self) -> Var:
        name = self.consume(IDENTIFIER, "Expect a name after 'var'.") # self.variable() # ??
        expr = None
        if self.match(EQUAL):
            expr = self.expression()
        self.consume(SEMICOLON, "Expect ';' after value.");
        return Var(name=name, initializer=expr)

    def statement(self) -> Stmt:
        if self.match(PRINT):
            return self.printStatement()
        return self.expressionStatement()

    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(SEMICOLON, "Expect ';' after value.");
        return Print(value)

    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(SEMICOLON, "Expect ';' after value.");
        return Expression(expr)
    
    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.equality();
        if self.match(EQUALS):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

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
        if self.match(IDENTIFIER):
            return Variable(self.previous())
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
