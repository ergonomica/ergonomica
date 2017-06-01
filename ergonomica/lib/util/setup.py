import os

def setup():
    os.mkdir(os.path.join(os.path.expanduser("~"), ".ergo"))
    os.mkdir(os.path.join(os.path.expanduser("~"), ".ergo", "packages"))
    open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile"), "w")
    open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_history"), "w")
    open(os.path.join(os.path.expanduser("~"), ".ergo", "package", "__init__.py"), "w")
