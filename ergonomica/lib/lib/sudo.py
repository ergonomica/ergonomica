#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/sudo.py]

Defines the "sudo" command for permission escalation.5555
"""

import sys, os, traceback, types
from ergonomica.lib.lang.error import ErgonomicaError

verbs = {}

def isUserAdmin():
    """@return: True if the current user is an 'Admin' whatever that
    means (root on Unix), otherwise False.
    Warning: The inner function fails unless you have Windows XP SP2 or
    higher. The failure causes a traceback to be printed and this
    function to return False.
    """
    
    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print "Admin check failed, assuming not an admin."
            return False
    else:
        # Check for root on Posix
        return os.getuid() == 0

def runAsAdmin(cmdLine=None, wait=True):
    """Attempt to relaunch the current script as an admin using the same
    command line parameters.  Pass cmdLine in to override and set a new
    command.  It must be a list of [command, arg1, arg2...] format.
    Set wait to False to avoid waiting for the sub-process to finish. You
    will not be able to fetch the exit code of the process if wait is
    False.
    Returns the sub-process return code, unless wait is False in which
    case it returns None.
    @WARNING: this function only works on Windows.
    """

    if os.name != 'nt':
        euid = os.geteuid()
        if euid != 0:
            print "Script not started as root. Running sudo.."
            args = ['sudo', sys.executable] + sys.argv + [os.environ]
            # the next line replaces the currently-running process with the sudo
            os.execlpe('sudo', *args)

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon
    
    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType,types.ListType):
        raise ValueError, "cmdLine is not a sequence."
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'  # causes UAC elevation prompt.
    
    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']    
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        #print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc

def sudo():
    """ """

    

def sudo():
    """A simple test function; check if we're admin, and if not relaunch
    the script as admin.""",
    rc = 0
    if not isUserAdmin():
        print "You're not an admin.", os.getpid(), "params: ", sys.argv
        #rc = runAsAdmin(["c:\\Windows\\notepad.exe"])
        rc = runAsAdmin()
    else:
        print "You are an admin!", os.getpid(), "params: ", sys.argv
        rc = 0
    x = raw_input('Press Enter to exit.')
    return rc


if __name__ == "__main__":
    res = test()
    sys.exit(res)


verbs["echo"] = echo
verbs["print"] = echo
