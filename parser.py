"""Lexer module. Contains tokenize()."""

import re
import subprocess
from verbs import verbs

def tokenize(string):
    """Tokenize ergonomica commands."""

    tokens = [""]
    try:
        bash_escaped = re.search("`(.+?)`", string).groups()

        for item in bash_escaped:
            string = string.replace("`" + item + "`", subprocess.check_output(item.split(","), cwd=verbs.directory))
    except AttributeError:
        pass

    tokens = [""]
    _special = False
    kwargs = []
    args = []

    for char in string:
        if _special:
            if char in ["}", "]"]:
                if _special == "{":
                    kwargs.append(special)
                elif _special == "[":
                    args.append(special)
                _special = False
            else:
                special += char
        else:
            if char == " ":
                tokens.append("")
            elif char in ["{", "["]:
                _special = char
                special = ""
            else:
                tokens[-1] += char

           # filter out empty strings
    return [[x for x in tokens if x], args, kwargs]

def parse(string):
    blocks = [tokenize(x) for x in string.split("->")]
    for i in range(0, len(blocks)):
        kwargs = {}
        blocks[i] = "%s(%s, %s)" % (blocks[i][0][0], ", ".join(blocks[i][1]), ", ".join([s.replace(":", "=") for s in blocks[i][2]]))
    return blocks
