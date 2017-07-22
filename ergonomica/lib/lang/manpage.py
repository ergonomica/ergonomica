"""
[lib/lang/manpage.py]

Manpage parsing utilities for manpage-based autocompletion.
"""

import os
import sqlite3

conn = sqlite3.connect()

c.execute('''create table if not exists completions
             (stem text, tail text)''')

def get_all_args_from_man(command):
    """
    Returns a dictionary mapping option->their descriptions
    """

    devnull = open(os.devnull, 'w')
    try:
        options = [x for x in subprocess.check_output(["man", command], stderr=devnull).replace("\x08", "").replace("\n\n", "{TEMP}").replace("\n", " ").replace("{TEMP}", "\n").split("\n") if x.startswith("     -")]
    except OSError:
        return {}
    except subprocess.CalledProcessError:
        try:
            options = [x for x in subprocess.check_output([command, "--help"], stderr=devnull).replace("\x08", "").replace("\n\n", "{TEMP}").replace("\n", " ").replace("{TEMP}", "\n").split("\n") if x.startswith("     -")]
        except subprocess.CalledProcessError:
            return {}
        except OSError:
            return {}
        return {}
        
    options = [re.sub("[ ]+", " ", x) for x in options]

    parsed_options = {}
    
    for i in options:
        parsed_options[i.strip().split(" ")[0][::2]] = " ".join(i.strip().split(" ")[1:])
    
    return parsed_options


class BasicCompleter(Completer):
    

class UNIXCompleter(Completer):
   """A completer object with support for automatic manpage parsing."""

def get_completer():
   