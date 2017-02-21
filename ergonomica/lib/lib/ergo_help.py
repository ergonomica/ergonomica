#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/ergo_help.py]

Defines the "ergo_help" command.
"""

from lib.lang.error import ErgonomicaError
from lib.globalization.globalization import globalization_query

verbs = {}

def ergo_help(env, args, kwargs):
    """[COMMAND,...]@Display all ergonomica commands. If COMMANDs specified, returns the docstrings and arguments for them."""
    out = ""
    if args == []:
        return globalization_query("help_welcome_message", env.LANG)
    for arg in args:

        if arg == "syntax":
            out += """In Ergonomica, commands are of the form

            command arg1 arg2,... {kwarg1:val1,kwarg2:val2,...}

For example, finding all files in the root directory that match the regular expression 'e.*o':

            find / {name:e.*o}

Note that you can call a command by the first three letters of its name. For example, instead of

            edit important_code.py

you can type

           edi important_code.py

If a command is not defined in Ergonomica, ergonomica will fallback to BASH (but with Ergonomica syntax). Arguments are the same. If a flag requires a value (like -f file), there will be a kwarg with that flag that takes that value. If it does not require a value, simply supply 't' or 'true' for the value. For example, the command

            git commit --interactive -m "Making the world a better place"

The Ergonomica equivalent for this command would be
            
            git commit {-interactive:t,m:"Making the world a better place"}

            or

            git commit {-interactive:true,m:"Making the world a better place"}

To "pipe" in Ergonomica, one uses the '->' symbol. Commands may be put together as a chain

            command1 -> command2 -> command3

The last command in the chain will have its output printed. Each command outputs "args", and certain operators (defined later) allow for piping of kwargs. To make a command accept the arguments from the last command, one uses --arg as one of the arguments. For example, to list all files and remove them, one would run

            ls -> rm --arg

(analagous to)

            rm file1.txt file2.mp3,...

To accept kwargs, one uses --kw.
To process pipes of arguments, there are "operators", denoted by parenthases, e.g.,

            (filter) x.endswith(".py")

The available operators are:
(map) python_expression: applies a python expression to each argument. For example,

            ls -> (map) x + ' is on my computer.'
            # adds ' is on my computer' to each directory listing

(filter) python_expression: returns all arguments such that python_expression is true. For example,

            ifconfig -> (match) .*broadcast.*
            # shows lines that contain "broadcast" in ifconfig (ip address on wifi cards)

(match) regular_expression: returns all arguments that match regexp regular_expression. For example,

           ls -> (match) .*\.py
           # display all .py files
            
(reverse): reverses all arguments
(splice): splice arguments from last and current pipes. For example,
       
           echo a b -> echo c d -> (splice)
           # returns a c b d

(split): splits all arguments by spaces and flattens list

           echo "hello world" -> (splice)
           # returns hello world

(kw): sets each first argument to the value of the second in kwargs. For example,

          echo a 2 b 3 -> (kw) -> set --kw
          # sets a to 2 and b to 3\n\n"""

        elif arg == "commands":
            pruned_verbs = {}
            for item in env.verbs:
                if item not in pruned_verbs:
                    pruned_verbs[item] = env.verbs[item]
            for item in pruned_verbs:
                docstring = env.verbs[item].__doc__.split("@")
                out += "%-36s |  %29s\n" % (item + " " + docstring[0], docstring[1])

        elif arg in env.verbs:
            docstring = env.verbs[arg].__doc__.split("@")
            out += "%-26s |  %29s\n" % (arg + " " + docstring[0], docstring[1])
        else:
            print("arg is", arg)
            raise ErgonomicaError("[ergo: HelpError]: No such help directive '%s'." % (arg))
    return out + "\nVisit https://github.com/ergonomica/ergonomica/wiki for more documentation."

verbs["help"] = ergo_help
