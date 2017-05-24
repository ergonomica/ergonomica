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
    'INDENT',
    'VARIABLE',
    'LBRACKET',
    'RBRACKET',
    'EVAL',
    'ESCAPE',
    'QUOTE',
)

t_ESCAPE = r'\\'
t_INDENT = r'[ ]{3}'
t_NEWLINE  = r'\n+'
t_PIPE = r'\|'
#t_ignore = ' \t'
t_LBRACKET = '\('
t_RBRACKET = '\)'
t_QUOTE = '"'

def t_LITERAL(t):
    r'[:\/\*A-Z\$\-a-z_\.,/~><\d{}]+'
    if t.value == "def":
        t.type = 'DEFINITION'
    elif t.value[0] == '$':
        t.type = 'EVAL'
        t.value = t.value[1:]
    return t

def t_ARGARRAY(t):
    r'\[.*?\]'
    t.value = t.value[1:-1].split()
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
            if in_quotes:
                in_quotes = False
                tokens[-1].value += '"'
            else:
                in_quotes = True
                tokens.append(lexer.token())
                tokens[-1].value = '"' + tokens[-1].value
            continue

        elif in_quotes:
            tokens[-1].value += " " + tok.value
        
        
        else:
            tokens.append(tok)
            
    return tokens
