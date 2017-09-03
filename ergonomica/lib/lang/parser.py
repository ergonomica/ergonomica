#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ergonomica import ErgonomicaError
from ergonomica.lib.lang.tokenizer import tokenize

def validate_symbol(symbol):
    """
    Throws appropriate exceptions on an invalid symbol.
    """

    return

class Symbol(str):
    def __new__(self, value):
        validate_symbol(value)
        return super(Symbol, self).__new__(self, value)

def convert_piping_tokens(_tokens):
    tokens = [x for x in _tokens]
    if "{}" in tokens:
        for i in range(len(tokens)):
            if tokens[i] == "{}":
                tokens[i] = Symbol("__stdin__")
        return (0, tokens)

    blocksize = -1

    for i in range(len(tokens)):
        token = tokens[i]
        if isinstance(token, str) and token.startswith("{") and token.endswith("}"):
            content = token[1:-1] # the index code
            if "/" in content:
                blocksize = int(content.split("/")[1])
                tokens[i] = [Symbol("slice"), int(content.split("/")[0]), Symbol("__stdin__")]
            else:
                if int(content) > blocksize:
                    blocksize = int(content)
                tokens[i] = [Symbol("slice"), int(content), Symbol("__stdin__")]

    return (blocksize + 1, tokens)


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
            compiled_tokens.append([Symbol("lambda"), [Symbol("__stdin__")], convert_piping_tokens(exp)[1]])
            blocksizes.append(convert_piping_tokens(exp)[0])
        return [Symbol("pipe"), [Symbol("list")] + blocksizes] + compiled_tokens
    else: # nothing to be compiled
        return tokens


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
            if token == "\x00)":
                depth -= 1
            elif token == "\x00(":
                parsed_command = True
                depth += 1
            if depth == 0:
                parsed_tokens.append(parse(L))
                L = []
            else:
                L.append(token)
            continue

        if token == "\x00(":
            parsed_command = True
            depth = 1
            continue

        if token == "|":
            parsed_command = False
            parsed_tokens.append(token)
            continue

        if not parsed_command:
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
                            parsed_tokens.append(token.encode())
                        else:
                            parsed_tokens.append(token.encode().decode("unicode-escape"))

    if (L != []) and allow_unclosed_blocks:
        # i.e., there are some incomplete S-expressions. We want to allow
        # parsing this because it's necessary for the completion engine
        parsed_tokens.append(parse(L, allow_unclosed_blocks))

    return pipe_compile(parsed_tokens)

def file_lines(stdin):
    split_lines = [""]
    paren_depth = 0
    for line in stdin.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            continue
        paren_depth += tokenize(line).count("\x00(") - tokenize(line).count("\x00)")
        if paren_depth == 0:
            split_lines[-1] += line
            split_lines.append("")
        else:
            split_lines[-1] += line
    return [x for x in split_lines if x]

def check_token(token):
    """Raise a SyntaxError on a malformed token."""
    if (token.startswith("'") and token.endswith("'")) or \
       (token.startswith("\"") and token.endswith("\"")):
        return
