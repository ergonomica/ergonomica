import verbs
import parser

commandCheck = False
argumentCheck = False
kargumentCheck = False

def cmdCheck(string):
    command = parser.tokenize(string)
    if len(command[0][0]) !=0:
        pass
    else:
        if command in verbs.verbs:
            commandCheck = True
            return string
        else:
            pass

def argCheck(string):
    argument = parser.tokenize(string)[1][0]

def kargCheck(string):
    kargument = parser.tokenize(string)[2][0]
