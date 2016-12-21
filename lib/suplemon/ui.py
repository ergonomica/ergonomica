# -*- encoding: utf-8
"""
Curses user interface.
"""

import os
import sys
import logging

from .prompt import Prompt, PromptBool, PromptFile
from .key_mappings import key_map

# Curses can't be imported yet but we'll
# predefine it to avoid confusing flake8
curses = None


class InputEvent:
    """Represents a keyboard or mouse event."""
    def __init__(self):
        self.type = None  # 'key' or 'mouse'
        self.key_name = None
        self.key_code = None
        self.is_typeable = False
        self.curses_key_name = None
        self.mouse_code = None
        self.mouse_pos = (0, 0)
        self.logger = logging.getLogger("{0}.InputEvent".format(__name__))

    def parse_key_code(self, key_code):
        """Parse a key code (or character) from curses."""
        self.type = "key"
        self.key_code = key_code
        self.key_name = self._key_name(key_code)
        self.curses_key_name = self._curses_key_name(key_code)

    def set_key_name(self, name):
        """Manually set the event key name."""
        self.type = "key"
        self.key_name = name

    def parse_mouse_state(self, state):
        """Parse curses mouse events."""
        self.type = "mouse"
        self.mouse_code = state[4]
        self.mouse_pos = (state[1], state[2])

    def _key_name(self, key_code):
        """Return a normalized key name for key_code."""
        if isinstance(key_code, int):
            if key_code in key_map.keys():
                return key_map[key_code]
        curs_key_name = self._curses_key_name(key_code)
        if curs_key_name:
            if curs_key_name in key_map.keys():
                return key_map[curs_key_name]
            self.is_typeable = True  # We'll assume the key is typeable if it's not found in the key map
            return curs_key_name
        else:
            char = None
            if key_code in key_map.keys():
                return key_map[key_code]

            if sys.version_info[0] >= 3:
                if isinstance(key_code, str):
                    self.is_typeable = True
                    return key_code

            try:
                char = chr(key_code)
            except:
                pass
            if char is not None:
                self.is_typeable = True
                return char
        return False

    def _curses_key_name(self, key):
        """Return the curses key name for keys received from get_wch (and getch)."""
        # Handle multibyte get_wch input in Python 3.3
        if isinstance(key, str):
            return str(curses.keyname(ord(key)).decode("utf-8"))
        # Fallback to try and handle Python < 3.3
        # Special keys can also be ints on Python > 3.3
        if isinstance(key, int):  # getch fallback
            try:  # Try to convert to a curses key name
                name = str(curses.keyname(key).decode("utf-8"))
                return name
            except:  # Otherwise try to convert to a character
                return False
        return False

    def __str__(self):
        parts = [
            str(self.type),
            str(self.key_name),
            str(self.key_code),
            str(self.mouse_code),
            str(self.mouse_pos)
        ]
        return " ".join(parts)


