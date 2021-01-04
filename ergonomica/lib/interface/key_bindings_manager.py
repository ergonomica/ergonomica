#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/interface/key_bindings_manager.py]

Defines the prompt_toolkit key bindings manager for Ergonomica's interface.
"""

from __future__ import print_function

from prompt_toolkit.document import Document
from prompt_toolkit.application import get_app
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import (
    has_selection, is_multiline, has_focus, vi_insert_mode, emacs_insert_mode)
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.filters import Filter, Condition
from ergonomica.lib.lang.tokenizer import tokenize


@Condition
def tabs_should_insert_whitespace():
    """
    When the 'tab' key is pressed with only whitespace character before the
    cursor, do autocompletion. Otherwise, insert indentation.
    Except for the first character at the first line. Then always do a
    completion. It doesn't make sense to start the first line with
    indentation.
    """
    current_buffer = get_app().current_buffer
    before_cursor = current_buffer.document.current_line_before_cursor

    return bool(current_buffer.text and (not before_cursor or before_cursor.isspace()))


def load_key_bindings(env):
    """Return a KeyBindings object given an Ergonomica environment."""
    kb = KeyBindings()

    # for some reason Pylint doesn't think this function is "used"
    @kb.add('c-l')
    def clear_(event): # pylint: disable=unused-variable
        """
        Clear the screen.
        """
        clear()
        print(env.get_prompt(), end="")

    @kb.add('tab', filter=tabs_should_insert_whitespace)
    def _(event):
        """
        When tab should insert whitespace, do that instead of completion.
        """
        event.app.current_buffer.insert_text('   ')

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

    # prompt_toolkit _wants_ these two methods (they have different filter
    # attributes)
    @kb.add('enter', filter=~has_selection &
            (vi_insert_mode | emacs_insert_mode) &
            has_focus(DEFAULT_BUFFER) & is_multiline)
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
            return tokenize(ptk_buffer.text).count("(") == tokenize(ptk_buffer.text).count(")")

        if at_the_end(current_buffer)\
           and (current_buffer.document.text.replace(' ', '')
                .endswith('\n' * (empty_lines_required - 1)
                         ) or all_blocks_closed(current_buffer)):
            current_buffer.document = Document(
                text=current_buffer.text.rstrip(),
                cursor_position=len(current_buffer.text.rstrip()))

            current_buffer.validate_and_handle()
        else:
            _auto_newline(current_buffer)

    return kb
