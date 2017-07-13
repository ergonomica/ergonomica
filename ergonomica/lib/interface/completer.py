#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/interface/completer.py]

The autocomplete engine for ergonomica.
"""

# for completing directory/filenames
import os
import subprocess
import re

from prompt_toolkit.completion import Completer, Completion
from ergonomica.lib.lang.tokenizer import tokenize

def get_all_args_from_man(command):
    """
    Returns a dictionary mapping option->their descriptions
    """
    
    try:
        devnull = open(os.devnull, 'w')
        options = [x for x in subprocess.check_output(["man", command], stderr=devnull).replace("\x08", "").replace("\n\n", "{TEMP}").replace("\n", " ").replace("{TEMP}", "\n").split("\n") if x.startswith("     -")]
    except subprocess.CalledProcessError:
        return {}
        
    options = [re.sub("[ ]+", " ", x) for x in options]

    parsed_options = {}
    
    for i in options:
        parsed_options[i.strip().split(" ")[0][::2]] = " ".join(i.strip().split(" ")[1:])
    
    return parsed_options


def get_arg_type(verbs, text):
    """
    Get the type of the current argument to complete,
    given the buffer text and the verbs dictionary.
    """

    tokens = tokenize(text)
    argcount = 0
    for i in range(len(tokens))[:-1]:
        token = tokens[i]
        if (i == 0) or (tokens[i - 1].type == 'PIPE'):
            current_command = token.value
            argcount = len(tokens) - i

    # lookup and get docstring
    try:
        # regexp match
        docstring = re.search(r'(Usage|usage):\n\s.*', verbs[current_command].__doc__).group()

        # preprocess
        docstring = docstring.split("\n")[1].strip().split()
    except TypeError: # empty buffer
        return "<file/directory>"
    except KeyError: # no such command
        return ("<file/directory>", get_all_args_from_man(current_command))

    parsed_docstring = []
    for item in docstring:
        if (parsed_docstring == []) or \
           ((parsed_docstring[-1].count('(') == parsed_docstring[-1].count(')')) and \
           (parsed_docstring[-1].count('[') == parsed_docstring[-1].count(')'))):
            parsed_docstring.append(item)

        else:
            parsed_docstring[-1] += item

    try:
        return re.match(r'<[a-z]+?>', parsed_docstring[argcount - 1]).group()
    except AttributeError:
        return "<file>"
    except IndexError:
        return "<none>"


def complete(verbs, text):
    """
    Return a completion for a command or directory.
    """

    verbs.update({'def': None})

    last_word = text.strip().split(" ")[-1]

    fixed_text = text
    if text.endswith(" "):
        fixed_text += "a"

    options = []
    cli_options = False
    meta = {}
    
        
    if len(text.split(" ")) > 1:
        argtype = get_arg_type(verbs, fixed_text)

        if isinstance(argtype, tuple):
            (argtype, meta) = argtype
            cli_options = [x for x in meta]

        if argtype == "<none>":
            # aka no more arguments to supply to function
            pass

        elif argtype == "<variable>":
            options = [x for x in verbs.keys() if not hasattr(verbs[x], "__call__")]

        elif argtype in ["<file>", "<directory>", "<file/directory>"]:
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
                    options += [os.path.join(original_dirname, x) for x in os.listdir(dirname)]
                except OSError:
                    pass

            if argtype == "<file>":
                options = [x for x in options if os.path.isfile(x)]
            elif argtype == "<directory>":
                options = [x for x in options if os.path.isdir(x)]

        elif get_arg_type(verbs, fixed_text) == "<string>":
            options = [text.split(" ")[-1] + '"']
    else:
        options = [x for x in verbs.keys() if hasattr(verbs[x], "__call__")]

    if cli_options:
        options += cli_options

    options = [i for i in options if i.startswith(last_word)]
    if options == []:
        if text.endswith("/"):
            try:
                options = os.listdir(last_word)
            except OSError:
                options = []
            return ([(0, option) for option in options], meta)
    if options != []:
        return ([(len(last_word), i) for i in options], meta)
    return ([], {})


class ErgonomicaCompleter(Completer):
    """
    Ergonomica subset of the Completer class.
    This handles all Ergonomica completion (using its syntax).
    """

    verbs = {}

    def __init__(self, verbs):
        self.verbs = verbs

    def get_completions(self, document, complete_event):
        completions = complete(self.verbs, document.text)
        for result in completions[0]:

            start_point = result[0]

            # check if there's a space that needs to be escaped
            if " " in result[1]:
                text = '"%s"' % (result[1])
            else:
                text = result[1]

            yield Completion(text, start_position=-start_point, display_meta=completions[1].get(text, ''))
