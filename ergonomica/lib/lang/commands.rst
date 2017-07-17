load
----

..code::


    load: Load a file into ergonomica.

    Usage:
       load FILE
    
pyvim
-----

..code::


        pyvim: Pure Python Vim clone.

        Usage:
            pyvim [FILES...]
        
rprompt
-------

..code::


       rprompt: Set the text for the Ergonomica rprompt (next next to prompt).

       Usage:
          rprompt STRING

    
shuffle
-------

..code::

shuffle: Shuffle STDIN.

    Usage:
        shuffle
    
help
----

..code::

help: the Ergonomica help system.
    
    Usage:
        help command COMMAND
        help commands
    
mkdir
-----

..code::

mkdir: Make a directory.

    Usage:
       mkdir DIR
    
cd
--

..code::

cd: Changes the directory.

    Usage:
        cd [DIR]
    
set
---

..code::

set: Set variables.

    Usage:
       set <variable>VAR VAL
    
pass
----

..code::

pass: Does nothing.

    Usage:
       pass
    
download
--------

..code::


    download: Download a remote file.

    Usage:
       download URL
    
cp
--

..code::

cp: Copy files.

    Usage:
        cp SOURCE DESTINATION
    
removeline
----------

..code::

removeline: Remove lines with indices LINENUM from FILE.

    Usage:
        removeline (-f FILE) <int>LINENUM...

    Options:
        -f --file  Specify the file to operate on.
    
find
----

..code::

find: Find patterns.

    Usage:
        find PATTERN
        find file PATTERN [-f | --flat] [-s | --strict-path]
        find string PATTERN [-f | --flat]

    Options:
    -f --flat         Do not search recursively (search only the current directory).
    -s --strict-path  Require that file regexp matches full path to the file.

    
if
--

..code::

if: If this, do that.

    Usage:
       if FUNCTION1 FUNCTION2 [FUNCTION3]
    
quit
----

..code::

quit: Exit the Ergonomica shell.

    Usage:
       quit
    
list_modules
------------

..code::

list_modules: List all installed modules.

    Usage:
        list_modules
    
title
-----

..code::

title: Set the title of the current terminal window to TITLE.

    Usage:
        title TITLE
    
graph
-----

..code::

graph: Graph numbers in your terminal.
    
    Usage:
        graph NUMBERS...
    
py
--

..code::

py: Python ergonomica integration.

    Usage:
       py [(--file FILE | STRING)]
    
ping
----

..code::

ping: Ping HOSTNAMEs.

    Usage:
        ping [-c COUNT] HOSTNAMES...

    Options:
        -c --count  Specify the number of times to ping the server.
    
length
------

..code::

length: Return the number of items in STDIN.

    Usage:
        length
        length STRING
    
write
-----

..code::

write: Write STDIN to file FILE.

    Usage:
        write <file>FILE
    
mv
--

..code::

mv: Move files.

    Usage:
       mv TARGET DESTINATION
    
exit
----

..code::

exit: Exit the Ergonomica shell.

    Usage:
       exit
    
ls
--

..code::


    ls: List files in a directory.

    Usage:
       ls <directory>[DIR] [-c | --count-files][-d | --date] [-h | --hide-dotfiles]

    Options:
       -d --date           Show file creation dates.
       -h --hide-dotfiles  Ignore dotfiles.
       -c --count-files    Return the number of files in a directory.
    
print
-----

..code::


    print: Print strings.

    Usage:
       print <string>[STRINGS...] [-m MULTIPLIER] [-f INDICES...]

    Options:
       -f --filter     INDICES  Print the items of the input with the specified indices.
       -m --multiplier MULTIPLIER    Print the given item COUNT times (seperated by newlines).
    
mul
---

..code::

mul: Multiply a string N times.

    Usage:
        mul STRING N
    
net
---

..code::

net: Various network information commands.
    Usage:
        net ip (local|global)
        net mac INTERFACE
        net interfaces
    
