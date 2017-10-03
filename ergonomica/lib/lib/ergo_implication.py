import os
import dill

def implication(events, functions):

    
    try:
        # load implications store
        implications = dill.load(open(os.path.expanduser('~/.ergo/.events')))
    except IOError:
        # initialize the implications as a blank dictionary.
        # if the file doesn't already exist, it will be dumped
        # with the new data created.
        implications = {}
        

        
    if not isinstance(events, list):
        events = [events]

    if not isinstance(functions, list):
        functions = [functions]

    for event in events:
        implications[event] = implications.get(event, []) + functions

        
    dill.dump(implications, open(os.path.join(os.path.expanduser('~'), '.ergo', '.events'), 'wb'))
        
    return
    

    
exports = {'implication': implication}
