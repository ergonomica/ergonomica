def get_prompt(env):
    return unicode(env.prompt.replace("<user>", env.user).replace("<directory>", env.directory))
