# lextab.py. This file automatically created by PLY (version 3.10). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('COMMENT', 'DEFINITION', 'END', 'STRING', 'INT', 'NEWLINE', 'PIPE', 'LITERAL', 'ARGARRAY', 'SUBSTITUTION'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_SUBSTITUTION>\\$\\d+)|(?P<t_LITERAL>[a-z_\\./~]+)|(?P<t_ARGARRAY>\\[.*?\\])|(?P<t_STRING>".*")|(?P<t_INT>\\d+)|(?P<t_COMMENT>\\#.*)|(?P<t_NEWLINE>\\n+)|(?P<t_PIPE>->)', [None, ('t_SUBSTITUTION', 'SUBSTITUTION'), ('t_LITERAL', 'LITERAL'), ('t_ARGARRAY', 'ARGARRAY'), ('t_STRING', 'STRING'), ('t_INT', 'INT'), ('t_COMMENT', 'COMMENT'), (None, 'NEWLINE'), (None, 'PIPE')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
