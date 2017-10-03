import pickle

def implication(events, functions):

    # load implications store
    implications = pickle.load(open(os.path.expanduser('~/.ergo/.events')))

    if not isinstance(events, list):
        events = [events]

    if not isinstance(functions, list):
        functions = [functions]

    for event in events:
        implications[event] = implications.get(event, []) + functions

    return
    

    
        
