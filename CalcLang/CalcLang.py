from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def is_balanced(code):
    """
    Rudimentary check to see if we have outstanding blocks that need an 'end'.
    """
    open_blocks = code.count('def ') + code.count('if ') + code.count('while ')
    closed_blocks = code.count('end')
    return open_blocks <= closed_blocks

def repl():
    print("Welcome to CalcLang! Type your code below. Type 'exit' to quit.")
    interpreter = Interpreter()
    
    while True:
        try:
            code = input("CalcLang> ")
            if code.strip().lower() == 'exit':
                break
            if not code.strip():
                continue

            # Multi-line handling
            while not is_balanced(code):
                line = input("      ... ")
                code += " " + line

            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            if not tokens:
                continue

            parser = Parser(tokens)
            ast = parser.parse_program()
            
            interpreter.interpret(ast)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()