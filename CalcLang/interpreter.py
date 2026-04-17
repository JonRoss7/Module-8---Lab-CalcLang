import math
from ast_nodes import *

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: '{name}'")

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.functions = {}
        self.call_stack = [] 
        
        # Challenge 5: Built-in functions
        self.built_ins = {
            'sqrt': math.sqrt,
            'pow': math.pow,
            'abs': abs
        }

    def print_traceback(self):
        if not self.call_stack:
            return
        print("\n--- Call Stack Traceback ---")
        for i, (func_name, locals) in enumerate(self.call_stack):
            print(f"[{i}] Function: {func_name}() | Locals: {locals}")
        print("----------------------------")

    def visit(self, node):
        try:
            method_name = f'visit_{type(node).__name__}'
            return getattr(self, method_name, self.no_visit)(node)
        except Exception as e:
            if not isinstance(e, ReturnException):
                # Print trace automatically if a genuine error happens deeper in the tree
                if len(self.call_stack) > 0 and "Traceback" not in str(e):
                    self.print_traceback()
            raise e

    def no_visit(self, node):
        raise RuntimeError(f"No visit method for {type(node)}")

    def visit_NumberNode(self, node):
        return node.value

    def visit_VarNode(self, node):
        return self.current_env.get(node.name)

    def visit_AssignNode(self, node):
        value = self.visit(node.expr)
        self.current_env.set(node.var, value)
        return value

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # Arithmetic uses the literal symbols
        if node.op == '+': return left + right
        if node.op == '-': return left - right
        if node.op == '*': return left * right
        if node.op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
            
        # Comparisons use the token types
        if node.op == 'GT': return 1.0 if left > right else 0.0
        if node.op == 'LT': return 1.0 if left < right else 0.0
        if node.op == 'EQ': return 1.0 if left == right else 0.0
        if node.op == 'GE': return 1.0 if left >= right else 0.0
        if node.op == 'LE': return 1.0 if left <= right else 0.0
        if node.op == 'NE': return 1.0 if left != right else 0.0
        
        raise ValueError(f"Unknown op {node.op}")

    def visit_IfNode(self, node):
        # Push block scope
        previous_env = self.current_env
        self.current_env = Environment(parent=self.current_env)
        
        cond = self.visit(node.cond)
        result = None
        if cond != 0.0:
            for stmt in node.then_body:
                result = self.visit(stmt)
        else:
            for stmt in node.else_body:
                result = self.visit(stmt)
                
        # Pop block scope
        self.current_env = previous_env
        return result

    def visit_WhileNode(self, node):
        previous_env = self.current_env
        self.current_env = Environment(parent=self.current_env)
        result = None
        
        while self.visit(node.cond) != 0.0:
            for stmt in node.body:
                result = self.visit(stmt)
                
        self.current_env = previous_env
        return result

    def visit_FuncDefNode(self, node):
        self.functions[node.name] = (node.params, node.body)
        return None

    def visit_FuncCallNode(self, node):
        # Handle built-ins
        if node.name in self.built_ins:
            evaluated_args = [self.visit(arg) for arg in node.args]
            return float(self.built_ins[node.name](*evaluated_args))

        if node.name not in self.functions:
            raise NameError(f"Undefined function: '{node.name}'")
            
        params, body = self.functions[node.name]
        if len(params) != len(node.args):
            raise TypeError(f"{node.name}() takes {len(params)} arguments but {len(node.args)} were given")

        evaluated_args = [self.visit(arg) for arg in node.args]
        
        previous_env = self.current_env
        self.current_env = Environment(parent=self.global_env) 
        
        for param, arg in zip(params, evaluated_args):
            self.current_env.set(param, arg)

        self.call_stack.append((node.name, self.current_env.vars))
        
        result = None
        try:
            for stmt in body:
                result = self.visit(stmt)
        except ReturnException as ret:
            result = ret.value 
        finally:
            self.call_stack.pop()
            self.current_env = previous_env
            
        return result

    def visit_ReturnNode(self, node):
        value = self.visit(node.expr)
        raise ReturnException(value)

    def visit_PrintNode(self, node):
        value = self.visit(node.expr)
        print(value)
        return value

    def interpret(self, ast):
        result = None
        for stmt in ast:
            result = self.visit(stmt)
        return result