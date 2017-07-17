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
    'QUOTE',
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
    'PIPE',
    'LITERAL',
)

t_ESCAPE = r'\\'
t_NEWLINE = r'[\n+;]+'
#t_PIPE = r'\|'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_QUOTE = r'"'

def t_LITERAL(t):
    r'[^\n\)\(;" ]+'
    if t.value == "def":
        t.type = 'DEFINITION'
    elif t.value == "$":
        t.type = 'EVAL'
    elif t.value == "|":
        t.type = "PIPE"
    return t

    #r'[\[\]\'=:\/\*A-Z\$\-a-z_\.,/~><\d{}]+'

t_INDENT = r'[ ]{3}'

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex(optimize=1)

def tokenize(string):
    """
    Returns a preprocessed list of tokens.
    """

    in_quotes = False
    cleaned_tokens = []
    last_token_type = None  # there isn't just a `last_token` object to read attributes from because that 
    last_token_value = None # would throw an AttributeError

    lexer.input(string)

    while True:
        tok = lexer.token()

        if not tok:
            break

        elif tok.type == 'QUOTE':
            if in_quotes:
                if last_token_value.endswith("\\"):
                    cleaned_tokens[-1].value += '\\"'
                else:
                    cleaned_tokens[-1].value += '"'
                    in_quotes = False
            else:
                in_quotes = True
                cleaned_tokens.append(tok)
                cleaned_tokens[-1].type = 'LITERAL'
                cleaned_tokens[-1].value = '"'
                last_token_value = tok.value
            continue

        elif in_quotes:
            if (tok.type == 'RBRACKET') or (last_token_type == 'LBRACKET'):
                cleaned_tokens[-1].value += tok.value
            else:
                if cleaned_tokens[-1].value not in ["", '"']:
                    cleaned_tokens[-1].value += " "
                
                cleaned_tokens[-1].value += tok.value

        else:
            cleaned_tokens.append(tok)

        last_token_type = tok.type
        last_token_value = tok.value

    return cleaned_tokens
