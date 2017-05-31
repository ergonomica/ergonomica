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

try:
    HISTORY = FileHistory(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_history"))
except IOError as error:
    print("[ergo: ConfigError]: No such file ~/.ergo_history. Please run ergo_setup. " + str(error), file=sys.stderr)

    #return prompt_toolkit.prompt(unicode_(PROMPT), history=history, completer=ErgonomicaCompleter(verbs), multiline=True,key_bindings_registry=key_bindings_registry)
        
def prompt(env, ns):

    key_bindings_registry = manager_for_environment(env).registry
    return prompt_toolkit.prompt(env.get_prompt(), multiline=True, completer=ErgonomicaCompleter(ns), history=HISTORY, auto_suggest=AutoSuggestFromHistory(), key_bindings_registry=key_bindings_registry)
