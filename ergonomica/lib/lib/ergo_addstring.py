"""
[lib/lib/addstring.py]

Defines the Ergonomica addstring command.
"""


def addstring(argc):
    """addstring: Add all strings from STDIN.
    Usage:
       addstring [-s | --separator SEPARATOR]
    
    """
    
    #
    # Options:
    #     -s--seperator  Specify a seperator for the strings.
    # """

    if argc.args['--separator']:
        yield argc.args['SEPARATOR'].join(argc.stdin)
    else:
        yield "".join(argc.stdin)
        
exports = {'addstring': addstring}
