import sys
from docopt import docopt

__doc__ = "usage: example.py LOL"

print(sys.argv)

print(docopt(__doc__, argv=["lol"]))
