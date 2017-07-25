"""
[lib/lib/ergo_help.py]

Defines the "help" command.
"""

def _help(argc):
    """
    help: the Ergonomica help system.
    
    Usage:
        help command COMMAND
        help commands
    """
    
    if argc.args['command']:
        yield argc.ns[argc.args['COMMAND']].__doc__
    
    elif argc.args['commands']:
        for command in argc.ns:
            yield command


exports = {'help': _help}
