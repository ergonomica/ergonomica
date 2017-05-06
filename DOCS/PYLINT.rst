Why Ergonomica's Pylint Standards
=================================

Pylint is a nice, easy way to ensure some degree of code quality and adherence to standards like PEP8. However, it can be a pain sometimes. Here are the modififications used in the Ergonomica :code:`.pylintrc` file, as well as explanation of the reasoning behind these choices.

Design
======
	
Public Method 
----------------------------

Public/Private method limits (R0903, R0904) can be silly


Maximum number of arguments for function/method
-----------------------------------------------

In unix shell utilities such as `cat`, `man`, `sudo`, there are typically a wide variety of options for modifying the execution of these functions to many different use cases. As a result, in order for Ergonomica functions to replicate this usefulness (imagine a different `sudo` for each option), more arguments need to be provided to each method. This 
