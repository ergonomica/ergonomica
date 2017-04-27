from __future__ import print_function

import sys

from prompt_toolkit.document import Document
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import (
    HasSelection, IsMultiline, HasFocus, ViInsertMode, EmacsInsertMode)
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.shortcuts import clear
from ergonomica.lib.lib.ls import ls

def unicode_(PROMPT):
    if sys.version_info[0] >= 3:
        return str(PROMPT)
    else:
        return unicode(PROMPT)

def manager_for_environment(env):

    def load_bindings(key_bindings_manager):
        handle = key_bindings_manager.registry.add_binding
        has_selection = HasSelection()

        @key_bindings_manager.registry.add_binding(Keys.ControlL)#, eager=True)
        def clear_(event):
            clear()
            print(env.welcome)
            PROMPT = env.prompt
            PROMPT = PROMPT.replace(r"\u", env.user).replace(r"\w", env.directory)
            print(unicode_(PROMPT), end="")

        @key_bindings_manager.registry.add_binding(Keys.ControlB)
        def list_(event):
            print("\n".join(ls(env, [], {})))
            PROMPT = env.prompt
            PROMPT = PROMPT.replace(r"\u", env.user).replace(r"\w", env.directory)
            print(env.default_color, end="")
            print(unicode_(PROMPT), end="")
            
        @handle(Keys.ControlJ, filter= ~has_selection &
            (ViInsertMode() | EmacsInsertMode()) &
            HasFocus(DEFAULT_BUFFER) & IsMultiline())
        def _(event):
            """
            Behaviour of the Enter key.
            
            Auto indent after newline/Enter.
            (When not in Vi navigaton mode, and when multiline is enabled.)
            """
            b = event.current_buffer
            empty_lines_required = 2

            def at_the_end(b):
                """ we consider the cursor at the end when there is no text after
                the cursor, or only whitespace. """
                text = b.document.text_after_cursor
                return text == '' or (text.isspace() and not '\n' in text)

            if at_the_end(b) and (b.document.text.replace(' ', '').endswith('\n' * (empty_lines_required - 1)) or (b.document.text.replace("\n", "").endswith(";"))):
                # When the cursor is at the end, and we have an empty line:
                # drop the empty lines, but return the value.
                b.document = Document(
                    text=b.text.rstrip(),
                    cursor_position=len(b.text.rstrip()))

                b.accept_action.validate_and_handle(event.cli, b)
            else:
                _auto_newline(b)

    def _auto_newline(_buffer):
        r"""
        Insert \n at the cursor position. Also add necessary padding.
        """
        insert_text = _buffer.insert_text

        if _buffer.document.current_line_after_cursor:
            # When we are in the middle of a line. Always insert a newline.
            insert_text('\n')
        else:
            # Go to new line, but also add indentation.
            current_line = _buffer.document.current_line_before_cursor.rstrip()
            insert_text('\n')
            
            # Unident if the last line ends with 'pass', remove four spaces.
            unindent = current_line.rstrip().endswith(' pass')
                    
            # Copy whitespace from current line
            current_line2 = current_line[4:] if unindent else current_line
                    
            for c in current_line2:
                if c.isspace():
                    insert_text(c)
                else:
                    break
                        
            # If the last line ends with a colon, add four extra spaces.
            if current_line[-1:] == ':':
                for x in range(4):
                    insert_text(' ')
    
    manager = KeyBindingManager.for_prompt()

    load_bindings(manager)

    return manager
