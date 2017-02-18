"""
[lib/lang/stdout.py]

Handle output.
"""

from __future__ import print_function

def handle_stdout(stdout, pipe, num_blocks):
    #if not isinstance(stdout, list):
    #    pipe.setstack_args([stdout])
    #    if (not num_blocks) and (stdout != None):
    #        print(stdout, file=sys.stderr)
    #else:
    pipe.setstack_args(stdout)
    if not num_blocks:
        return stdout
