class ASTNode:
    pass

class BinOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name

class AssignNode(ASTNode):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class IfNode(ASTNode):
    def __init__(self, cond, then_body, else_body):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class WhileNode(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class FuncDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FuncCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class PrintNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr