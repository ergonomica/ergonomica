#!/usr/bin/pythAon
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# pylint doesn't know where verbs.py is being imported
# pylint: disable=import-error

"""
[verbs.py]

Contains all the native commands for ergonomica
"""

import os
import fnmatch
import shutil

from lib.load.config import EDITOR

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
    """Changes to a directory"""
    if args[0][0] in ["~", "/"]:
        env.directory = args[0]
    else:
        env.directory += "/" + args[0]# + "/"
    os.chdir(env.directory)

verbs["cd"] = cd
verbs["directory"] = cd

def ls(env, args, kwargs):
    """List files in a directory."""
    if len(args) == 0:
        return os.listdir(env.directory)
    else:
        return os.listdir(args[0])

verbs["ls"] = ls
verbs["list"] = ls

def rm(env, args, kwargs):
    """Remove files."""
    map(lambda x: os.remove(env.directory + "/" + x), args)
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
    pattern = kwargs["name"]
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

def ergo_help(env, args, kwargs):
    """ergonomica help"""
    if args == []:
        for item in env.verbs:
            print "%-9s |  %29s" % (item, env.verbs[item].__doc__)
    else:
        for item in args:
            print env.verbs[item].__doc__

verbs["help"] = ergo_help
