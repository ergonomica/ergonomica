#!/usr/bin/pythonAA
# -*- coding: utf-8 -*-

# global statements are good here
# pylint: disable=global-statement

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[verbs.py]

Contains all the native commands for ergonomica
"""

import os
import fnmatch
import shutil

from lib.load.config import EDITOR

run = True
directory = os.getcwd()
user = os.getenv("USER")
home = os.getenv(key="HOME")
verbs = {}
namespace = {}

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
        directory += "/" + args[0]# + "/"
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

def mkdir(args, kwargs):
    """Create a directory."""
    for arg in args:
        try:
            os.mkdir(directory + "/" + arg)
        except OSError:
            pass
    return

verbs["mkdir"] = mkdir

def find(args, kwargs):
    """Finds a file with a pattern"""
    pattern = kwargs["name"]
    try:
        path = args[0]
    except IndexError:
        path = directory
    result = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if fnmatch.fnmatch(os.path.join(root, dir), pattern):
                result.append(os.path.join(root, dir))
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return list(set(result))

verbs["find"] = find

def mv(args, kwargs):
    """Move files."""
    for i in range(0, len(args) - 1):
        try:
            shutil.move(directory + "/" + args[i], directory + "/" + args[i+1])
        except OSError:
            pass
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

def _set(args, kwargs):
    """set the value of a variable"""
    for key in kwargs:
        namespace[key] = kwargs[key]
    return

verbs["set"] = _set
verbs["def"] = _set
verbs["var"] = _set

def get(args, kwargs):
    """get the value of a variable"""
    return [namespace[x] for x in args]

verbs["get"] = get
verbs["val"] = get

def edit(args, kwargs):
    """ """
    os.system(EDITOR + " " + " ".join(args))

verbs["edit"] = edit
    
def ergo_help(args, kwargs):
    """ergonomica help"""
    global verbs
    if args == []:
        for item in verbs:
            print "%-9s |  %29s" % (item, verbs[item].__doc__)
    else:
        for item in args:
            print verbs[item].__doc__

verbs["help"] = ergo_help

