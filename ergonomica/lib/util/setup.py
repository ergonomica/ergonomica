"""
[lib/util/setup.py]

The Ergonomica setup script.
"""

import os
import requests
import shutil

try:
   input = raw_input
except NameError:
   pass

def setup():
    """
    Set up the users computer for Ergonomica. Note that this is only
    called when it is known that their computer does not have this structure
    is installed.
    """

    user_dir = os.path.expanduser("~")

    os.mkdir(os.path.join(user_dir, ".ergo"))
    os.mkdir(os.path.join(user_dir, ".ergo", "packages"))
    open(os.path.join(user_dir, ".ergo", ".ergo_profile"), "w")
    open(os.path.join(user_dir, ".ergo", ".ergo_history"), "w")
    open(os.path.join(user_dir, ".ergo", "packages", "__init__.py"), "w")

    # prompt for installing epm
    while True:
        choice = input("Do you want to install epm (the Ergonomica Package Manager) (recommended)? (Y/n): ").strip()
        if (choice.lower() == "y") or (choice == ""):
            url = "https://raw.githubusercontent.com/ergonomica/package-epm/master/epm.py"
            response = requests.get(url)
            with open(os.path.join(user_dir, ".ergo", "packages", "epm.py"), 'w') as out_file:
                out_file.write(response.content)
            break
        elif (choice.lower() == "n"):
            break
        else:
            print("[ergo]: [ergo-installer]: Invalid choice {}.".format(choice))
    
