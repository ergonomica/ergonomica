from lexer import tokenize
import commands

def eval(stdin):
    tokens = tokenize(stdin)
    return commands.commands[tokens[0][0]](tokens[1], tokens[2])

while 1:
    STDIN = raw_input("[ergo}> ")
    STDOUT = eval(STDIN)
