"""
[lib/lang/arguments.py]

The Ergonomica arguments handler. Creates the ArgumentsContainer object.
"""

import re
from docopt import docopt

class ArgumentsContainer:
    
    def __init__(self, env, ns, stdin, args):            
        self.env, self.ns, self.stdin, self.args = env, ns, stdin, args
        
def get_typed_args(docstring, argv):
    # remove function description
    docstring = docstring.split("@")[0]
    
    # remove all type declarations
    docstring = re.sub("<.*?>", '', docstring)

    # read in docopt arguments
    d_parsed = docopt("usage: function " + docstring, argv=argv)
        
    # perform type modifications
    for item in re.findall("<[a-z]+>[A-Z]+", docstring):
        item = item[1:]
        _type, variable = item.split(">")[0]
        if _type == "str":
            pass
        else:
            evalable = True
            try:
                evaled_var = eval(d_parsed[variable])
            except:
                evalable = False 
            if (type(evaled_var).__name__ == _type) and evalable:
                d_parsed[variable] = evaled_var
            else:
                print("[ergo: TypeError]: Error converting '%s' to type '%s'.")

    return d_parsed
