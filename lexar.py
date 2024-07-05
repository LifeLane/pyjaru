import re

def lexer(code):
    token_specification = [
        ('NUMBER',   r'\d+'),
        ('IDENT',    r'[A-Za-z_]\w*'),
        ('ASSIGN',   r'='),
        ('PRINT',    r'print'),
        ('IF',       r'if'),
        ('WHILE',    r'while'),
        ('DEF',      r'def'),
        ('CLASS',    r'class'),
        ('NEW',      r'new'),
        ('EQ',       r'=='),
        ('NE',       r'!='),
        ('LT',       r'<'),
        ('GT',       r'>'),
        ('LE',       r'<='),
        ('GE',       r'>='),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('LBRACE',   r'\{'),
        ('RBRACE',   r'\}'),
        ('LBRACK',   r'\['),
        ('RBRACK',   r'\]'),
        ('COLON',    r':'),
        ('PLUS',     r'\+'),
        ('MINUS',    r'-'),
        ('TIMES',    r'\*'),
        ('DIVIDE',   r'/'),
        ('SEMI',     r';'),
        ('COMMA',    r','),
        ('DOT',      r'\.'),
        ('SKIP',     r'[ \t\n]+'), # Skip spaces, tabs, and newlines
        ('MISMATCH', r'.')         # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value} unexpected')
        tokens.append((kind, value))
    return tokens
