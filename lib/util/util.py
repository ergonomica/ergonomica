import os
import subprocess
import shlex

def run_command(env, cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    try:
        os.environ["PATH"] = env.PATH                                                                                                                                                           
        return subprocess.Popen(shlex.split(cmd), env=os.environ.copy()).communicate()
    except subprocess.CalledProcessError:
        return
