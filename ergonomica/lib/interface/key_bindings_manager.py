#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/interface/key_bindings_manager.py]

Defines the prompt_toolkit key bindings manager for Ergonomica's interface.
"""

from __future__ import print_function

from prompt_toolkit.document import Document
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import (
    HasSelection, IsMultiline, HasFocus, ViInsertMode, EmacsInsertMode)
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.filters import Filter
from ergonomica.lib.lang.tokenizer import tokenize

class TabShouldInsertWhitespaceFilter(Filter):
    """
    When the 'tab' key is pressed with only whitespace character before the
    cursor, do autocompletion. Otherwise, insert indentation.
    Except for the first character at the first line. Then always do a
    completion. It doesn't make sense to start the first line with
    indentation.
    """
    # this is something PTK does
    def __call__(self, cli): # pylint: disable=arguments-differ
        current_buffer = cli.current_buffer
        before_cursor = current_buffer.document.current_line_before_cursor

        return bool(current_buffer.text and (not before_cursor or before_cursor.isspace()))

def manager_for_environment(env):
    """Return a key bindings manager given an Ergonomica environment."""
    def load_bindings(key_bindings_manager):
        """
        Load keybindings into prompt_toolkit.
        """

        handle = key_bindings_manager.registry.add_binding
        has_selection = HasSelection()

        # for some reason Pylint doesn't think this function is "used"
        @key_bindings_manager.registry.add_binding(Keys.ControlL)
        def clear_(event): # pylint: disable=unused-variable
            """
            Clear the screen.
            """

            clear()
            print(env.welcome)
            print(env.get_prompt(), end="")

        @handle(Keys.Tab, filter=TabShouldInsertWhitespaceFilter())
        def _(event):
            """
            When tab should insert whitespace, do that instead of completion.
            """
            event.cli.current_buffer.insert_text('   ')

        # prompt_toolkit _wants_ these two methods (they have different filter
        # attributes)
        @handle(Keys.ControlJ, filter=~has_selection &
                (ViInsertMode() | EmacsInsertMode()) &
                HasFocus(DEFAULT_BUFFER) & IsMultiline())
        def _(event): # pylint: disable=function-redefined
            """
            Behaviour of the Enter key.

            Auto indent after newline/Enter.
            (When not in Vi navigaton mode, and when multiline is enabled.)
            """
            current_buffer = event.current_buffer
            empty_lines_required = 2

            def at_the_end(ptk_buffer):
                """ we consider the cursor at the end when there is no text after
                the cursor, or only whitespace. """
                text = ptk_buffer.document.text_after_cursor
                return text == '' or (text.isspace() and not '\n' in text)

            def all_blocks_closed(ptk_buffer):
                """Return True when all Ergonomica code blocks are closed."""
                return tokenize(ptk_buffer.text).count("\x00(") == tokenize(ptk_buffer.text).count("\x00)")

            if at_the_end(current_buffer)\
               and (current_buffer.document.text.replace(' ', '')
                    .endswith('\n' * (empty_lines_required - 1)
                             ) or all_blocks_closed(current_buffer)):
                current_buffer.document = Document(
                    text=current_buffer.text.rstrip(),
                    cursor_position=len(current_buffer.text.rstrip()))

                current_buffer.accept_action.validate_and_handle(event.cli, current_buffer)
            else:
                _auto_newline(current_buffer)

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

            for character in current_line:
                if character.isspace():
                    insert_text(character)
                else:
                    break

            # If the last line ends with a colon, add four extra spaces.
            insert_text('   ' * (tokenize(current_line).count("(") - tokenize(current_line).count(")")))

    manager = KeyBindingManager.for_prompt()

    load_bindings(manager)

    return manager


