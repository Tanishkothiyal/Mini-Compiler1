class ASTNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None


    def eat(self, token_type):
        token = self.current()
        if token and token[0] == token_type:
            self.pos += 1
            return token
        raise SyntaxError("Unexpected token")


    def factor(self):
        token = self.current()

        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ASTNode(token[1])

        elif token[0] == 'ID':
            self.eat('ID')
            return ASTNode(token[1])

        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node


    def term(self):
        node = self.factor()

        while self.current() and self.current()[0] in ('MULT', 'DIV'):
            op = self.current()
            self.eat(op[0])
            node = ASTNode(op[1], node, self.factor())

        return node


    def expr(self):
        node = self.term()

        while self.current() and self.current()[0] in ('PLUS', 'MINUS'):
            op = self.current()
            self.eat(op[0])
            node = ASTNode(op[1], node, self.term())

        return node


    def parse(self):
        return self.expr()