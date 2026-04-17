from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def eat(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.pos += 1
            return token[1]
        raise SyntaxError(f"Expected {expected_type}, got {token}")

    def parse_program(self):
        statements = []
        while self.current_token():
            statements.append(self.parse_statement())
        return statements

    def parse_block(self, end_tokens):
        statements = []
        while self.current_token() and self.current_token()[0] not in end_tokens:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token()
        
        if token[0] == 'IF':
            return self.parse_if()
        elif token[0] == 'WHILE':
            return self.parse_while()
        elif token[0] == 'DEF':
            return self.parse_func_def()
        elif token[0] == 'RETURN':
            self.eat('RETURN')
            expr = self.parse_expression()
            return ReturnNode(expr)
        elif token[0] == 'PRINT':
            self.eat('PRINT')
            expr = self.parse_expression()
            return PrintNode(expr)
        elif token[0] == 'ID':
            next_token = self.peek()
            if next_token and next_token[0] == 'ASSIGN':
                return self.parse_assignment()
        
        return self.parse_expression()

    def parse_assignment(self):
        var_name = self.eat('ID')
        self.eat('ASSIGN')
        expr = self.parse_expression()
        return AssignNode(var_name, expr)

    def parse_if(self):
        self.eat('IF')
        cond = self.parse_expression()
        self.eat('THEN')
        then_body = self.parse_block(['ELSE', 'END'])
        
        else_body = []
        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.eat('ELSE')
            else_body = self.parse_block(['END'])
            
        self.eat('END')
        return IfNode(cond, then_body, else_body)

    def parse_while(self):
        self.eat('WHILE')
        cond = self.parse_expression()
        self.eat('DO')
        body = self.parse_block(['END'])
        self.eat('END')
        return WhileNode(cond, body)

    def parse_func_def(self):
        self.eat('DEF')
        name = self.eat('ID')
        self.eat('LPAREN')
        params = []
        if self.current_token()[0] == 'ID':
            params.append(self.eat('ID'))
            while self.current_token()[0] == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('ID'))
        self.eat('RPAREN')
        body = self.parse_block(['END'])
        self.eat('END')
        return FuncDefNode(name, params, body)

    def parse_expression(self):
        node = self.parse_arithmetic()
        if self.current_token() and self.current_token()[0] in ('GT', 'LT', 'EQ', 'GE', 'LE', 'NE'):
            op_token = self.current_token()
            self.eat(op_token[0])
            right = self.parse_arithmetic()
            node = BinOpNode(op_token[0], node, right)
        return node

    def parse_arithmetic(self):
        node = self.parse_term()
        while self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS'):
            op = self.eat(self.current_token()[0])
            right = self.parse_term()
            node = BinOpNode(op, node, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token() and self.current_token()[0] in ('MUL', 'DIV'):
            op = self.eat(self.current_token()[0])
            right = self.parse_factor()
            node = BinOpNode(op, node, right)
        return node

    def parse_factor(self):
        token = self.current_token()
        
        if token[0] == 'MINUS':
            self.eat('MINUS')
            node = self.parse_factor()
            return BinOpNode('-', NumberNode(0.0), node)

        if token[0] == 'NUMBER':
            return NumberNode(self.eat('NUMBER'))
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        elif token[0] == 'ID':
            next_token = self.peek()
            if next_token and next_token[0] == 'LPAREN':
                return self.parse_func_call()
            return VarNode(self.eat('ID'))
            
        raise SyntaxError(f"Unexpected token in factor: {token}")

    def parse_func_call(self):
        name = self.eat('ID')
        self.eat('LPAREN')
        args = []
        if self.current_token()[0] != 'RPAREN':
            args.append(self.parse_expression())
            while self.current_token()[0] == 'COMMA':
                self.eat('COMMA')
                args.append(self.parse_expression())
        self.eat('RPAREN')
        return FuncCallNode(name, args)