class UI:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.warned_old_curses = 0
        self.limited_colors = True

    def init(self):
        """Set ESC delay and then import curses."""
        global curses
        # Set ESC detection time
        os.environ["ESCDELAY"] = str(self.app.config["app"]["escdelay"])
        # Now import curses, otherwise ESCDELAY won't have any effect
        import curses
        self.logger.debug("Loaded curses {0}".format(curses.version.decode()))

        # Notify user if Pygments syntax highlighting isn't available
        try:
            import pygments  # noqa
        except:
            self.logger.info("Pygments not available, please install python3-pygments for proper syntax highlighting.")

    def run(self, func):
        """Run the application main function via the curses wrapper for safety."""
        curses.wrapper(func)

    def load(self, *args):
        """Setup curses."""
        # Log the terminal type
        termname = curses.termname().decode("utf-8")
        self.logger.debug("Loading UI for terminal: {0}".format(termname))

        self.screen = curses.initscr()
        self.setup_colors()

        curses.raw()
        curses.noecho()

        try:
            # Hide the default cursor
            # Might fail on vt100 terminal emulators
            curses.curs_set(0)
        except:
            self.logger.warning("curses.curs_set(0) failed!")

        self.screen.keypad(1)

        self.current_yx = self.screen.getmaxyx()  # For checking resize
        self.setup_mouse()
        self.setup_windows()

    def unload(self):
        """Unload curses."""
        curses.endwin()

    def setup_mouse(self):
        # Mouse support
        curses.mouseinterval(10)
        if self.app.config["editor"]["use_mouse"]:
            curses.mousemask(-1)  # All events
        else:
            curses.mousemask(0)  # All events

    def setup_colors(self):
        """Initialize color support and define colors."""
        curses.start_color()
        try:
            curses.use_default_colors()
        except:
            self.logger.warning("Failed to load curses default colors. You could try 'export TERM=xterm-256color'.")
            return False

        # Default foreground color (could also be set to curses.COLOR_WHITE)
        fg = -1
        # Default background color (could also be set to curses.COLOR_BLACK)
        bg = -1

        # This gets colors working in TTY's as well as terminal emulators
        # curses.init_pair(10, -1, -1) # Default (white on black)
        # Colors for xterm (not xterm-256color)
        # Dark Colors
        curses.init_pair(0, curses.COLOR_BLACK, bg)      # 0 Black
        curses.init_pair(1, curses.COLOR_RED, bg)        # 1 Red
        curses.init_pair(2, curses.COLOR_GREEN, bg)      # 2 Green
        curses.init_pair(3, curses.COLOR_YELLOW, bg)     # 3 Yellow
        curses.init_pair(4, curses.COLOR_BLUE, bg)       # 4 Blue
        curses.init_pair(5, curses.COLOR_MAGENTA, bg)    # 5 Magenta
        curses.init_pair(6, curses.COLOR_CYAN, bg)       # 6 Cyan
        curses.init_pair(7, fg, bg)                      # 7 White on Black
        curses.init_pair(8, fg, curses.COLOR_BLACK)      # 8 White on Black (Line number color)

        # Set color for whitespace
        # Fails on default Ubuntu terminal with $TERM=xterm (max 8 colors)
        # TODO: Smarter implementation for custom colors
        try:
            curses.init_pair(9, 8, bg)                   # Gray (Whitespace color)
            self.limited_colors = False
        except:
            # Try to revert the color
            self.limited_colors = True
            try:
                curses.init_pair(9, fg, bg)              # Try to revert color if possible
            except:
                # Reverting failed
                self.logger.error("Failed to set and revert extra colors.")

        # Nicer shades of same colors (if supported)
        if curses.can_change_color():
            try:
                # TODO: Define RGB for these to avoid getting
                # different results in different terminals
                # xterm-256color chart http://www.calmar.ws/vim/256-xterm-24bit-rgb-color-chart.html
                curses.init_pair(0, 242, bg)  # 0 Black
                curses.init_pair(1, 204, bg)  # 1 Red
                curses.init_pair(2, 119, bg)  # 2 Green
                curses.init_pair(3, 221, bg)  # 3 Yellow
                curses.init_pair(4, 69, bg)   # 4 Blue
                curses.init_pair(5, 171, bg)  # 5 Magenta
                curses.init_pair(6, 81, bg)   # 6 Cyan
                curses.init_pair(7, 15, bg)   # 7 White
                curses.init_pair(8, 8, curses.COLOR_BLACK)  # 8 Gray on Black (Line number color)
                curses.init_pair(9, 8, bg)   # 8 Gray (Whitespace color)
            except:
                self.logger.warning("Enhanced colors failed to load. You could try 'export TERM=xterm-256color'.")
                self.app.config["editor"]["theme"] = "8colors"
        else:
            self.logger.warning("Enhanced colors not supported. You could try 'export TERM=xterm-256color'.")
            self.app.config["editor"]["theme"] = "8colors"

        self.app.themes.use(self.app.config["editor"]["theme"])

    def setup_windows(self, resize=False):
        """Initialize windows."""
        yx = self.screen.getmaxyx()
        self.text_input = None
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)

        # Test for new curses
        if "get_wch" not in dir(self.header_win):
            # Notify only once
            if not self.warned_old_curses:
                self.logger.warning("Using old curses! Some keys and special characters might not work.")
                self.warned_old_curses = 1

        y_sub = 0
        y_start = 0
        if self.app.config["display"]["show_top_bar"]:
            y_sub += 1
            y_start = 1
        if self.app.config["display"]["show_bottom_bar"]:
            y_sub += 1
        if self.app.config["display"]["show_legend"]:
            y_sub += 2
        self.editor_win = curses.newwin(yx[0]-y_sub, yx[1], y_start, 0)
        if self.app.config["display"]["show_top_bar"]:
            self.legend_win = curses.newwin(2, yx[1], yx[0]-y_sub+1, 0)
        else:
            self.legend_win = curses.newwin(2, yx[1], yx[0]-y_sub, 0)

        if resize:
            self.app.get_editor().resize((yx[0]-y_sub, yx[1]))
            self.app.get_editor().move_win((y_start, 0))

    def get_size(self):
        """Get terminal size."""
        y, x = self.screen.getmaxyx()
        return (x, y)

    def update(self):
        self.check_resize()

    def refresh(self):
        self.refresh_status()
        self.screen.refresh()

    def resize(self, yx=None):
        """Resize UI to yx."""
        if yx is None:
            yx = self.screen.getmaxyx()
        self.screen.erase()
        curses.resizeterm(yx[0], yx[1])
        self.setup_windows(resize=True)

    def check_resize(self):
        """Check if terminal has resized and resize if needed."""
        yx = self.screen.getmaxyx()
        if self.current_yx != yx:
            self.current_yx = yx
            self.resize(yx)

    def refresh_status(self):
        """Refresh status windows."""
        if self.app.config["display"]["show_top_bar"]:
            self.show_top_status()
        if self.app.config["display"]["show_legend"]:
            self.show_legend()
        if self.app.config["display"]["show_bottom_bar"]:
            self.show_bottom_status()

    def show_top_status(self):
        """Show top status row."""
        self.header_win.erase()
        size = self.get_size()
        display = self.app.config["display"]
        head_parts = []
        if display["show_app_name"]:
            name_str = "Suplemon Editor v{0} -".format(self.app.version)
            if self.app.config["app"]["use_unicode_symbols"]:
                logo = "\u2688"      # Simple lemon (filled)
                name_str = " {0} {1}".format(logo, name_str)
            head_parts.append(name_str)

        # Add module statuses to the status bar
        for name in self.app.modules.modules.keys():
            module = self.app.modules.modules[name]
            if module.options["status"] == "top":
                status = module.get_status()
                if status:
                    head_parts.append(status)

        if display["show_file_list"]:
            head_parts.append(self.file_list_str())

        head = " ".join(head_parts)
        head = head + (" " * (self.screen.getmaxyx()[1]-len(head)-1))
        if len(head) >= size[0]:
            head = head[:size[0]-1]
        if self.app.config["display"]["invert_status_bars"]:
            self.header_win.addstr(0, 0, head, curses.color_pair(0) | curses.A_REVERSE)
        else:
            self.header_win.addstr(0, 0, head, curses.color_pair(0))
        self.header_win.refresh()

    def file_list_str(self):
        """Return rotated file list beginning at current file as a string."""
        curr_file_index = self.app.current_file_index()
        files = self.app.get_files()
        file_list = files[curr_file_index:] + files[:curr_file_index]
        str_list = []
        no_write_symbol = ["!", "\u2715"][self.app.config["app"]["use_unicode_symbols"]]
        is_changed_symbol = ["*", "\u2732"][self.app.config["app"]["use_unicode_symbols"]]
        for f in file_list:
            prepend = [no_write_symbol, ""][f.is_writable()]
            append = ""
            if self.app.config["display"]["show_file_modified_indicator"]:
                append += ["", is_changed_symbol][f.is_changed()]
            fname = prepend + f.name + append
            if not str_list:
                str_list.append("[{0}]".format(fname))
            else:
                str_list.append(fname)
        return " ".join(str_list)

    def show_bottom_status(self):
        """Show bottom status line."""
        editor = self.app.get_editor()
        size = self.get_size()
        cur = editor.get_cursor()

        # Core status info
        status_str = "@{0},{1} cur:{2} buf:{3}".format(
            str(cur[0]),
            str(cur[1]),
            str(len(editor.cursors)),
            str(len(editor.get_buffer()))
        )

        # Add module statuses to the status bar
        module_str = ""
        for name in self.app.modules.modules.keys():
            module = self.app.modules.modules[name]
            if module.options["status"] == "bottom":
                module_str += " " + module.get_status()
        status_str = module_str + " " + status_str

        self.status_win.erase()
        status = self.app.get_status()
        extra = size[0] - len(status+status_str) - 1
        line = status+(" "*extra)+status_str

        if len(line) >= size[0]:
            line = line[:size[0]-1]

        if self.app.config["display"]["invert_status_bars"]:
            attrs = curses.color_pair(0) | curses.A_REVERSE
        else:
            attrs = curses.color_pair(0)

        # This thwarts a weird crash that happens when pasting a lot
        # of data that contains line breaks into the find dialog.
        # Should probably figure out why it happens, but it's not
        # due to line breaks in the data nor is the data too long.
        # Thanks curses!
        try:
            self.status_win.addstr(0, 0, line, attrs)
        except:
            self.logger.exception("Failed to show bottom status bar. Status line was: {0}".format(line))

        self.status_win.refresh()

    def show_legend(self):
        """Show keyboard legend."""
        # Only the most important commands are displayed in the legend
        legend_commands = [
            ("save_file", "Save"),
            ("save_file_as", "Save as"),
            ("reload_file", "Reload"),
            ("undo", "Undo"),
            ("redo", "Redo"),
            ("open", "Open"),
            ("copy", "Copy"),
            ("cut", "Cut"),
            ("insert", "Paste"),
            ("find", "Find"),
            ("find_next", "Find next"),
            ("find_all", "Find all"),
            ("duplicate_line", "Duplicate line"),
            ("escape", "Single cursor"),
            ("go_to", "Go to"),
            ("run_command", "Run command"),
            ("toggle_mouse", "Mouse mode"),
            ("help", "Help"),
            ("ask_exit", "Exit"),
        ]

        # Get the key bindings for the commands
        keys = []
        for command in legend_commands:
            for item in self.app.config.keymap:
                if item["command"] == command[0]:
                    key = item["keys"][0]
                    keys.append((key, command[1]))
                    break

        # Render the keys
        self.legend_win.erase()
        x = 0
        y = 0
        max_y = 1
        for item in keys:
            key = item[0]
            label = item[1]
            key = key.upper()
            # Format some key names to look better
            if key.startswith("CTRL+"):
                key = "^"+key[5:]
            if key == "ESCAPE":
                key = "ESC"

            if x+len(" ".join((key, label))) >= self.get_size()[0]:
                x = 0
                y += 1
                if y > max_y:
                    break
            self.legend_win.addstr(y, x, key.upper(), curses.A_REVERSE)
            x += len(key)
            self.legend_win.addstr(y, x, " "+label)
            x += len(label)+2
        self.legend_win.refresh()

    def _query(self, text, initial="", cls=Prompt):
        """Ask for text input via the status bar."""

        # Disable render blocking
        blocking = self.app.block_rendering
        self.app.block_rendering = 0

        # Create our text input
        self.text_input = cls(self.app, self.status_win)
        self.text_input.set_config(self.app.config["editor"].copy())
        self.text_input.set_input_source(self.get_input)
        self.text_input.init()

        # Get input from the user
        out = self.text_input.get_input(text, initial)

        # Restore render blocking
        self.app.block_rendering = blocking

        return out

    def query(self, text, initial=""):
        """Get a single line input string from the user."""
        result = self._query(text, initial)
        return result

    def query_bool(self, text, default=False):
        """Get a boolean from the user."""
        result = self._query(text, default, PromptBool)
        return result

    def query_file(self, text, initial=""):
        """Get a file path from the user."""
        result = self._query(text, initial, PromptFile)
        return result

    def get_input(self, blocking=True):
        """Get an input event from keyboard or mouse. Returns an InputEvent instance or False."""
        event = InputEvent()  # Initialize new empty event
        char = False
        input_func = None
        if "get_wch" in dir(self.screen):
            # New Python 3.3 curses method for wide characters.
            input_func = self.screen.get_wch
        else:
            # Old Python fallback. No multibyte characters.
            input_func = self.screen.getch
        try:
            if blocking:
                self.screen.nodelay(0)
            else:
                self.screen.nodelay(1)
            char = input_func()
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt as Ctrl+C
            event.set_key_name("ctrl+c")
            return event
        except:
            # No input available
            return False
        finally:
            self.screen.nodelay(0)

        if char and char != -1:
            if self.is_mouse(char):
                state = self.get_mouse_state()
                if state:
                    event.parse_mouse_state(state)
                    return event
            else:
                event.parse_key_code(char)
                return event
        return False

    def is_mouse(self, key):
        """Check for mouse events"""
        return key == curses.KEY_MOUSE

    def get_mouse_state(self):
        """Get the mouse event data."""
        try:
            mouse_state = curses.getmouse()
        except:
            self.logger.error("curses.getmouse() failed!", exc_info=True)
            return False

        # Translate the coordinates to the editor coordinate system
        return self._translate_mouse_to_editor(mouse_state)

    def _translate_mouse_to_editor(self, state):
        """Translate the screen coordinates to position in the editor view."""
        editor = self.app.get_editor()
        x, y = (state[1], state[2])
        if self.app.config["display"]["show_top_bar"]:
            y -= 1
        x -= editor.line_offset() - editor.x_scroll
        if x < 0:
            x = 0
        y += editor.y_scroll
        return (state[0], x, y, state[3], state[4])
