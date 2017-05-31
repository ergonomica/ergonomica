#!/usr/bin/python
# -*- coding: utf-8 -*-

# py lex-yacc standards aren't pylint-friendly
# pylint: disable=invalid-name

# not all PLY functions are supposed to have docstrings (would mess with parsing)
# pylint: disable=missing-docstring

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
t_NEWLINE = r'[\n+;]+'
t_PIPE = r'\|'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_QUOTE = r'"'

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

    """Returns a preprocessed list of tokens."""

    in_quotes = False
    cleaned_tokens = []

    lexer.input(string)

    while True:
        tok = lexer.token()

        if not tok:
            break

        elif tok.type == 'QUOTE':
            if in_quotes:
                in_quotes = False
                cleaned_tokens[-1].value += '"'
            else:
                in_quotes = True
                cleaned_tokens.append(lexer.token())
                cleaned_tokens[-1].value = '"' + cleaned_tokens[-1].value
            continue

        elif in_quotes:
            cleaned_tokens[-1].value += " " + tok.value


        else:
            cleaned_tokens.append(tok)

    return cleaned_tokens
