# pylint: disable W0603
import os
"""
[verbs.py]
Contains all the native commands for ergonomica
"""
run = True

def yes(*args, **kwargs):
    """Returns a 'y'"""
    return "y"

def quit(*args, **kwargs):
    global run
    run = False

def no(*args, **kwargs):
    return "n"

def find(*args, **kwargs):
    path = "Desktop/" 
    name = args[0]
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

verbs = {"yes" : yes,
         "quit": quit,
         "no" : no,
         "find":find,
           }
