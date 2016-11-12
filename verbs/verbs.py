run = True

def yes(*args, **kwargs):
    return "y"

def quit(*args, **kwargs):
    global run
    run = False

verbs = {"yes" : yes,
            "quit": quit,
           }