size
----

..code::

size: Return the sizes of files.

    Usage:
        size [-u UNIT] FILE...

    Options:
        -u, --unit  Specify the unit of size in which to display the file.

    
swap
----

..code::

swap: Swap the names/contents of two files.

    Usage:
        swap <file>FILE1 <file>FILE2
    
sort
----

..code::

sort: Sort files into folders based on match of regex EXPRESSION in their names.

    Usage:
        sort [DIR=.] EXPRESSION
    
map
---

..code::


    map: Map an argument on STDIN.

    Usage:
       map ARGS...
       map -b BLOCKSIZE ARGS...

    Options:
       -i --ignore-blocksize  If the last block is not complete, ignore.
    
users
-----

..code::

users: Returns a list of currently logged in users.

    Usage:
        users
    
get
---

..code::

get: Get the value of a variable.

    Usage:
       get <variable>VAR
    
read
----

..code::


    read: Read a file.

    Usage:
       read FILE
    
time
----

..code::


    time: Display the current time. FORMAT is in strftime format.

    Usage:
        time [FORMAT]
    
nequal
------

..code::

nequal: Compare if arguments are not equal.

    Usage:
       nequal A B
    
pwd
---

..code::

pwd: Print the working directory.

    Usage:
        pwd
    
rm
--

..code::

rm: Remove files and directories.

    Usage:
       rm <file/directory>FILE
    
write_documentation_with_command
--------------------------------

..code::

usage: function COMMAND
addstring
---------

..code::

addstring: Add all strings from STDIN.

    Usage:
       addstring [-s | --separator SEPARATOR]
    
    
sysinfo
-------

..code::


    sysinfo: Print system information

    Usage:
       sysinfo stat [-apr]
       sysinfo dyn  [-cu]

    Options:
       -a --architecture   Print the system bits as well as linkage.
       -p --processor      Print processor name.
       -o --os             Print OS common name.
       -c --cpu-count       Print the number of CPUs on the system.
       -u --percent-usage  Print percent CPU usage for each CPU.
    
toolbar
-------

..code::


       toolbar: Set the text for the Ergonomica toolbar (bar at bottom of screen).

       Usage:
          toolbar STRING
    
license
-------

..code::

license: Return Ergonomica license information.

    Usage:
        license (show w|show c)
    
cow
---

..code::

cow: Make a cow say STRING.

    Usage:
        cow STRING
    
environment
-----------

..code::


       environment: Configure environment variables.

       Usage:
          environment set VARIABLE VALUE
          environment macro add REGEXP REPLACEMENT
          environment alias add COMMAND REPLACEMENT
    
split
-----

..code::

split: Split a string.

    Usage:
        split STRING SEP
    
clear
-----

..code::

clear: Clear the screen.

    Usage:
       clear
    
f
-

..code::

f: Return false.

    Usage:
       f
    
equal
-----

..code::

equal: Compare equality of arguments.

    Usage:
        equal A B
    
try
---

..code::

try: handle error catching
    
    Usage:
        try BODY
        try BODY EXCEPTION
    
alias
-----

..code::

alias: Map commands to names.
    Usage:
        alias NAME FUNCTION
    
while
-----

..code::

while: While CONDITION returns true, do BODY.

    Usage:
        while CONDITION BODY
    
epm
---

..code::

epm: Ergonomica's package manager.

    Usage:
        epm install PACKAGES...
        epm uninstall PACKAGES...
        epm packages (local|remote)
        epm repos
        epm update
        epm add-source NAME URL
    
t
-

..code::

t: Return true.

    Usage:
       t
    
macro
-----

..code::

macro: Defines a text macro mapping STRING to REPLACEMENT_STRING.

    Usage:
        macro STRING REPLACEMENT_STRING
    
whoami
------

..code::

whoami: Return the current user.

    Usage:
       whoami
    