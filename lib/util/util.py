import os
import subprocess
import shlex

def run_command(env, cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    try:
        os.environ["PATH"] = env.PATH
        return subprocess.check_output(shlex.split(cmd), env=os.environ.copy())#, stderr=open(os.devnull, 'wb'))
    except OSError:
        raise Exception
