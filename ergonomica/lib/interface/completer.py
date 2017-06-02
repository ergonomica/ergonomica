#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/interface/completer.py]

The autocomplete engine for ergonomica.
"""

# for completing directory/filenames
import os

from prompt_toolkit.completion import Completer, Completion


def complete(verbs, text):
    """Return a completion for a command or directory."""
    last_word = text.split(" ")[-1]
    if len(text.split(" ")) > 1:
        options = []
        if os.path.basename(text) == text:
            try:
                options = os.listdir(".")
            except OSError:
                pass
        else:
            dirname = os.path.dirname(text.split(" ")[1])
            original_dirname = dirname

            # process dirname
            if not dirname.startswith("/"):
                if dirname.startswith("~"):
                    dirname = os.path.expanduser(dirname)
                else:
                    dirname = "./" + dirname
            try:
                options = [original_dirname + "/" + x for x in os.listdir(dirname)]
            except OSError:
                pass
    else:
        options = verbs.keys()
    options = [i for i in options if i.startswith(last_word)]
    if options == []:
        if text.endswith("/"):
            try:
                options = os.listdir(last_word)
            except OSError:
                options = []
            return [(0, option) for option in options]
    if options != []:
        return [(len(last_word), i) for i in options]
    return ""


class ErgonomicaCompleter(Completer):
    """
    Ergonomica subset of the Completer class.
    This handles all Ergonomica completion (using its syntax).
    """

    verbs = {}

    def __init__(self, verbs):
        self.verbs = verbs

    def get_completions(self, document, complete_event):
        for result in complete(self.verbs, document.text):

            start_point = result[0]

            # check if there's a space that needs to be escaped
            if " " in result[1]:
                text = '"%s"' % (result[1])
            else:
                text = result[1]

            yield Completion(text, start_position=-start_point)
