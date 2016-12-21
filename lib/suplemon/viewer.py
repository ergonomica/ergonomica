# -*- encoding: utf-8
"""
Text viewer component subclassed by Editor.
"""

import os
import re
import sys
import curses
import logging
try:
    import importlib
except ImportError:
    importlib = False

from . import helpers

from .line import Line
from .cursor import Cursor
from .themes import scope_to_pair
import suplemon.linelight  # NOQA

try:
    import pygments.lexers
    from .lexer import Lexer
except ImportError:
    pygments = False


class BaseViewer:
    def __init__(self, app, window):
        """
        Handle Viewer initialization

        :param App app: The main App class of Suplemon
        :param Window window: The ui window to use for the viewer
        """
        self.app = app
        self.window = window
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.data = ""
        self.lines = [Line()]
        self.file_extension = ""

        # Map special extensions to generic ones for highlighting
        self.extension_map = {
            "scss": "css",
            "less": "css",
            "tmtheme": "xml",
            "ts": "js",
        }
        self.show_line_ends = True

        self.cursor_style = curses.A_UNDERLINE

        self.y_scroll = 0
        self.x_scroll = 0
        self.cursors = [Cursor()]

        # Copy/paste buffer
        self.buffer = []

        # Last search used in 'find'
        self.last_find = ""

        # Runnable methods
        self.operations = {
            "arrow_right": self.arrow_right,              # Arrow Right
            "arrow_left": self.arrow_left,                # Arrow Left
            "arrow_up": self.arrow_up,                    # Arrow Up
            "arrow_down": self.arrow_down,                # Arrow Down
            "jump_left": self.jump_left,                  # Ctrl + Left
            "jump_right": self.jump_right,                # Ctrl + Right
            "jump_up": self.jump_up,                      # Ctrl + Up
            "jump_down": self.jump_down,                  # Ctrl + Down
            "page_up": self.page_up,                      # Page Up
            "page_down": self.page_down,                  # Page Down
            "home": self.home,                            # Home
            "end": self.end,                              # End
            "find": self.find_query,                      # Ctrl + F
            "find_next": self.find_next,                  # Ctrl + D
            "find_all": self.find_all,                    # Ctrl + A
        }

    def init(self):
        pass

    def get_buffer(self):
        """Returns the current buffer.

        Returns the local buffer or the global buffer depending on config.
        """
        if self.config["use_global_buffer"]:
            return self.app.global_buffer
        else:
            return self.buffer

    def get_size(self):
        """Get editor size (x,y)."""
        y, x = self.window.getmaxyx()
        return (x, y)

    def get_scroll_pos(self):
        return (self.y_scroll, self.x_scroll)

    def get_y_scroll(self):
        return self.y_scroll

    def get_x_scroll(self):
        return self.x_scroll

    def get_cursor(self):
        """Return the main cursor."""
        return self.cursors[0]

    def get_cursors(self):
        """Return list of all cursors."""
        return self.cursors

    def get_first_cursor(self):
        """Get the first (primary) cursor."""
        highest = None
        for cursor in self.cursors:
            if highest is None or cursor.y < highest.y:
                highest = cursor
        return highest

    def get_last_cursor(self):
        """Get the last cursor."""
        lowest = None
        for cursor in self.cursors:
            if lowest is None:
                lowest = cursor
            elif cursor.y > lowest.y:
                lowest = cursor
            elif cursor.y == lowest.y and cursor.x > lowest.x:
                lowest = cursor
        return lowest

    def get_cursors_on_line(self, line_no):
        """Return all cursors on a specific line."""
        cursors = []
        for cursor in self.cursors:
            if cursor.y == line_no:
                cursors.append(cursor)
        return cursors

    def get_line(self, n):
        """Return line at index n.

        :param n: Index of line to get.
        :return: The Line instance.
        """
        return self.lines[n]

    def get_lines_with_cursors(self):
        """Return all line indices that have cursors.

        :return: A list of line numbers that have cursors.
        :rtype: list
        """
        line_nums = []
        for cursor in self.cursors:
            if cursor.y not in line_nums:
                line_nums.append(cursor.y)
        line_nums.sort()
        return line_nums

    def get_data(self):
        """Get editor contents.

        :return: Editor contents.
        :rtype: str
        """
        str_lines = []
        for line in self.lines:
            if isinstance(line, str):
                str_lines.append(line)
            else:
                str_lines.append(line.get_data())
        data = str(self.config["end_of_line"].join(str_lines))
        return data

    def set_data(self, data):
        """Set editor data or contents.

        :param str data: Set the editor contents to data.
        """
        self.data = data
        self.lines = []
        lines = self.data.splitlines()
        # splitlines doesn't return the last line if it's empty so we add a line
        # if there we're no lines at all or if the data ends with a new line
        if not len(lines) or self.data.endswith(("\n", "\r\n", "\r")):
            lines.append(Line())
        for line in lines:
            self.lines.append(Line(line))

    def set_config(self, config):
        """Set the viewer configuration dict.

        :param dict config: Editor config dict with any supported fields. See config.py.
        """
        self.config = config
        self.set_cursor_style(self.config["cursor_style"])

    def set_scroll_pos(self, pos):
        self.y_scroll = pos[0]
        self.x_scroll = pos[1]

    def set_cursor_style(self, cursor_style):
        """Set cursor style.

        :param str cursor_style: Cursor type, either 'underline' or 'reverse'.
        """
        if cursor_style == "underline":
            self.cursor_style = curses.A_UNDERLINE
        elif cursor_style == "reverse":
            self.cursor_style = curses.A_REVERSE
        else:
            return False
        return True

    def set_cursor(self, cursor):
        self.logger.warning("set_cursor is deprecated, use set_cursor_style instead.")
        return self.set_cursor_style(cursor)

    def set_cursors(self, cursors):
        """Return list of all cursors."""
        self.cursors = [Cursor(c) for c in cursors]

    def set_single_cursor(self, cursor):
        """Discard all cursors and place a new one."""
        self.cursors = [Cursor(cursor)]

    def set_file_extension(self, ext):
        """Set the file extension."""
        ext = ext.lower()
        if ext and ext != self.file_extension:
            self.file_extension = ext
            self.setup_linelight()
            if self.config["show_highlighting"]:
                self.setup_highlight()

    def add_cursor(self, cursor):
        """Add a new cursor. Accepts a x,y tuple or a Cursor instance."""
        self.cursors.append(Cursor(cursor))

    def pad_lnum(self, n):
        """Pad line number with zeroes."""
        # TODO: move to helpers
        s = str(n)
        while len(s) < self.line_offset()-1:
            s = "0" + s
        return s

    def max_line_length(self):
        """Get maximum line length that fits in the editor."""
        return self.get_size()[0]-self.line_offset()-1

    def line_offset(self):
        """Get the x coordinate of beginning of line."""
        if not self.config["show_line_nums"]:
            return 0
        return len(str(len(self.lines)))+1

    def toggle_line_nums(self):
        """Toggle display of line numbers."""
        self.config["show_line_nums"] = not self.config["show_line_nums"]
        self.render()

    def toggle_line_ends(self):
        """Toggle display of line ends."""
        self.show_line_ends = not self.show_line_ends
        self.render()

    def toggle_highlight(self):
        """Toggle syntax highlighting."""
        return False

    ###########################################################################
    # Curses
    ###########################################################################

    def move_win(self, yx):
        """Move the editor window to position yx."""
        # Must try & catch since mvwin might
        # crash with incorrect coordinates
        try:
            self.window.mvwin(yx[0], yx[1])
        except:
            self.logger.warning("Moving window failed!", exc_info=True)

    def refresh(self):
        """Refresh the editor curses window."""
        self.move_cursors()
        self.render()
        self.window.refresh()

    def resize(self, yx=None):
        """Resize the UI."""
        if not yx:
            yx = self.window.getmaxyx()
        self.window.resize(yx[0], yx[1])
        self.move_cursors()
        self.refresh()

    def render(self):
        """Render the editor curses window."""
        if self.app.block_rendering:
            return

        self.window.erase()
        i = 0
        max_y = self.get_size()[1]
        max_len = self.max_line_length()
        # Iterate through visible lines
        while i < max_y:
            x_offset = self.line_offset()
            lnum = i + self.y_scroll
            if lnum >= len(self.lines):  # Make sure we have a line to show
                break
            # Get line for current row
            line = self.lines[lnum]
            if self.config["show_line_nums"]:
                curs_color = curses.color_pair(line.number_color)
                self.window.addstr(i, 0, self.pad_lnum(lnum+1)+" ", curs_color)

            pos = (x_offset, i)
            try:
                self.render_line_contents(line, pos, x_offset, max_len)
            except:
                self.logger.error("Failed rendering line #{0} @{1} DATA:'{2}'!".format(lnum+1, pos, line),
                                  exc_info=True)
            i += 1
        self.render_cursors()

    def render_line_contents(self, line, pos, x_offset, max_len):
        """Render the contents of a line to the screen

        Renders a line to the screen with the appropriate rendering method
        based on settings.

        :param line: Line instance to render.
        :param pos: Position (x, y) for beginning of line.
        :param x_offset: Offset from left edge of screen. Currently same as x position.
        :param max_len: Maximum amount of chars that will fit on screen.
        """
        show_highlighting = self.config["show_highlighting"]
        if pygments and show_highlighting and self.pygments_syntax and self.app.themes.current_theme:
            self.render_line_pygments(line, pos, x_offset, max_len)
        elif self.config["show_line_colors"]:
            self.render_line_linelight(line, pos, x_offset, max_len)
        else:
            self.render_line_normal(line, pos, x_offset, max_len)

    def render_line_pygments(self, line, pos, x_offset, max_len):
        """Render line with Pygments syntax highlighting."""
        x, y = pos
        line_data = line.get_data()
        # Lazily prepare and slice the line,
        # even though it affects highlighting.
        line_data = self._prepare_line_for_rendering(line_data,
                                                     max_len,
                                                     no_wspace=True)
        # TODO:
        # 1) The line should not be prepared for rendering like this
        #    because it can get sliced. Sliced lines won't always get
        #    completely highlighted (partial words). Syntax highlighting
        #    should be done first and then only render visible words.
        # 2) Additionaly highlighing should be done for all lines at once
        #    and tokens should be cached in line instances. That way we can
        #    support multi line comment syntax etc. It should also perform
        #    better, since we only need to re-highlight lines when they change.
        # TODO 2: Optimize lexer performance
        tokens = self.lexer.lex(line_data, self.pygments_syntax)
        first_token = True
        for token in tokens:
            if token[1] == "\n":
                break
            scope = token[0]
            text = self.replace_whitespace(token[1])
            if token[1].isspace() and not self.app.ui.limited_colors:
                pair = 9  # Default to gray text on normal background
                settings = self.app.themes.get_scope("global")
                if settings and settings.get("invisibles"):
                    fg = int(settings.get("invisibles") or -1)
                    bg = int(settings.get("background") or -1)
                    curses.init_pair(pair, fg, bg)
                curs_color = curses.color_pair(pair)
                # Only add tab indicators to the inital whitespace
                if first_token and self.config["show_tab_indicators"]:
                    text = self.add_tab_indicators(text)
                self.window.addstr(y, x_offset, text, curs_color)
            else:
                # Color with pygments
                settings = self.app.themes.get_scope(scope)
                pair = scope_to_pair.get(scope)
                if settings and pair is not None:
                    fg = int(settings.get("foreground") or -1)
                    bg = int(settings.get("background") or -1)
                    curses.init_pair(pair, fg, bg)
                    curs_color = curses.color_pair(pair)
                    self.window.addstr(y, x_offset, text, curs_color)
                else:
                    self.window.addstr(y, x_offset, text)
            if first_token:
                first_token = False
            x_offset += len(text)

    def render_line_linelight(self, line, pos, x_offset, max_len):
        """Render line with naive line based highlighting."""
        y = pos[1]
        line_data = line.get_data()
        line_data = self._prepare_line_for_rendering(line_data, max_len)
        curs_color = curses.color_pair(self.get_line_color(line))
        self.window.addstr(y, x_offset, line_data, curs_color)

    def render_line_normal(self, line, pos, x_offset, max_len):
        """Render line without any highlighting."""
        y = pos[1]
        line_data = line.get_data()
        line_data = self._prepare_line_for_rendering(line_data, max_len)
        self.window.addstr(y, x_offset, line_data)

    def add_tab_indicators(self, data):
        new_data = ""
        i = 0
        for char in data:
            if i == 0:
                new_data += self.config["tab_indicator_character"]
            else:
                new_data += char
            i += 1
            if i > self.config["tab_width"]-1:
                i = 0
        return new_data

    def replace_whitespace(self, data):
        # TODO: Optimize performance
        """Replace unsafe whitespace with alternative safe characters

        Replace unsafe whitespace with normal space or visible replacement.
        For example tab characters make cursors go out of sync with line
        contents.
        """
        for key in self.config["white_space_map"]:
            char = " "
            if self.config["show_white_space"]:
                char = self.config["white_space_map"][key]
            data = data.replace(key, char)
        # Remove newlines, they cause curses errors
        data = data.replace("\n", "")
        return data

    def _prepare_line_for_rendering(self, line_data, max_len, no_wspace=False):
        if self.show_line_ends:
            line_data += self.config["line_end_char"]
        line_data = self._slice_line_for_rendering(line_data, max_len)
        if not no_wspace:
            line_data = self.replace_whitespace(line_data)

        # Use unicode support on Python 3.3 and higher
        if sys.version_info[0] == 3 and sys.version_info[1] > 2:
            line_data = line_data.encode("utf-8")
        return line_data

    def _slice_line_for_rendering(self, line, max_len):
        """Return sliced line data.

        Returns what's left of line data after scrolling it horizontally
        and removing excess characters from the end.

        :param line: Line to slice.
        :param max_len: Maximum length of line.
        :return: Sliced line.
        """
        line = line[min(self.x_scroll, len(line)):]
        if not line:
            return ""
        # Clamp line length to view width
        line = line[:min(len(line), max_len)]
        return line

    def render_cursors(self):
        """Render editor window cursors."""
        if self.app.block_rendering:
            return

        max_x, max_y = self.get_size()
        for cursor in self.cursors:
            x = cursor.x - self.x_scroll + self.line_offset()
            y = cursor.y - self.y_scroll
            if y < 0:
                continue
            if y >= max_y:
                break
            if x < self.line_offset():
                continue
            if x > max_x-1:
                continue
            self.window.chgat(y, cursor.x+self.line_offset()-self.x_scroll, 1, self.cursor_style)

    ###########################################################################
    # Scrolling
    ###########################################################################

    def scroll_up(self):
        """Scroll view up if neccesary."""
        cursor = self.get_first_cursor()
        if cursor.y - self.y_scroll < 0:
            # Scroll up
            self.y_scroll = cursor.y

    def scroll_down(self):
        """Scroll view up if neccesary."""
        cursor = self.get_last_cursor()
        size = self.get_size()
        if cursor.y - self.y_scroll >= size[1]:
            # Scroll down
            self.y_scroll = cursor.y - size[1]+1

    def scroll_to_line(self, line_no):
        """Center the viewport on line_no."""
        if line_no >= len(self.lines):
            line_no = len(self.lines)-1
        new_y = line_no - int(self.get_size()[1] / 2)
        if new_y < 0:
            new_y = 0
        self.y_scroll = new_y

    def move_y_scroll(self, delta):
        """Add delta the y scroll axis scroll"""
        self.y_scroll += delta

    ###########################################################################
    # Cursors
    ###########################################################################

    def move_cursors(self, delta=None):
        """Move all cursors with delta. To avoid refreshing the screen set noupdate to True."""
        for cursor in self.cursors:
            if delta:
                if delta[0] != 0 and cursor.x >= 0:
                    cursor.move_right(delta[0])
                if delta[1] != 0 and cursor.y >= 0:
                    cursor.move_down(delta[1])

            if cursor.x < 0:
                cursor.x = 0
            if cursor.y < 0:
                cursor.y = 0
            if cursor.y >= len(self.lines)-1:
                cursor.y = len(self.lines)-1
            if cursor.x >= len(self.lines[cursor.y]):
                cursor.x = len(self.lines[cursor.y])
            elif cursor.persistent_x != cursor.x:
                # Retain the 'desired' x coordinate
                cursor.x = min(cursor.persistent_x, len(self.lines[cursor.y]))

        cur = self.get_cursor()  # Main cursor
        size = self.get_size()
        offset = self.line_offset()
        # Check if we should scroll horizontally
        if cur.x - self.x_scroll+offset > size[0] - 1:
            # -1 to allow space for cursor at line end
            self.x_scroll = len(self.lines[cur.y]) - size[0]+offset+1
        if cur.x - self.x_scroll < 0:
            self.x_scroll -= abs(cur.x - self.x_scroll)  # FIXME
        if cur.x - self.x_scroll+offset < offset:
            self.x_scroll -= 1
        self.purge_cursors()

    def move_x_cursors(self, line, col, delta):
        """Move all cursors starting at line and col with delta on the x axis."""
        for cursor in self.cursors:
            if cursor.y == line:
                if cursor.x > col:
                    cursor.move_right(delta)

    def move_y_cursors(self, line, delta, exclude=None):
        """Move all cursors starting at line and col with delta on the y axis.
        Exclude a cursor by passing it via the exclude argument."""
        for cursor in self.cursors:
            if cursor == exclude:
                continue
            if cursor.y > line:
                cursor.move_down(delta)

    def cursor_exists(self, cursor):
        """Check if a given cursor exists."""
        return cursor.tuple() in [cur.tuple() for cur in self.cursors]

    def remove_cursor(self, cursor):
        """Remove a cursor object from the cursor list."""
        try:
            index = self.cursors.index(cursor)
        except:
            return False
        self.cursors.pop(index)
        return True

    def purge_cursors(self):
        """Remove duplicate cursors that have the same position."""
        new = []
        # This sucks: can't use "if .. in .." for different instances (?)
        # Use a reference list instead. FIXME: use a generator
        ref = []
        for cursor in self.cursors:
            if not cursor.tuple() in ref:
                ref.append(cursor.tuple())
                new.append(cursor)
        self.cursors = new

    def purge_line_cursors(self, line_no):
        """Remove all but first cursor on given line."""
        line_cursors = []
        for cursor in self.cursors:
            if cursor.y == line_no:
                line_cursors.append(cursor)
        if len(line_cursors) < 2:
            return False

        # Leave the first cursor out
        line_cursors.pop(0)
        # Remove the rest
        for line_cursors in cursor:
            self.remove_cursor(cursor)
        return True

    ###########################################################################
    # Input Handling
    ###########################################################################

    def get_key_bindings(self):
        """Get list of editor key bindings."""
        return self.app.get_key_bindings()

    def handle_input(self, event):
        """Handle input."""
        if event.type == "mouse":
            return False
        key = event.key_code
        name = event.key_name
        # Try match a key to a method and call it

        key_bindings = self.get_key_bindings()
        operation = None
        if key in key_bindings:
            operation = key_bindings[key]
        elif name in key_bindings:
            operation = key_bindings[name]
        if operation:
            self.run_operation(operation)
            return True
        return False

    def run_operation(self, operation):
        """Run an editor core operation."""
        if operation in self.operations:
            cancel = self.app.trigger_event_before(operation)
            if cancel:
                return False
            result = self.operations[operation]()
            self.app.trigger_event_after(operation)
            return result
        return False

    ###########################################################################
    # Operations
    ###########################################################################

    def arrow_right(self):
        """Move cursors right."""
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            # If we are at the end of the line
            if cursor.x >= len(line) or len(line) == 0:
                # If there is another line, then move down
                if cursor.y != len(self.lines)-1:
                    cursor.move_down()
                    cursor.set_x(0)
            # Otherwise, move the cursor right
            else:
                cursor.move_right()
        self.move_cursors()
        self.scroll_down()

    def arrow_left(self):
        """Move cursors left."""
        for cursor in self.cursors:
            if cursor.y != 0 and cursor.x == 0:
                cursor.move_up()
                cursor.set_x(len(self.lines[cursor.y])+1)
        self.move_cursors((-1, 0))
        self.scroll_up()

    def arrow_up(self):
        """Move cursors up."""
        self.move_cursors((0, -1))
        self.scroll_up()

    def arrow_down(self):
        """Move cursors down."""
        self.move_cursors((0, 1))
        self.scroll_down()

    def home(self):
        """Move to start of line or text on that line."""
        for cursor in self.cursors:
            wspace = helpers.whitespace(self.lines[cursor.y])
            if cursor.x == wspace:
                cursor.set_x(0)
            else:
                cursor.set_x(wspace)
        self.move_cursors()

    def end(self):
        """Move to end of line."""
        for cursor in self.cursors:
            cursor.set_x(len(self.lines[cursor.y]))
        self.move_cursors()

    def page_up(self):
        """Move half a page up."""
        amount = int(self.get_size()[1]/2) * -1
        self.move_cursors((0, amount))
        self.scroll_up()

    def page_down(self):
        """Move half a page down."""
        amount = int(self.get_size()[1]/2)
        self.move_cursors((0, amount))
        self.scroll_down()

    def jump_left(self):
        """Jump one 'word' to the left."""
        chars = self.config["punctuation"]
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            if cursor.x == 0:
                if cursor.y > 0:
                    # Jump to end of previous line
                    cursor.set_x(len(self.lines[cursor.y-1]))
                    cursor.move_up()
                continue
            if cursor.x <= len(line):
                cur_chr = line[cursor.x-1]
            else:
                cur_chr = line[cursor.x]
            while cursor.x > 0:
                next = cursor.x-2
                if next < 0:
                    next = 0
                if cur_chr == " ":
                    cursor.move_left()
                    if line[next] != " ":
                        break
                else:
                    cursor.move_left()
                    if line[next] in chars:
                        break
        self.move_cursors()

    def jump_right(self):
        """Jump one 'word' to the right."""
        chars = self.config["punctuation"]
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            if cursor.x == len(line):
                if cursor.y < len(self.lines):
                    # Jump to start of next line
                    cursor.set_x(0)
                    cursor.move_down()
                continue
            cur_chr = line[cursor.x]
            while cursor.x < len(line):
                next = cursor.x+1
                if next == len(line):
                    next -= 1
                if cur_chr == " ":
                    cursor.move_right()
                    if line[next] != " ":
                        break
                else:
                    cursor.move_right()
                    if line[next] in chars:
                        break
        self.move_cursors()

    def jump_up(self):
        """Jump up 3 lines."""
        self.move_cursors((0, -3))
        self.scroll_up()

    def jump_down(self):
        """Jump down 3 lines."""
        self.move_cursors((0, 3))
        self.scroll_down()

    def find_query(self):
        """Find in file via user input."""
        what = self.app.ui.query("Find:", self.last_find)
        if what:
            self.find(what)

    def find(self, what, findall=False):
        """Find what in data (from top to bottom). Adds a cursor when found."""
        # Sorry for this colossal function
        if not what:
            return
        last_cursor = self.get_last_cursor()
        y = last_cursor.y

        found = False
        new_cursors = []
        # Loop through all lines starting from the last cursor
        while y < len(self.lines):
            line = self.lines[y]
            x_offset = 0  # Which character to begin searching from
            if y == last_cursor.y:
                # On the current line begin from the last cursor x pos
                x_offset = last_cursor.x

            # Find all occurances of search string
            s = str(line[x_offset:])  # Data to search in
            if y < len(self.lines)-1:  # Make line breaks findable (add them to all except last line)
                s = s + "\n"
            pattern = re.escape(what)  # Default to non regex pattern
            if self.config["regex_find"]:
                try:  # Try to search with the actual regex
                    indices = [match.start() for match in re.finditer(what, s)]
                except:  # Revert to normal search
                    indices = [match.start() for match in re.finditer(pattern, s)]
            else:
                # Use normal search
                indices = [match.start() for match in re.finditer(pattern, s)]

            # Loop through the indices and add cursors if they don't exist yet
            for i in indices:
                new = Cursor(i+x_offset, y)
                if not self.cursor_exists(new):
                    found = True
                    if new not in new_cursors:  # Make sure we don't get duplicates
                        new_cursors.append(new)
                    if not findall:
                        break
                if new not in new_cursors:
                    new_cursors.append(new)
            if found and not findall:
                break
            y += 1

        if not new_cursors:
            self.app.set_status("Can't find '{0}'".format(what))
            return False
        else:
            # If we only have one cursor, and it's not
            # where the first occurance is, just remove it
            if len(self.cursors) == 1 and self.cursors[0].tuple() != new_cursors[0].tuple():
                self.cursors = []
        self.last_find = what   # Only store string if it's really found

        # Add the new cursors
        for cursor in new_cursors:
            if not self.cursor_exists(cursor):
                self.cursors.append(cursor)

        destination = self.get_last_cursor().y
        self.scroll_to_line(destination)
        self.store_action_state("find")  # Store undo point

    def find_next(self):
        """Find next occurance."""
        what = self.last_find
        if what == "":
            cursor = self.get_cursor()
            search = "^([\w\-]+)"
            line = self.lines[cursor.y][cursor.x:]
            matches = re.match(search, line)
            if matches:
                what = matches.group(0)
            else:
                if line:
                    what = line[0]
            # Escape the data if regex is enabled
            if self.config["regex_find"]:
                what = re.escape(what)
            self.last_find = what
        self.find(what)

    def find_all(self):
        """Find all occurances."""
        self.find(self.last_find, True)


