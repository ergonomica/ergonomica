import ConfigParser

config = ConfigParser.RawConfigParser()

config = ConfigParser.SafeConfigParser()

# sections are added in the reverse order that they appear
# (https://docs.python.org/2/library/configparser.html#examples)
config.add_section('Prompt')
config.set('Prompt', 
