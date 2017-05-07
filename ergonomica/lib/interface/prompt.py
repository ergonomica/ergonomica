import prompt_toolkit

def prompt():
    #return prompt_toolkit.prompt(unicode_(PROMPT), history=history, completer=ErgonomicaCompleter(verbs), multiline=True,key_bindings_registry=key_bindings_registry)
    return prompt_toolkit.prompt(multiline=True)
