import subprocess
import shlex

def run_command(cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    try:
        return subprocess.check_output(shlex.split(cmd)) #shell=True), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return
