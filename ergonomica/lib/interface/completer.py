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
from ergonomica.lib.lang.parser import parse, Symbol

def get_all_args_from_man(command):
    """
    Returns a dictionary mapping option->their descriptions
    """

    try:
        devnull = open(os.devnull, 'w')
        try:
            options = [x for x in subprocess.check_output(["man", command], stderr=devnull).decode().replace("\x08", "").replace("\n\n", "{TEMP}").replace("\n", " ").replace("{TEMP}", "\n").split("\n") if x.startswith("     -")]
        except OSError:
            return []
        except subprocess.CalledProcessError:
            try:
                options = [x for x in subprocess.check_output([command, "--help"], stderr=devnull).decode().replace("\x08", "").replace("\n\n", "{TEMP}").replace("\n", " ").replace("{TEMP}", "\n").split("\n") if x.startswith("     -")]
            except subprocess.CalledProcessError:
                return []
            except OSError:
                return []
            return []
    
        options = [re.sub("[ ]+", " ", x) for x in options]
    
        out = []
        for i in options:
            out.append((i.strip().split(" ")[0][::2], " ".join(i.strip().split(" ")[1:])))
    
        return out
    except:
        # TODO: clean this up. potentially take inspiration from Fish shell?
        # currently this is really buggy, and given the wide variety of manpage styles, having this break somebody's Ergonomica wouldn't be great.
        return {}

def get_arg_type(verbs, text):
    """
    Get the type of the current argument to complete,
    given the buffer text and the verbs dictionary.
    """
    
    if text[-1] == " ":
        text += "a"

    tokens = parse(tokenize(text))

    if text.endswith("(") or (len(tokens) == 0) or isinstance(tokens[-1], Symbol):
        return [("<function>", "")]

    for token in tokens[::-1]:
        if isinstance(token, Symbol):
            current_command = token

    argcount = 0
    for i in range(len(tokens))[::-1]:
        token = tokens[i]
        if (i == 0) or (isinstance(tokens[i - 1], list)):
            argcount = len(tokens)  - i
            
    # lookup and get docstring
    try:
        # regexp match
        docstrings = re.search(r'(Usage|usage):\n\s.*', verbs[current_command].__doc__).group()

        # preprocess
        docstrings = [x.strip().split() for x in docstrings.split("\n")[1:]]

    except AttributeError:
        return [("<file/directory>", "")]
    except TypeError: # empty buffer
        return [("<file/directory>", "")]
    except KeyError: # no such command        
        if os.name != "nt":
            return [("<file/directory>", "")] + get_all_args_from_man(current_command)
        else:
            return [("<file/directory>", "")]

    # we .split() the docstring which splits it by spaces--but this needs to be corrected
    # for individual elements that contain spaces, e.g. (-a | --address)
    # parsed_docstring contains the corrected list of arguments.
    parsed_docstrings = []
    for docstring in docstrings:
        parsed_docstrings.append([])
        for item in docstring:
            if (parsed_docstrings[-1] == []) or \
                ((parsed_docstrings[-1][-1].count('(') == parsed_docstrings[-1][-1].count(')')) and \
                (parsed_docstrings[-1][-1].count('[') == parsed_docstrings[-1][-1].count(']'))):
                parsed_docstrings[-1].append(item)

            else:
                parsed_docstrings[-1][-1] += item
    
    out = []
    for parsed_docstring in parsed_docstrings:
        try:
            preset_arg = re.match(r'[a-z]+', parsed_docstring[argcount - 1])
            if preset_arg and (preset_arg.group() == parsed_docstring[argcount - 1]):
                out.append((parsed_docstring[argcount - 1], ""))
            else:
                try:
                    out.append((re.match(r'<[a-z]+?>', parsed_docstring[argcount - 1]).group(), ""))
                except AttributeError:
                    # current argument doesn't have a declared type
                    out.append(("<file/directory>", ""))
                except IndexError:
                    # no argument
                    pass
        except IndexError:
            pass

    return out


def complete(verbs, text):
    """
    Return a completion for a command or directory.
    """

    verbs.update({"if": None,
                  "set": None,
                  "global": None,
                  "lambda": None,})
    
    fixed_text = text
    if text.endswith(" "):
        fixed_text += "a"
        last_word = ""
    
    last_word = tokenize(text)[-1]
        
    options = []
    meta = {}

    if True:#(["("] + tokenize(text))[-2] != "(":
        for argtype in get_arg_type(verbs, fixed_text):

            if argtype[1] != "":
                # aka there's a meta definition
                meta[argtype[0]] = argtype[1]
                
            if not (argtype[0].startswith("<") or argtype[0].endswith(">")):
                # then add it directory
                options.append(argtype[0])

            if argtype[0] == "<none>":
                # aka no more arguments to supply to function
                pass

            elif argtype[0] == "<variable>":
                options += [x for x in verbs.keys() if not hasattr(verbs[x], "__call__")] + ['def']

            elif argtype[0] in ["<file>", "<directory>", "<file/directory>"]:
                if os.path.basename(text) == text:
                    try:
                        options += os.listdir(".")
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

                if argtype[0] == "<file>":
                    options = [x for x in options if os.path.isfile(x)]
                elif argtype[0] == "<directory>":
                    options = [x for x in options if os.path.isdir(x)]

            elif argtype[0] == "<string>":
                options += [text.split(" ")[-1] + '"']        

            elif argtype[0] == "<function>":
                commands = [os.listdir(y) for y in os.environ['PATH'].split(os.pathsep)]
                flattened_commands = [x for l in commands for x in l]
                options = [x for x in verbs.keys() if hasattr(verbs[x], "__call__")] + flattened_commands

    if text.endswith(" "):
        last_word = ""

    if last_word == "(":
        last_word = ""
                
    if not text.endswith(" "):
        options = [i for i in options if i.startswith(last_word)]
        
    if options == []:
        if text.endswith("/"):
            try:
                options = os.listdir(last_word)
            except OSError:
                options = []
            return ([(len(last_word), option) for option in options], meta)
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
        try:
            completions, meta = complete(self.verbs, document.text)
            for completion in completions:
                yield Completion(completion[1], start_position=-completion[0], display_meta=meta.get(completion[1], ''))
        except Exception:
            pass
