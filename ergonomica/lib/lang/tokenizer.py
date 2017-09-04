#!/usr/bin/env python
# -*- coding: utf-8 -*-

def quotereplacechar(char, sub, string):
    """
    Quote respecting replace.
    """

    quote = False
    fixed_string = ""
    
    for i in string:
        # quote handling
        if i in ["'", "\""]:
            if not quote:
                quote = i
                fixed_string += i
            elif quote == i:
                quote = False
                fixed_string += i
            else:
                fixed_string += i
                
        elif quote:
            fixed_string += i
            
        else:        
            if i == char:
                fixed_string += sub
            else:
                fixed_string += i
    
    return fixed_string
    

def quotesplit(string):
    """
    Quote respecting split (by spaces).
    
    Example:
    
    >>> quotesplit('a b c')
    ['a', 'b', 'c']
    >>> quotesplit('a "b c"')
    ['a', '"b c"']
    """
    
    quote = False
    split_string = [""]
    
    for i in string:
        # quote handling
        if i in ["'", "\""]:
            if not quote:
                quote = i
            elif quote == i:
                quote = False
    
        if quote:
            split_string[-1] += i
            
        else:
            if i in [" ", "\t", "\n", "\r"]:
                split_string.append("")
            else:
                split_string[-1] += i
    
    return [x for x in split_string if x != ""]

def tokenize(string):    
    return quotesplit(quotereplacechar("(", " ( ", quotereplacechar(")", " ) ", string)))

def convert_piping_tokens(_tokens):
    tokens = [x for x in _tokens]
    if "{}" in tokens:
        for i in range(len(tokens)):
            if tokens[i] == "{}":
                tokens[i] = "$__stdin__"
        return (0, tokens)

    blocksize = -1

    for i in range(len(tokens)):
        token = tokens[i]
        if isinstance(token, str) and token.startswith("{") and token.endswith("}"):
            content = token[1:-1] # the index code
            if "/" in content:
                blocksize = int(content.split("/")[1])
                tokens[i] = "$__stdin__[" + content.split("/")[0] + "]"
            else:
                if int(content) > blocksize:
                    blocksize = int(content)
                tokens[i] = "$__stdin__[" + content + "]"

    return (blocksize + 1, tokens)


