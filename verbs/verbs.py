# pylint: disable=W0603, C0325
"""
[verbs.py]

Contains all the native commands for ergonomica
"""

import os
import fnmatch
import shutil

run = True
directory = os.getcwd()
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

def cd(args, kwargs):
    """Changes to a directory"""
    global directory
    if args[0][0] in ["~", "/"]:
        directory = args[0]
    else:
        directory += args[0] + "/"
    os.chdir(directory)

verbs["cd"] = cd
verbs["directory"] = cd

def ls(args, kwargs):
    """List files in a directory."""
    if len(args) == 0:
        return os.listdir(directory)
    else:
        return os.listdir(args[0])

verbs["ls"] = ls
verbs["list"] = ls

def rm(args, kwargs):
    """Remove files."""
    map(lambda x: os.remove(directory + "/" + x), args)
    return

verbs["rm"] = rm
verbs["remove"] = rm

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

def mv(args, kwargs):
    """Move files."""
    for x in args:
        shutil.move(directory  + "/" + x, kwargs["path"])
    return

verbs["move"] = mv
verbs["mv"] = mv

def cp(args, kwargs):
    """Copy files."""
    for x in args:
        shutil.copy2(directory + "/" + x, kwargs["path"])
    return

verbs["copy"] = cp
verbs["cp"] = cp

def echo(args, kwargs):
    """Echos a phrase"""
    return args

verbs["echo"] = echo
verbs["print"] = echo

def clear(args, kwargs):
    """Clears the screen"""
    os.system('clear')

verbs["clear"] = clear

def Help(args, kwargs):
    """ergonomica help"""
    global verbs
    print(verbs)
    if args == []:
        for item in verbs:
            print(item + " : " + verbs[item].__doc__)
    else:
        for item in args:
            print(verbs[item].__doc__)

verbs["help"] = Help
