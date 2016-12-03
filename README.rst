==========
ergonomica
==========
A Bash alternative written in Python.

|homebrew| |license| |cissues| |codeclimate|

commands
========

yes
---

Returns a 'y'.

quit/exit
---------

Quits the ergonomica shell.

cd *dir*
--------

Changes to directory *dir*.


list/ls [*dir*]
---------------

Lists files in the current directory. If *dir* is specified, will list files in that directory.

remove/rm *file*
----------------

Removes *file* (also accepts directories).

mkdir
-----

Make directory

find *dir* {name:*name*}
------------------------

Find all files in *dir*, recursively. If *name* is specified, all files within *dir* that match that pattern (according to python regexp) will be returned.


move/mv *path1* *path2*
-----------------------

Move a file or directory from *path1* to *path2*.

copy/cp *path1* *path2*
-----------------------

Copy a file or directory from *path1* to *path2*.

echo/print *string*
-------------------

Prints *string*.

set/def/var {*var1*:*val1*,*var2*:*val2*,...}
---------------------------------------------

Set *var1* to *val1*, *var2* to *val2*, etc. in the ergonomica namespace.


get/val *var*
-------------

Returns the value of *var* in the ergonomica namespace.


edit *file1*, *file2*...
------------------------

Edit all *file*s specified.


whoami
------

Returns the current user.


pwd
---

Return the current working directory.

version
-------

Return ergonomica version information.

help [*command*]
----------------

Prints all commands and their docstrings. If *command* is specified, returns the docstring for command *command*.



.. |homebrew| image:: https://img.shields.io/badge/homebrew-1.0.0a1-orange.svg?style=flat-square

.. |license| image:: https://img.shields.io/github/license/ergonomica/ergonomica.svg?style=flat-square

.. |cissues| image:: https://img.shields.io/github/issues-closed/ergonomica/ergonomica.svg?style=flat-square

.. |codeclimate| image:: https://codeclimate.com/github/ergonomica/ergonomica/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/ergonomica/ergonomica
   :alt: Code Climate
 
