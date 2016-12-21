# -*- encoding: utf-8
"""
Editor class for extending viewer with text editing features.
"""


from . import helpers

from .line import Line
from .cursor import Cursor
from .viewer import Viewer


class State:
    """Store editor state for undo/redo."""
    def __init__(self, editor=None):
        self.cursors = [Cursor()]
        self.lines = [Line()]
        self.y_scroll = 0
        self.x_scroll = 0
        self.last_find = ""
        if editor is not None:
            self.store(editor)

    def store(self, editor):
        """Store the state of editor instance."""
        self.cursors = [cursor.tuple() for cursor in editor.cursors]
        self.lines = [line.data for line in editor.lines]
        self.y_scroll = editor.y_scroll
        self.x_scroll = editor.x_scroll
        self.last_find = editor.last_find

    def restore(self, editor):
        """Restore stored state into the editor instance."""
        editor.cursors = [Cursor(cursor) for cursor in self.cursors]
        editor.lines = [Line(line) for line in self.lines]
        editor.y_scroll = self.y_scroll
        editor.x_scroll = self.x_scroll
        editor.last_find = self.last_find


class Editor(Viewer):
    """Extends Viewer with editing capabilities."""
    def __init__(self, app, window):
        """Initialize the editor.

        Args:
            app: The Suplemon main instance.
            window: A window object to use for the ui.
        """
        Viewer.__init__(self, app, window)

        # History of editor states for undo/redo
        self.history = [State()]
        # Current state index of the editor
        self.current_state = 0
        # Last editor action that was used (for undo/redo)
        self.last_action = None

    def init(self):
        Viewer.init(self)
        operations = {
            "backspace": self.backspace,                  # Backspace
            "delete": self.delete,                        # Delete
            "insert": self.insert,                        # Insert
            "enter": self.enter,                          # Enter
            "tab": self.tab,                              # Tab
            "untab": self.untab,                          # Shift + Tab
            "escape": self.escape,                        # Escape
            "single_selection": self.single_selection,    # Escape
            "clear_last_find": self.clear_last_find,      # Escape
            "new_cursor_up": self.new_cursor_up,          # Alt + Up
            "new_cursor_down": self.new_cursor_down,      # Alt + Down
            "new_cursor_left": self.new_cursor_left,      # Alt + Left
            "new_cursor_right": self.new_cursor_right,    # Alt + Right
            "page_up": self.page_up,                      # Page Up
            "page_down": self.page_down,                  # Page Down
            "push_up": self.push_up,                      # Alt + Page Up
            "push_down": self.push_down,                  # Alt + Page Down
            "undo": self.undo,                            # F5
            "redo": self.redo,                            # F6
            "toggle_line_nums": self.toggle_line_nums,    # F9
            "toggle_line_ends": self.toggle_line_ends,    # F10
            "toggle_highlight": self.toggle_highlight,    # F11
            "copy": self.copy,                            # Ctrl + C
            "cut": self.cut,                              # Ctrl + X
            "duplicate_line": self.duplicate_line,        # Ctrl + W
        }
        for key in operations.keys():
            self.operations[key] = operations[key]

    def set_buffer(self, buffer):
        """Sets local or global buffer depending on config."""
        if self.app.config["editor"]["use_global_buffer"]:
            self.app.global_buffer = buffer
        else:
            self.buffer = buffer

    def set_data(self, data):
        """Set the editor text contents."""
        Viewer.set_data(self, data)
        buffer = self.get_buffer()  # TODO: check this
        if len(buffer) > 1:
            self.store_state()
        else:
            state = State()
            state.store(self)
            self.history[0] = state

    def store_action_state(self, action, state=None):
        """Store the editor state if a new action is taken."""
        if self.last_action != action:
            self.last_action = action
            self.store_state(state)
        else:
            # FIXME: This if is here just for safety.
            # FIXME: current_state might be wrong ;.<
            if self.current_state < len(self.history)-1:
                self.history[self.current_state].store(self)

    def store_state(self, state=None, action=None):
        """Store the current editor state for undo/redo."""
        if state is None:
            state = State()
            state.store(self)
        if len(self.history) > 1:
            if self.current_state < len(self.history)-1:
                self.history = self.history[:self.current_state]

        self.history.append(state)
        self.current_state = len(self.history)-1

        if len(self.history) > self.config["max_history"]:
            self.history.pop(0)

    def restore_state(self, index=None):
        """Restore an editor state."""
        if len(self.history) <= 1:
            return False
        if index is None:
            index = self.current_state-1

        if index < 0 or index >= len(self.history):
            return False

        # if self.current_state < len(self.history):
        #     self.current_state = self.current_state-1

        state = self.history[index]
        state.restore(self)
        self.current_state = index

    def handle_input(self, event):
        done = Viewer.handle_input(self, event)
        if not done:
            if event.is_typeable:
                if isinstance(event.key_code, str):
                    self.type(event.key_code)
                elif event.key_name:
                    self.type(event.key_name)
                return True
        return False

    def undo(self):
        """Undo the last command or change."""
        self.last_action = "undo"
        self.restore_state()

    def redo(self):
        """Redo the last command or change."""
        self.last_action = "redo"
        if self.current_state == len(self.history)-1:
            return False
        index = self.current_state+1
        self.restore_state(index)

    #
    # Cursor operations
    #

    def new_cursor_up(self):
        """Add a new cursor one line up."""
        x = self.get_cursor().x
        cursor = self.get_first_cursor()
        if cursor.y == 0:
            return
        new = Cursor(x, cursor.y-1)
        self.cursors.append(new)
        self.move_cursors()
        self.scroll_up()

    def new_cursor_down(self):
        """Add a new cursor one line down."""
        x = self.get_cursor().x
        cursor = self.get_last_cursor()
        if cursor.y == len(self.lines)-1:
            return
        new = Cursor(x, cursor.y+1)
        self.cursors.append(new)
        self.move_cursors()
        self.scroll_down()

    def new_cursor_left(self):
        """Add a new cursor one character left."""
        new = []
        for cursor in self.cursors:
            if cursor.x == 0:
                continue
            new.append(Cursor(cursor.x-1, cursor.y))
        for c in new:
            self.cursors.append(c)
        self.move_cursors()
        self.scroll_up()

    def new_cursor_right(self):
        """Add a new cursor one character right."""
        new = []
        for cursor in self.cursors:
            if cursor.x+1 > len(self.lines[cursor.y]):
                continue
            new.append(Cursor(cursor.x+1, cursor.y))
        for c in new:
            self.cursors.append(c)
        self.move_cursors()
        self.scroll_down()

    def escape(self):
        """Handle escape key.

        Wrapper for clear_last_find and single_selection."""
        self.clear_last_find()
        self.single_selection()

    def clear_last_find(self):
        """Removes last_find so a new auto-find can be initiated."""
        self.last_find = ""

    def single_selection(self):
        """Removes all cursors except primary cursor."""
        self.cursors = [self.cursors[0]]
        self.move_cursors()

    #
    # Text editing operations
    #

    def replace_all(self, what, replacement):
        """Replaces what with replacement on each line."""
        for line in self.lines:
            data = line.get_data()
            new = data.replace(what, replacement)
            line.set_data(new)
        self.move_cursors()

    def delete(self):
        """Delete the next character."""
        for cursor in self.cursors:
            if len(self.lines)-1 < cursor.y:
                # If we've run out of lines
                break
            line = self.lines[cursor.y]
            # if we have more than 1 line
            # and we're at the end of the current line
            # and we're not on the last line
            if len(self.lines) > 1 and cursor.x == len(line) and cursor.y != len(self.lines) - 1:
                data = self.lines[cursor.y].get_data()
                self.lines.pop(cursor.y)
                self.lines[cursor.y].set_data(data+self.lines[cursor.y])
                # Reposition cursors from line below into correct positions on current line
                line_cursors = self.get_cursors_on_line(cursor.y+1)
                for c in line_cursors:
                    c.move_right(len(data))
                    c.move_up()
                self.move_y_cursors(cursor.y, -1)
            else:
                start = line[:cursor.x]
                end = line[cursor.x+1:]
                self.lines[cursor.y].set_data(start+end)
                self.move_x_cursors(cursor.y, cursor.x, -1)
        self.move_cursors()
        # Add a restore point if previous action != delete
        self.store_action_state("delete")

    def backspace(self):
        """Delete the previous character."""
        curs = reversed(sorted(self.cursors, key=lambda c: (c[1], c[0])))
        # Iterate through all cursors from bottom to top
        for cursor in curs:
            line_no = cursor.y
            # If we're at the beginning of file don't do anything
            if cursor.x == 0 and cursor.y == 0:
                continue
            # If were operating at the beginning of a line
            if cursor.x == 0 and cursor.y != 0:
                curr_line = self.lines.pop(line_no)
                prev_line = self.lines[line_no-1]
                length = len(prev_line)  # Get the length of previous line

                # Add the current line to the previous one
                new_data = self.lines[cursor.y-1] + curr_line
                self.lines[cursor.y-1].set_data(new_data)

                # Get all cursors on current line
                line_cursors = self.get_cursors_on_line(line_no)

                for line_cursor in line_cursors:  # Move the cursors
                    line_cursor.move_up()
                    # Add the length of previous line to each x coordinate
                    # so that their relative positions
                    line_cursor.move_right(length)
                # Move all cursors below up one line
                # (since a line was removed above them)
                self.move_y_cursors(cursor.y, -1)
            # Handle all other cases
            else:
                curr_line = self.lines[line_no]
                # Remove one character by default
                del_n_chars = 1
                # Check if we should unindent
                if self.config["backspace_unindent"]:
                    # Check if we can unindent, and that it's actually whitespace
                    # We don't do this for hard tabs since they're just a single character
                    if not self.config["hard_tabs"]:
                        indent = self.config["tab_width"]
                        if cursor.x >= indent:
                            if curr_line[cursor.x-indent:cursor.x] == indent*" ":
                                # Remove an indents worth of whitespace
                                del_n_chars = indent
                # Slice characters out of the line
                start = curr_line[:cursor.x-del_n_chars]
                end = curr_line[cursor.x:]
                # Store the new line
                self.lines[line_no].set_data(start+end)
                # Move the operating curser back the deleted amount
                cursor.move_left(del_n_chars)
                # Do the same to the rest
                self.move_x_cursors(line_no, cursor.x, -1*del_n_chars)
        # Ensure we keep the view scrolled
        self.move_cursors()
        self.scroll_up()
        # Add a restore point if previous action != backspace
        self.store_action_state("backspace")

    def enter(self):
        """Insert a new line at each cursor."""
        # We sort the cursors, and loop through them from last to first
        # That way we avoid messing with
        # the relative positions of the higher cursors
        curs = sorted(self.cursors, key=lambda c: (c[1], c[0]))
        curs = reversed(curs)
        for cursor in curs:
            # The current line this cursor is on
            line = self.lines[cursor.y]

            # Start of the line
            start = line[:cursor.x]

            # End of the line
            end = line[cursor.x:]

            # Leave the beginning of the line
            self.lines[cursor.y].set_data(start)
            wspace = ""
            if self.config["auto_indent_newline"]:
                wspace = helpers.whitespace(self.lines[cursor.y])*" "
            self.lines.insert(cursor.y+1, Line(wspace+end))
            self.move_y_cursors(cursor.y, 1)
            cursor.set_x(len(wspace))
            cursor.move_down()
        self.move_cursors()
        self.scroll_down()
        # Add a restore point if previous action != enter
        self.store_action_state("enter")

    def insert(self):
        """Insert buffer data at cursor(s)."""
        cur = self.get_cursor()
        buffer = list(self.get_buffer())

        # If we have more than one cursor
        # Or one cursor and one line
        if len(self.cursors) > 1 or len(buffer) == 1:
            # If the cursor count is more than the buffer length extend
            # the buffer until it's at least as long as the cursor count
            while len(buffer) < len(self.cursors):
                buffer.extend(buffer)
            curs = sorted(self.cursors, key=lambda c: (c[1], c[0]))
            for cursor in curs:
                line = self.lines[cursor.y]
                buf = buffer[0]
                line = line[:cursor.x] + buf + line[cursor.x:]
                self.lines[cursor.y].set_data(line)
                buffer.pop(0)
                self.move_x_cursors(cursor.y, cursor.x-1, len(buf))
        # If we have one cursor and multiple lines
        else:
            for buf in buffer:
                y = cur[1]
                if y < 0:
                    y = 0
                self.lines.insert(y, Line(buf))
                self.move_y_cursors(cur[1]-1, 1)
        self.move_cursors()
        self.scroll_down()
        # Add a restore point if previous action != insert
        self.store_action_state("insert")

    def insert_lines_at(self, lines, at):
        rev_lines = reversed(lines)
        for line in rev_lines:
            self.lines.insert(at, Line(line))
        self.move_y_cursors(at, len(lines))

    def push_up(self):
        """Move current lines up by one line."""
        used_y = []
        curs = sorted(self.cursors, key=lambda c: (c[1], c[0]))
        for cursor in curs:
            if cursor.y in used_y:
                continue
            used_y.append(cursor.y)
            if cursor.y == 0:
                break
            old = self.lines[cursor.y-1]
            self.lines[cursor.y-1] = self.lines[cursor.y]
            self.lines[cursor.y] = old
        self.move_cursors((0, -1))
        self.scroll_up()
        # Add a restore point if previous action != push_up
        self.store_action_state("push_up")

    def push_down(self):
        """Move current lines down by one line."""
        used_y = []
        curs = reversed(sorted(self.cursors, key=lambda c: (c[1], c[0])))
        for cursor in curs:
            if cursor.y in used_y:
                continue
            if cursor.y >= len(self.lines)-1:
                break
            used_y.append(cursor.y)
            old = self.lines[cursor.y+1]
            self.lines[cursor.y+1] = self.lines[cursor.y]
            self.lines[cursor.y] = old

        self.move_cursors((0, 1))
        self.scroll_down()
        # Add a restore point if previous action != push_down
        self.store_action_state("push_down")

    def tab(self):
        """Indent lines."""
        # Add a restore point if previous action != tab
        self.store_action_state("tab")
        if not self.config["hard_tabs"]:
            self.type(" "*self.config["tab_width"])
        else:
            self.type("\t")

    def untab(self):
        """Unindent lines."""
        linenums = []
        # String to compare tabs to
        tab = " "*self.config["tab_width"]
        if self.config["hard_tabs"]:
            tab = "\t"
        width = len(tab)
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            if cursor.y in linenums:
                cursor.x = helpers.whitespace(line)
                continue
            elif line[:width] == tab:
                line = Line(line[width:])
                self.lines[cursor.y] = line
                cursor.x = helpers.whitespace(line)
                linenums.append(cursor.y)
        # Add a restore point if previous action != untab
        self.store_action_state("untab")

    def copy(self):
        """Copy lines to buffer."""
        # Store cut lines in buffer
        copy_buffer = []
        # Get all lines with cursors on them
        line_nums = self.get_lines_with_cursors()
        i = 0
        while i < len(line_nums):
            # Get the line
            line = self.lines[line_nums[i]]
            # Put it in our temporary buffer
            copy_buffer.append(line.get_data())
            i += 1
        self.set_buffer(copy_buffer)
        self.store_action_state("copy")

    def cut(self):
        """Cut lines to buffer."""
        # Store cut lines in buffer
        cut_buffer = []
        # Get all lines with cursors on them
        line_nums = self.get_lines_with_cursors()
        # Sort from last to first (invert order)
        line_nums = line_nums[::-1]
        i = 0
        while i < len(line_nums):  # Iterate from last to first
            # Make sure we don't completely remove the last line
            if len(self.lines) == 1:
                cut_buffer.append(self.lines[0])
                self.lines[0] = Line()
                break
            # Get the current line
            line_no = line_nums[i]
            # Get and remove the line
            line = self.lines.pop(line_no)
            # Put it in our temporary buffer
            cut_buffer.append(line)
            # Move all cursors below the current line up
            self.move_y_cursors(line_no, -1)
            i += 1
        self.move_cursors()  # Make sure cursors are in valid places
        # Reverse the buffer to get correct order and store it
        self.set_buffer(cut_buffer[::-1])
        self.store_action_state("cut")

    def type(self, data):
        """Insert data at each cursor position."""
        for cursor in self.cursors:
            self.type_at_cursor(cursor, data)
        self.move_cursors()
        # Add a restore point if previous action != type
        self.store_action_state("type")

    def type_at_cursor(self, cursor, data):
        """Insert data at specified cursor."""
        line = self.lines[cursor.y]
        start = line[:cursor.x]
        end = line[cursor.x:]
        self.lines[cursor.y].set_data(start + data + end)
        self.move_x_cursors(cursor.y, cursor.x, len(data))
        cursor.move_right(len(data))

    def go_to_pos(self, line_no, col=0):
        """Move primary cursor to line_no, col=0."""
        if line_no < 0:
            line_no = len(self.lines)-1
        else:
            line_no = line_no-1

        self.store_state()
        cur = self.get_cursor()
        if col is not None:
            cur.x = col
        cur.y = line_no
        if cur.y >= len(self.lines):
            cur.y = len(self.lines)-1
        self.scroll_to_line(cur.y)
        self.move_cursors()

    def duplicate_line(self):
        """Copy current line and add it below as a new line."""
        curs = sorted(self.cursors, key=lambda c: (c.y, c.x))
        for cursor in curs:
            line = Line(self.lines[cursor.y])
            self.lines.insert(cursor.y+1, line)
            self.move_y_cursors(cursor.y, 1)
        self.move_cursors()
        self.store_action_state("duplicate_line")
