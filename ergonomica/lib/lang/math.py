

def add(argc):
    """add: Add a series of numbers.
    
    Usage:
        add [NUMBERS...]"""

    try:
        i = int

def geq(argc):
    """geq: Compare equality of arguments.

    Usage:
        geq ARG1 ARG2
    """
    
    try:
        i = int(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = int(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i >= j
    
def geq(argc):
    """geq: Compare equality of arguments.

    Usage:
        geq ARG1 ARG2
    """
    
    try:
        i = int(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = int(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i >= j
    
def geq(argc):
    """equal: Compare equality of arguments.

    Usage:
        equal ARGS...
    """
    
    try:
        i = int(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = int(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i >= j
    
def geq(argc):
    """geq: Compare equality of arguments.

    Usage:
        geq ARG1 ARG2
    """
    
    try:
        i = int(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = int(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i >= j

def add_math_functions_to_namespace(ns):
    ns.update({'+': add,
               '-': subtract,
               ''})