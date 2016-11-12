"""
[ergonomica.py]
The ergonomica runtime.
"""


from lexer import tokenize
from verbs import verbs

def eval(stdin):
    tokens = tokenize(stdin)
    return verbs.verbs[tokens[0][0]](tokens[1], tokens[2])

while verbs.run:
    STDIN = raw_input("[ergo}> ")
    try:
        STDOUT = eval(STDIN)
    except Exception, e:
        STDOUT = repr(e)
    print STDOUT
