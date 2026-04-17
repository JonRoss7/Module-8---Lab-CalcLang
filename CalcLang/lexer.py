import re

keywords = {
    'if': 'IF', 'then': 'THEN', 'else': 'ELSE', 'end': 'END', 
    'def': 'DEF', 'print': 'PRINT', 'while': 'WHILE', 'do': 'DO',
    'return': 'RETURN'
}

token_regex = {
    'NUMBER': r'\d+(\.\d+)?',
    'ID': r'[a-zA-Z_]\w*',
    'EQ': r'==', 'GE': r'>=', 'LE': r'<=', 'NE': r'!=',
    'PLUS': r'\+', 'MINUS': r'-', 'MUL': r'\*', 'DIV': r'/',
    'GT': r'>', 'LT': r'<', 
    'LPAREN': r'\(', 'RPAREN': r'\)', 'COMMA': r',', 'ASSIGN': r'=',
}

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.code):
            match = None
            for token_type, pattern in token_regex.items():
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)
                if match:
                    value = match.group(0)
                    if token_type == 'ID' and value in keywords:
                        self.tokens.append((keywords[value], value))
                    else:
                        if token_type == 'NUMBER':
                            value = float(value)
                        self.tokens.append((token_type, value))
                    self.pos = match.end()
                    break
            
            if not match:
                if self.code[self.pos].isspace():
                    self.pos += 1
                    continue
                raise SyntaxError(f"Unexpected character: {self.code[self.pos]}")
                
        return self.tokens