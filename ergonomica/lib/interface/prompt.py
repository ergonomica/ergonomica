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

# this is the standard (namespace is ns) elsewhere
def prompt(env, ns): # pylint: disable=invalid-name
    """Get input from prompt_toolkit prompt."""
    key_bindings_registry = manager_for_environment(env).registry
    return prompt_toolkit.prompt(env.get_prompt(),
                                 multiline=True,
                                 completer=ErgonomicaCompleter(ns),
                                 history=HISTORY,
                                 auto_suggest=AutoSuggestFromHistory(),
                                 key_bindings_registry=key_bindings_registry,
                                 mouse_support=True
                                 # get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
#                                  style=style)
                                 )
