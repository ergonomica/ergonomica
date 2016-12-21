"""
Help text for Suplemon
"""

help_text = """
# Suplemon Help

*Contents*
1. General description
2. User interface
3. Default keyboard shortcuts
4. Commands

## 1. General description
Suplemon is designed to be an easy, intuitive and powerful text editor.
It emulates some features from Sublime Text and the user interface of Nano.
Multi cursor editing is a core feature. Suplemon also supports extensions
so you can customize it to work how you want.

## 2. User interface
The user interface is designed to be as intuitive and informative as possible.
There are two status bars, one at the top and one at the bottom. The top bar
shows the program version, a clock, and a list of opened files. The bottom bar
shows status messages and handles input for commands. Above the bottom status
bar there is a list of most common keyboard shortcuts.

## 3. Default keyboard shortcuts
The default keyboard shortcuts imitate those of common graphical editors.
Most shortcuts are also shown at the bottom in the legend area. Here's
the complete reference.


 * Ctrl + Q
   > Exit

 * Ctrl + C
   > Copy line(s) to buffer

 * Ctrl + X
   > Cut line(s) to buffer

 * Ctrl + V
   > Insert buffer

 * Ctrl + K
   > Duplicate line

 * Ctrl + G
   > Go to line number or file (type the beginning of a filename to switch to it).
   > You can also use 'filena:42' to go to line 42 in filename.py etc.

 * Ctrl + F
   > Search for a string or regular expression (configurable)

 * Ctrl + D
   > Search for next occurance or find the word the cursor is on. Adds a new cursor at each new occurance.

 * Alt + Arrow Key
   > Add new curor in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word or line

 * ESC
   > Revert to a single cursor / Cancel input prompt

 * Alt + Page Up
   > Move line(s) up

 * Alt + Page Down
   > Move line(s) down

 * Ctrl + S
   > Save current file

 * F1
   > Save file with new name

 * F2
   > Reload current file

 * Ctrl + O
   > Open file

 * Ctrl + W
   > Close file

 * Ctrl + Page Up
   > Switch to next file

 * Ctrl + Page Down
   > Switch to previous file

 * Ctrl + E
   > Run a command.

 * F5
   > Undo

 * F6
   > Redo

 * F7
   > Toggle visible whitespace

 * F8
   > Toggle mouse mode

 * F9
   > Toggle line numbers

 * F11
   > Toggle full screen

### Mouse shortcuts

 * Left Click
   > Set cursor at mouse position. Reverts to a single cursor.

 * Right Click
   > Add a cursor at mouse position.

 * Scroll Wheel Up / Down
   > Scroll up & down.


## 4. Commands
Commands are special operations that can be performed (e.g. remove whitespace
or convert line to uppercase). Each command can be run by pressing Ctrl + E
and then typing the command name. Commands are extensions and are stored in
the modules folder in the Suplemon installation.

"""
