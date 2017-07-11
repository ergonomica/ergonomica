#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/interface/completer.py]

The autocomplete engine for ergonomica.
"""

# for completing directory/filenames
import os
import re

from prompt_toolkit.completion import Completer, Completion
from ergonomica.lib.lang.tokenizer import tokenize

def get_arg_type(verbs, text):
    tokens = tokenize(text)
    argcount = 0
    for i in range(len(tokens))[:-1]:
        token = tokens[i]
        if (i == 0) or (tokens[i - 1].type == 'PIPE'):
            current_command = token.value
            argcount = len(tokens) - i
    
    # lookup and get docstring
    try:
        docstring = re.search(r'(Usage|usage):\n\s.*', verbs[current_command].__doc__).group().split("\n")[1].strip().split()
    except KeyError: # command not found
        return "<file>"
        
    parsed_docstring = []
    for item in docstring:
        if (parsed_docstring == []) or \
           ((parsed_docstring[-1].count('(') == parsed_docstring[-1].count(')')) and \
           (parsed_docstring[-1].count('[') == parsed_docstring[-1].count(')'))):
             parsed_docstring.append(item)
        
        else:
            parsed_docstring[-1] += item     

    try: return re.match(r'<[a-z]+?>', parsed_docstring[argcount - 1]).group()
    except AttributeError: return "<file>"
    except IndexError: return "<none>"


def complete(verbs, text):
    """
    Return a completion for a command or directory.
    """

    #print(get_arg_type(verbs, 'ls e'))

    verbs.update({'def': None})

    last_word = text.split(" ")[-1]


    fixed_text = text
    if text[-1] == " ":
        fixed_text += "a"

    if len(text.split(" ")) > 1:
        if get_arg_type(verbs, fixed_text) == "<none>":
            # aka no more arguments to supply to function
            options = []
        if get_arg_type(verbs, fixed_text) == "<file>":
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
                    options = [os.path.join(original_dirname, x) for x in os.listdir(dirname)]
                except OSError:
                    pass

        elif get_arg_type(verbs, fixed_text) == "<string>":
            options = [text.split(" ")[-1] + '"']
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
