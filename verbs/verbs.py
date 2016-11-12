"""
[verbs.py]
"""

run = True
directory = ""

def yes(*args, **kwargs):
    return "y"

#def cd(*args, **kwargs):
#    directory =


def quit(*args, **kwargs):
    global run
    run = False



verbs = {"yes" : yes,
         "quit": quit,
        }
