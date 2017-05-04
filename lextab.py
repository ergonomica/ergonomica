# lextab.py. This file automatically created by PLY (version 3.10). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('COMMENT', 'STRING', 'INT', 'PIPE', 'COMMAND', 'ARG_INSERT'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_newline>\\n+)|(?P<t_STRING>".*")|(?P<t_INT>\\d+)|(?P<t_COMMENT>\\#.*)|(?P<t_COMMAND>[a-z_]+)|(?P<t_PIPE>->)', [None, ('t_newline', 'newline'), ('t_STRING', 'STRING'), ('t_INT', 'INT'), ('t_COMMENT', 'COMMENT'), (None, 'COMMAND'), (None, 'PIPE')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
