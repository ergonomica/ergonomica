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
    r'[\[\]\'=:\/\*A-Z\$\-a-z_\.,/~><\d{}]+'
    if t.value == "def":
        t.type = 'DEFINITION'
    elif t.value == "$":
        t.type = 'EVAL'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex(optimize=1)

def tokenize(string):

    """Returns a preprocessed list of tokens."""

    in_quotes = False
    cleaned_tokens = []
    last_token_type = None

    lexer.input(string)

    while True:
        tok = lexer.token()

        if not tok:
            break

        elif tok.type == 'QUOTE':
            if in_quotes:
                in_quotes = False
                #cleaned_tokens[-1].value += '"'
            else:
                in_quotes = True
                cleaned_tokens.append(lexer.token())
            continue

        elif in_quotes:
            if (tok.type == 'RBRACKET') or (last_token_type == 'LBRACKET'):
                cleaned_tokens[-1].value += tok.value
            else:
                cleaned_tokens[-1].value += " " + tok.value

        else:
            cleaned_tokens.append(tok)

        last_token_type = tok.type

    return cleaned_tokens
