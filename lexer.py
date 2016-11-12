#pylint: disable-all

"""Lexer module. Contains tokenize()."""


def tokenize(string):
    """Tokenize ergonomica commands."""    

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
