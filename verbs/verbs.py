# pylint: disable=W0603
"""
[verbs.py]
Contains all the native commands for ergonomica
"""

import os
import fnmatch

run = True
directory = ""

def yes(*args, **kwargs):
    """
     Returns a 'y'
    """
    return "y"

def Quit(*args, **kwargs):
    """What do you think?"""
    global run
    run = False

def Help(*args):
    """Display all commands"""
    if len(args[0]) == 0:
        print "test"
    else:
        print args

def yes(*args, **kwargs):
    return "y"

#def cd(*args, **kwargs):
#    directory =


def Quit(*args, **kwargs):
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
    """Clears the screen"""
    os.system('clear')

verbs = {"yes" : yes,

         "quit": Quit,
         "exit": Quit,

         "find": find,
         "clear":clear,
        }
