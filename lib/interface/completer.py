"""
[lib/interface/completer.py]

"""

# for completing directory/filenames
import os

from lib.prompt_toolkit.completion import Completer, Completion


def complete(verbs, text):
    """Return a completion for a command or directory."""
    last_word = text.split(" ")[-1]
    if len(text.split(" ")) > 1:
        options = os.listdir(".")
    else:
        options = verbs.keys()
    options = [i for i in options if i.startswith(last_word)]
    if options == []:
        if text.endswith("/"):
            options = os.listdir(last_word)
            return [(0, option) for option in options]
    if options != []:
        return [(len(last_word), i) for i in options]
    return ""

class ErgonomicaCompleter(Completer):

    verbs = {}
    
    def __init__(self, verbs):
        self.verbs = verbs
    
    def get_completions(self, document, complete_event):
        for result in complete(self.verbs, document.text):
            start_point = result[0]
            text = result[1]
            yield Completion(text, start_position=-start_point)
