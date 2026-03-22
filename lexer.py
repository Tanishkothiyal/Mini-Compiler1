import re

TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+'),
    ('ID',       r'[a-zA-Z_]\w*'),
    ('ASSIGN',   r'='),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MULT',     r'\*'),
    ('DIV',      r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('SEMICOLON',r';'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
]

token_regex = '|'.join(
    f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION
)

def tokenize(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind in ('SKIP', 'NEWLINE'):
            continue

        tokens.append((kind, value))

    return tokens