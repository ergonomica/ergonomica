def validate_symbol(symbol):
    """
    Throws appropriate exceptions on an invalid symbol.
    """

    if "]" in symbol:
        if not symbol.endswith("]"):
            raise SyntaxError("[ergo: SyntaxError]: Unexpected \"]\" in Symbol \"{}\".".format(symbol))
        else:
            try:
                int(symbol[(symbol.find("[") + 1):symbol.find("]")])
            except ValueError:
                raise SyntaxError("[ergo: SyntaxError]: Non-integer index specified in Symbol \"{}\".".format(symbol))
                              
    elif "[" in symbol:
        raise SyntaxError("[ergo: SyntaxError]: Unexpected \"[\" in Symbol \"{}\".".format(symbol))

class Symbol(str):
    def __new__(self, value):
        validate_symbol(value)
        return super(Symbol, self).__new__(self, value)

def unquote(str):
    """Remove quotes from a string."""
    if len(str) > 1:
        if str.startswith('"') and str.endswith('"'):
            return str[1:-1].replace('\\\\', '\\').replace('\\"', '"')
        if str.startswith('<') and str.endswith('>'):
            return str[1:-1]
    return str

def parse(tokens, allow_unclosed_blocks=False):
    depth = 0
    L = []
    parsed_command = False # switch set to true on first atom parsed---ensures that
                           # arguments after the command interpreted as strings
    parsed_tokens = []
    for token in tokens:
        if token.startswith("//"):
            continue
        if depth > 0:
            if token == ")":
                depth -= 1
            elif token == "(":
                depth += 1
            if depth == 0:
                parsed_tokens.append(parse(L))
                L = []
            else:
                L.append(token)
            continue
                
        if token == "(":
            depth = 1
            continue

        if token == "|":
            parsed_command = False
            parsed_tokens.append(token)
            continue
        
        if not parsed_command or token.startswith("#"):
            parsed_tokens.append(Symbol(token))
            parsed_command = True
            
        else:
            try:
                parsed_tokens.append(int(token))
            except ValueError: 
                try: 
                    parsed_tokens.append(float(token))
                except ValueError:
                    # it's a string or Symbol
                    if token.startswith("$"):
                        parsed_tokens.append(Symbol(token[1:])) # make a Symbol with the $ stripped away
                    else:
                        if token.startswith("'") or token.startswith("\""):
                            parsed_tokens.append(unquote(token))
                        else:
                            parsed_tokens.append(token)

    if (L != []) and allow_unclosed_blocks:
        # i.e., there are some incomplete S-expressions. We want to allow
        # parsing this because it's necessary for the completion engine
        parsed_tokens.append(parse(L, allow_unclosed_blocks))
                            
    return parsed_tokens
