# pylint: disable=W0603
"""
[verbs.py]
Contains all the native commands for ergonomica
"""
run = True

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
        }
