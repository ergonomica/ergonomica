#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/interface/prompt.py]

The Ergonomica interface handler. Defines the prompt function.
"""

from __future__ import print_function

import os
import sys
import prompt_toolkit
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from ergonomica.lib.interface.completer import ErgonomicaCompleter
from ergonomica.lib.interface.key_bindings_manager import manager_for_environment

from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

# def get_bottom_toolbar_tokens(cli):
#     return [(Token.Toolbar, ' This is a toolbar. ')]
#
# style = style_from_dict({
#     Token.Toolbar: '#ffffff bg:#333333',
# })

try:
    HISTORY = FileHistory(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_history"))
except IOError as error:
    print("[ergo: ConfigError]: No such file ~/.ergo_history. Please run ergo_setup. "
          + str(error),
          file=sys.stderr)

from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

def get_bottom_toolbar_tokens(cli):
    return [(Token.Toolbar, ' This is a toolbar. ')]

def get_rprompt_tokens(cli):
    return [(Token, ' '), (Token.RPrompt, '<rprompt>')]

style = style_from_dict({
    Token.RPrompt: 'bg:#ff0066 #ffffff',
    Token.Toolbar: '#ffffff bg:#333333',
})


# this is the standard (namespace is ns) elsewhere
def prompt(env, ns): # pylint: disable=invalid-name
    """Get input from prompt_toolkit prompt."""
    key_bindings_registry = manager_for_environment(env).registry
    if env.toolbar:
        # we need to seperate into conditionals otherwise the background for the toolbar will show up
        return prompt_toolkit.prompt(env.get_prompt(),
                                     multiline=True,
                                     completer=ErgonomicaCompleter(ns),
                                     history=HISTORY,
                                     auto_suggest=AutoSuggestFromHistory(),
                                     key_bindings_registry=key_bindings_registry,
    #                                 mouse_support=True,
                                     get_bottom_toolbar_tokens=lambda cli: [(Token.Toolbar, env.toolbar)],
                                     get_rprompt_tokens=lambda cli: [(Token, ' '), (Token.RPrompt, env.rprompt)] if env.rprompt else [],
                                     style=style)
    else:
        # we need to seperate into conditionals otherwise the background for the toolbar will show up
        return prompt_toolkit.prompt(env.get_prompt(),
                                     multiline=True,
                                     completer=ErgonomicaCompleter(ns),
                                     history=HISTORY,
                                     auto_suggest=AutoSuggestFromHistory(),
                                     key_bindings_registry=key_bindings_registry,
    #                                 mouse_support=True,
                                     get_rprompt_tokens=lambda cli: [(Token, ' '), (Token.RPrompt, env.rprompt)] if env.rprompt else [],
                                     style=style)
