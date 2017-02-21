"""
[lib/lang/ergo2bash.py]

Ergonomica to Bash syntax converter.
"""

from lib.lang.parser import tokenize

def ergo2bash(string):
    tokens = tokenize(string)
    command = tokens[0][0]
    args = " ".join(tokens[0][1:])
    switches = tokens[1]
    bash_switches = ""
    for item in switches:
        name, val = item.split(":", 1)
        if val in ["t", "true"]:
            bash_switches += " -%s " % name
        else:
            bash_switches += " -%s %s" % (name, val)
    return "%s %s %s" % (command, args, bash_switches)
