# pylint: disable=W0603
"""
[verbs.py]

Contains all the native commands for ergonomica
"""

import os
import fnmatch

run = True
directory = "/"
user = os.getenv("USER")
home = os.getenv(key="HOME")

verbs = {}

def yes(args, kwargs):
    """Returns a 'y'."""
    return ["y"]

verbs["yes"] = yes

def Quit(args, kwargs):
    """Quits the ergonomica shell."""
    global run
    run = False

verbs["quit"] = Quit
verbs["exit"] = Quit

def Help(args):
    """Display all commands"""
    if len(args[0]) == 0:
        print "test"
    else:
        print args

verbs["help"] = Help

def cd(args, kwargs):
    """Changes to a directory"""
    global directory
    if args[0][0] in ["~", "/"]:
        directory = args[0]
    else:
        directory += args[0] + "/"
        
verbs["cd"] = cd

def ls(args, kwargs):
    """List files in a directory."""
    if len(args) == 0:
        return os.listdir(directory)
    else:
        return os.listdir(args[0])

verbs["ls"] = ls
    
def rm(args, kwargs):
    """Remove files."""
    map(lambda x: os.remove(directory + "/" + x), args)
    return

verbs["rm"] = rm

def find(args, kwargs):
    """Finds a file with a pattern"""
    pattern = kwargs["name"]
    path = args[0]
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

verbs["find"] = find

def echo(args, kwargs):
    """Echos a phrase"""
    return args

verbs["echo"] = echo
verbs["print"] = echo

def clear(args, kwargs):
    """Clears the screen"""
    os.system('clear')

verbs["clear"] = clear
