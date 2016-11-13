<<<<<<< HEAD
# pylint: disable=W0603
"""
[verbs.py]
Contains all the native commands for ergonomica
"""
=======
"""
[verbs.py]
"""

import os
import fnmatch

>>>>>>> 92b1fee3050360d8d43e495c4dbbdddddda5074f
run = True
directory = ""

<<<<<<< HEAD
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

verbs = {"yes" : yes,

         "quit": Quit,
         "exit": Quit,

         "help": Help,
=======
def yes(args, kwargs):
    return "y"

#def cd(*args, **kwargs):
#    directory =


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
>>>>>>> 92b1fee3050360d8d43e495c4dbbdddddda5074f
        }
