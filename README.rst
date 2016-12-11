==========
ergonomica
==========
A Bash alternative written in Python.

|homebrew| |license| |cissues| |codeclimate| |travisci|

Commands
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

Find all files in *dir*, recursively. If *name* is specified, all files within *dir* whos name match that pattern (according to python regexp) will be returned.

find_string *dir* {name:*name*}
-------------------------------

GO through all lines in all files in *dir, recursively. Finds lines in these files that match pattern *name.


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


Examples
========

Mapping a function
------------------

.. code::

   [lschumm@/Users/lschumm]
   $ ls -> (map) x + " is on my computer"
   .emacs.d is on my computer
   Applications is on my computer
   Desktop is on my computer
   Documents is on my computer
   Library is on my computer
   Movies is on my computer
   Music is on my computer
   Pictures is on my computer
   Public is on my computer
   
Filtering
---------

.. code::

   [lschumm@/Users/lschumm]
   $ ls -> (filter) x[0] == "P"
   Pictures
   Public
   
Moving some log files into folders based on year
------------------------------------------------

.. code::

   [lschumm@/Users/lschumm]
   $ ls
   2016-1.log
   2016-2.log
   2016-3.log
   2015-1.log
   2015-2.log
   2015-3.log
   2014-1.log
   2014-2.log
   2014-3.log
   2013-1.log
   2013-2.log
   2013-3.log
   $ ls -> (map) x[:4] ->  mkdir
   $ ls -> (map) x[:4] -> (filter) "log" in x -> (splice) -> mv
   $ ls
   2016
   2015
   2014
   2013



.. |homebrew| image:: https://img.shields.io/badge/homebrew-1.0.0%20beta%205-orange.svg?style=flat-square

.. |license| image:: https://img.shields.io/github/license/ergonomica/ergonomica.svg?style=flat-square

.. |cissues| image:: https://img.shields.io/github/issues-closed/ergonomica/ergonomica.svg?style=flat-square

.. |codeclimate| image:: https://codeclimate.com/github/ergonomica/ergonomica/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/ergonomica/ergonomica
   :alt: Code Climate
 
.. |travisci| image:: https://travis-ci.org/ergonomica/ergonomica.svg?branch=master
   :target: https://travis-ci.org/ergonomica/ergonomica
   :alt: Travis CI Build Status
