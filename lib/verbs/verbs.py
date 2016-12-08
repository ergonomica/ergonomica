#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# pylint doesn't know where verbs.py is being imported
# pylint: disable=import-error

# default positional arguments are used for parsing
# pylint: disable=unused-argument

# list comprehension used for map/lambda operations
# pylint: disable=expression-not-assigned

"""
[lib/verbs/verbs.py]

Contains all the native commands for ergonomica
"""

import os
import fnmatch
import shutil
import sys
import code

from lib.lang.error import ErgonomicaError

verbs = {}

def yes(env, args, kwargs):
    """Returns a 'y'."""
    return ["y"]

verbs["yes"] = yes

def Quit(env, args, kwargs):
    """Quits the ergonomica shell."""
    env.run = False

verbs["quit"] = Quit
verbs["exit"] = Quit

def cd(env, args, kwargs):
    """Changes to a directory."""
    try:
        if args[0][0] in ["~", "/"]:
            os.chdir(args[0])
        else:
            os.chdir(env.directory + "/" + args[0])
        env.directory = os.getcwd()
    except OSError:
        raise ErgonomicaError("[ergo: NoSuchDirectoryError]: no such directory '%s'.")

verbs["cd"] = cd
verbs["directory"] = cd

def ls(env, args, kwargs):
    """List files in a directory."""
    if len(args) > 1:
        return [ls(env, x, kwargs) for x in args]
    try:
        if len(args) == 0:
            return os.listdir(env.directory)
        return os.listdir(env.directory)
    except OSError:
        raise ErgonomicaError("[ergo: NoSuchDirectoryError] No such file/directory '%s'.")

verbs["ls"] = ls
verbs["list"] = ls

def rm(env, args, kwargs):
    """Remove files."""
    try:
        [os.remove(env.directory + "/" + x) for x in args]
    except OSError:
        raise ErgonomicaError("")
    return

verbs["rm"] = rm
verbs["remove"] = rm

def mkdir(env, args, kwargs):
    """Create a directory."""
    for arg in args:
        try:
            os.mkdir(env.directory + "/" + arg)
        except OSError:
            pass
    return

verbs["mkdir"] = mkdir

def find(env, args, kwargs):
    """Finds a file with a pattern"""
    try:
        pattern = kwargs["name"]
    except KeyError:
        pattern = "*"
    try:
        path = args[0]
    except IndexError:
        path = env.directory
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

def mv(env, args, kwargs):
    """Move files."""
    for i in range(0, len(args) - 1):
        try:
            shutil.move(env.directory + "/" + args[i], env.directory + "/" + args[i+1])
        except OSError:
            pass
    return

verbs["move"] = mv
verbs["mv"] = mv

def cp(env, args, kwargs):
    """Copy files."""
    for x in args:
        shutil.copy2(env.directory + "/" + x, kwargs["path"])
    return

verbs["copy"] = cp
verbs["cp"] = cp

def echo(env, args, kwargs):
    """Prints its input."""
    return args

verbs["echo"] = echo
verbs["print"] = echo

def clear(env, args, kwargs):
    """Clears the screen."""
    os.system('clear')

verbs["clear"] = clear

def _set(env, args, kwargs):
    """set the value of a variable."""
    for key in kwargs:
        env.namespace[key] = kwargs[key]
    return

verbs["set"] = _set
verbs["def"] = _set
verbs["var"] = _set

def get(env, args, kwargs):
    """get the value of a variable"""
    return [env.namespace[x] for x in args]

verbs["get"] = get
verbs["val"] = get

def edit(env, args, kwargs):
    """Edit a file."""
    os.system(env.EDITOR + " " + " ".join(args))

verbs["edit"] = edit

def whoami(env, args, kwargs):
    """Return the user."""
    return env.user

verbs["whoami"] = whoami

def pwd(env, args, kwargs):
    """Print the working directory."""
    return env.directory

verbs["pwd"] = pwd

def version(env, args, kwargs):
    """Return ergonomica version information."""
    # &&&VERSION&&& replaced by Homebrew to the current version.
    return "Ergonomica &&&VERSION&&&."

verbs["version"] = version

def console_exit():
    raise SystemExit

def read(env, args, kwargs):
    """Read a file."""
    return [item for sublist in [open(x, "r").read().split("\n") for x in args] for item in sublist]
    
verbs["read"] = read
verbs["cat"] = read

def python(env, args, kwargs):
    """Drop into a python REPL."""
    temp_space = {}
    try:
        temp_space = globals()
        temp_space.update({"exit":sys.exit})
        temp_space.update({"quit":sys.exit})
        temp_space.update(env.namespace)
        code.InteractiveConsole(locals=temp_space).interact()
    except SystemExit:
        for key in temp_space:
            env.namespace[key] = temp_space[key]
        return ""


verbs["python"] = python

def bash(env, args, kwargs):
    """Open a bash shell."""
    os.system("bash")
    return

verbs["bash"] = bash

def fish(env, args, kwargs):
    """Open a fish shell."""
    os.system("fish")
    return

verbs["fish"] = fish

def zsh(env, args, kwargs):
    """Open a zsh shell."""
    os.system("zsh")
    return

verbs["zsh"] = zsh

def ergo_help(env, args, kwargs):
    """ergonomica help"""
    out = ""
    if args == []:
        for item in verbs:
            out += "%-9s |  %29s\n" % (item, verbs[item].__doc__)
    else:
        for item in args:
            out += verbs[item].__doc__ + "\n"
    return out

verbs["help"] = ergo_help
