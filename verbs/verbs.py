"""
[verbs.py]
"""

import os
import fnmatch

run = True
directory = ""

def yes(args, kwargs):
    return "y"

def cd(*args, **kwargs):
    directory = args[0]

def quit(*args, **kwargs):
    global run
    run = False

def find(args, kwargs):
    pattern = kwargs["name"]
    path = args[0]
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def clear(args, kwargs):
    os.system('clear')

verbs = {"yes" : yes,
         "quit": quit,
         "find": find,
         "clear":clear,
        }