class Viewer(BaseViewer):
    def __init__(self, app, window):
        BaseViewer.__init__(self, app, window)

        # Lexer for translating tokens to strings
        self.lexer = None
        # Built in syntax definition (for commenting etc.)
        self.syntax = None
        # Normal Pygments lexer
        self.pygments_syntax = None

        self.setup_linelight()

    def init(self):
        if self.config["show_highlighting"]:
            self.setup_highlight()

    def setup_linelight(self):
        """Setup line based highlighting."""
        ext = self.file_extension
        # Check if a file extension is redefined
        # Maps e.g. 'scss' to 'css'
        if ext in self.extension_map:
            ext = self.extension_map[ext]  # Use it
        curr_path = os.path.dirname(os.path.realpath(__file__))

        filename = ext + ".py"
        path = os.path.join(curr_path, "linelight", filename)
        module = False
        syntax_module_name = ".{0}".format(ext)
        if importlib and os.path.isfile(path):
            try:
                module = importlib.import_module(syntax_module_name, "suplemon.linelight")
            except:
                self.logger.error("Failed to load syntax file '{0}'!".format(path), exc_info=True)
        else:
            return False

        if not module or "Syntax" not in dir(module):
            self.logger.error("File doesn't match API!")
            return False
        self.syntax = module.Syntax()

    def setup_highlight(self):
        """Setup Pygments based highlighting."""
        if not pygments:
            return False
        self.lexer = Lexer(self.app)
        ext = self.file_extension.lower()
        if not ext:
            return False
        # Don't use Pygments for diffs. The text mate themes that are used don't often support it properly.
        # It's also such a basic format that it's justified to fall back on line based highlighting.
        if ext == "diff":
            return False
        # Check if a file extension is redefined
        # Maps e.g. 'scss' to 'css'
        if ext in self.extension_map:
            ext = self.extension_map[ext]  # Use it
        try:
            self.pygments_syntax = pygments.lexers.get_lexer_by_name(ext)
            self.logger.debug("Loaded Pygments lexer '{0}'.".format(ext))
        except:
            self.logger.debug("Failed to load Pygments lexer '{0}'.".format(ext))
            return False
        if ext == "php":
            # Hack to highlight PHP even without <?php ?> tags
            self.pygments_syntax.options.update({"startinline": 1})
            self.pygments_syntax.startinline = 1

    def get_line_color(self, raw_line):
        """Return a color based on line contents.

        :param str raw_line: The line from which to get a color value.
        :return: A color value for given raw_data.
        :rtype: int
        """
        if self.syntax:
            color = self.syntax.get_color(raw_line)
            if color is not None:
                return color
        return 0
