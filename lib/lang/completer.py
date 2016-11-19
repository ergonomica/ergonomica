from lib.verbs import verbs

def completer(text, state):
    options = [i for i in verbs.verbs if i.startswith(text)]
    #print options
    #try:
    if state > 2:
        return None
    if options != []:# len(options):
        return options[0]
    else:
        return None
