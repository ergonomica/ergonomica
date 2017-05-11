"""
[lib/lang/arguments.py]

The Ergonomica arguments handler. Creates the ArgumentsContainer object.
"""

class ArgumentsContainer:
    
    def __init__(self, env, ns, stdin, args):            
        self.env, self.ns, self.stdin, self.args = env, ns, stdin, args
    
    
