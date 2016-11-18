def get_hist_file():
    HIST_FILE = open(os.path.expanduser("~/.ergo_history"), 'a')


    
    HIST = open(os.path.expanduser("~/.ergo_history"), "r").read().split("\n")
    for item in HIST[:-1]:
        readline.add_history(item)
