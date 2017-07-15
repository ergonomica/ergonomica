# lextab.py. This file automatically created by PLY (version 3.10). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('COMMENT', 'DEFINITION', 'INDENT', 'STRING', 'QUOTE', 'NEWLINE', 'LBRACKET', 'LITERAL', 'EVAL', 'ESCAPE', 'VARIABLE', 'RBRACKET', 'PIPE'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_LITERAL>[^\\n\\)\\(;" ]+)|(?P<t_COMMENT>\\#.*)|(?P<t_NEWLINE>[\\n+;]+)|(?P<t_INDENT>[ ]{3})|(?P<t_ESCAPE>\\\\)|(?P<t_RBRACKET>\\))|(?P<t_LBRACKET>\\()|(?P<t_QUOTE>")', [None, ('t_LITERAL', 'LITERAL'), ('t_COMMENT', 'COMMENT'), (None, 'NEWLINE'), (None, 'INDENT'), (None, 'ESCAPE'), (None, 'RBRACKET'), (None, 'LBRACKET'), (None, 'QUOTE')])]}
_lexstateignore = {'INITIAL': ''}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
