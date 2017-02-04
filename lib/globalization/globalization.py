"""
[lib/globalization/globalization.py]

Globalization
"""

import os

def globalization_query(string, language):
    return open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "globalization", language, string)).read()[:-1]
