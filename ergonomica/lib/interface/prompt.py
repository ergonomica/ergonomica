#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/interface/prompt.py]

The Ergonomica interface handler. Defines the prompt function.
"""

from __future__ import print_function

import sys
import os.path

import prompt_toolkit
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from ergonomica.lib.interface.completer import ErgonomicaCompleter
from ergonomica.lib.interface.key_bindings_manager import load_key_bindings
from prompt_toolkit.styles import Style

try:
    HISTORY = FileHistory(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_history"))
except IOError as error:
    print("[ergo: ConfigError]: No such file ~/.ergo_history. Please run ergo_setup. "
          + str(error),
          file=sys.stderr)


style = Style.from_dict({
    'rprompt': 'bg:#ff0066 #ffffff',
    'toolbar': '#ffffff bg:#333333',
})


# this is the standard (namespace is ns) elsewhere
def prompt(env, ns): # pylint: disable=invalid-name
    """Get input from prompt_toolkit prompt."""
    key_bindings = load_key_bindings(env)

    if env.toolbar:
        # we need to seperate into conditionals otherwise the background for the toolbar will show up
        return prompt_toolkit.prompt(env.get_prompt(),
                                     multiline=True,
                                     completer=ErgonomicaCompleter(ns),
                                     history=HISTORY,
                                     auto_suggest=AutoSuggestFromHistory(),
                                     key_bindings=key_bindings,
    #                                 mouse_support=True,
                                     bottom_toolbar=lambda: [('class:toolbar', env.toolbar)],
                                     rprompt=lambda: [('', ' '), ('class:rprompt', env.rprompt)] if env.rprompt else [],
                                     style=style)
    else:
        # we need to seperate into conditionals otherwise the background for the toolbar will show up
        return prompt_toolkit.prompt(env.get_prompt(),
                                     multiline=True,
                                     completer=ErgonomicaCompleter(ns),
                                     history=HISTORY,
                                     auto_suggest=AutoSuggestFromHistory(),
                                     key_bindings=key_bindings,
    #                                 mouse_support=True,
                                     rprompt=lambda: [('', ' '), ('class:rprompt', env.rprompt)] if env.rprompt else [],
                                     style=style)
