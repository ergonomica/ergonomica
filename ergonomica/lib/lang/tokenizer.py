#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lexer.py]

The lexer for Ergonomica.
"""

import ply.lex as lex

tokens = (
    'ARGARRAY',
    'LITERAL',
    'PIPE',
    'STRING',
    'COMMENT',
    'NEWLINE',
    'DEFINITION',
    'END',
    'VARIABLE',
    'QUOTE',
    'LBRACKET',
    'RBRACKET',
)

t_NEWLINE  = r'\n+'
t_PIPE = r'\|'
t_ignore = ' \t'
t_QUOTE = '"'
t_LBRACKET = '\('
t_RBRACKET = '\)'

def t_LITERAL(t):
    r'[A-Z$\-a-z_\.,/~><\d{}]+'
    if t.value == "def":
        t.type = 'DEFINITION'
    elif t.value == "end":
        t.type = 'END'
    elif t.value[0] == '$':
        t.type = 'VARIABLE'
        t.value = t.value[1:]
    return t

def t_ARGARRAY(t):
    r'\[.*?\]'
    t.value = t.value[1:-1].split()
    return t
    
def t_STRING(t):
    r'".*"'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(string):

    in_quotes = False
    tokens = []
    lexer.input(string)
    while True:
        tok = lexer.token()

        if not tok:
            break
        
        elif tok.type == 'QUOTE':
            in_quotes = not in_quotes
            tokens.append(tok)

        elif in_quotes:
            tokens[-1] += tok.value

        else:
            tokens.append(tok)

    return tokens
