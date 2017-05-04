#
# [runtime.py]
#
#

from tokenizer import tokenize

import sys


def echo():
    print("a")

namespace = {'echo': echo}

class Operation:
    def __init__(self):
        self.function = ""
        self.args = []

    def set_function(self, functionname):
        self.function = functionname

    def add_argument(self, argument):
        self.args.append(argument)
    

operations = []

class Function:
    name = False
    body = False
    
    def __init__(self):
        pass


lines = open(sys.argv[1], "r").read()

tokens = tokenize(lines)

print("\n".join(map(str, tokens)))

def make_function(string):
    def f():
        return eval_tokens(string)
    return f

def ergo(stdin):
    return eval_tokens(tokenize(stdin))
    
def eval_tokens(tokens):
    
    operation = Operation()

    new_command = False
    in_function = False

    f = False
    args = []
    
    for token in tokens:

        # recognize commands as distinct from arguments
        if (token.type == 'NEWLINE') or (token.type == 'PIPE'):
            if f:
                f = namespace[f]
                f, args = False, []
            
            new_command = True
            continue
        else:
            new_command = False

        if token.type == 'FUNCTION':
            in_function = True
            function = Function()
            function.body = []
            continue
    
        if token.type == "END":
            in_function = False
            namespace[function.name] = make_function(function.body)
            continue
    
        elif (not new_command) and in_function:
            if not function.name:
                function.name = token.value
                pass
            else:
                function.body.append(token)
        
        if new_command and in_function:
            function.body.append(token)
            
        
        elif new_command and (not in_function):
            f = namespace(token.value)

        elif (not new_command) and (not in_function):
            args.append(token.value)
            
