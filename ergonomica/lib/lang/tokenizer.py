#!/usr/bin/python
# -*- coding: utf-8 -*-

from shlex import split

def pipe_compile(tokens):
    """
    Compile a list of ErgoLisp tokens that contain pipe characters to an expression using the `pipe` function.
    """
    
    if "|" in tokens:
        blocksizes = []
        expressions = [[]]
        for token in tokens:
            if token == "|":
                expressions.append([])
            else:
                expressions[-1].append(token)
        compiled_tokens = []
        for exp in expressions:
            compiled_tokens += ["(", "lambda", "(", "__stdin__", ")", "("] + convert_piping_tokens(exp)[1] + [")", ")"]
            blocksizes.append(str(convert_piping_tokens(exp)[0]))
        return ["pipe", "(", "list"] + blocksizes + [")"] + compiled_tokens
    else: # nothing to be compiled
        return tokens

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

def tokenize(string):
    return pipe_compile(split(escape_parens(string.replace("\n", " ")).replace("\x00(", " ( ").replace("\x00)", " ) "), posix=False))


def escape_parens(string):
    string_delim = False  # the wrapping quote
    escaped_string = [""]   # will be joined after completion
    for i in string:
        if i in ["(", ")"]:
            if not string_delim:
                escaped_string[-1] += "\x00" + i
                continue
            else:
                escaped_string[-1] += i
        elif i in ["\"", "'"]:
            escaped_string[-1] += i
            if string_delim:
                if string_delim == i:
                    string_delim = False
                    continue
            else:
                string_delim = i
                continue
        else:
            if (len(escaped_string) > 0):
                if (i == " ") and not string_delim:
                    escaped_string.append("")
                    pass
                else:
                    escaped_string[-1] += i
            else:
                escaped_string.append(i)

    return " ".join(escaped_string)

def pipe_compile(tokens):
    """
    Compile a list of ErgoLisp tokens that contain pipe characters to an expression using the `pipe` function.
    """
    
    if "|" in tokens:
        blocksizes = []
        expressions = [[]]
        for token in tokens:
            if token == "|":
                expressions.append([])
            else:
                expressions[-1].append(token)
        compiled_tokens = []
        for exp in expressions:
            compiled_tokens += ["(", "lambda", "(", "__stdin__", ")", "("] + convert_piping_tokens(exp)[1], [")", ")"]
            blocksizes.append(str(convert_piping_tokens(exp)[0]))
        return ["pipe", "(", "list"] + blocksizes + [")"] + compiled_tokens
    else: # nothing to be compiled
        return tokens

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
