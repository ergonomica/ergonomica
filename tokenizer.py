#
# [lexer.py]
#
# The lexer for Ergonomica.
#

import ply.lex as lex

tokens = (
    'ARGARRAY',
    'LITERAL',
    'PIPE',
    'INT',
    'STRING',
    'COMMENT',
    'END',
    'NEWLINE',
)

t_NEWLINE  = r'\n+'
t_PIPE = r'->'
t_LITERAL = r'[a-z]+'
t_ignore = ' \t'
t_END = "end"

def t_ARGARRAY(t):
    r'\[.*?\]'
    t.value = t.value[1:-1].split()
    return t
    
def t_STRING(t):
    r'".*"'
    t.value = t.value[1:-1]
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):

    print(t.value)
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(string):

    tokens = []
    lexer.input(string)
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens
    
