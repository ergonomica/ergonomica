# -*- encoding: utf-8

"""
The main class that starts and runs Suplemon.
"""


import os
import sys

from . import ui
from . import module_loader
from . import themes
from . import helpers

from .file import File
from .logger import logger
from .config import Config
from .editor import Editor

__version__ = "0.1.58"


class App:
    def __init__(self, filenames=None, config_file=None):
        """
        Handle App initialization

        :param list filenames: Names of files to load initially
        :param str filenames[*]: Path to a file to load
        """
        self.version = __version__
        self.inited = 0
        self.running = 0
        self.debug = 1
        self.block_rendering = False

        # Set default variables
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.files = []
        self.current_file = 0
        self.status_msg = ""
        self.last_input = None
        self.global_buffer = []
        self.event_bindings = {}

        # Maximum amount of inputs to process at once
        self.max_input = 100

        # Save filenames for later
        self.filenames = filenames

        # Save config file path for later
        self.config_file = config_file

        # Define core operations
        self.operations = {
            "help": self.help,
            "save_file": self.save_file,
            "run_command": self.query_command,
            "go_to": self.go_to,
            "open": self.open,
            "close_file": self.close_file,
            "new_file": self.new_file,
            "exit": self.ask_exit,
            "ask_exit": self.ask_exit,
            "prev_file": self.prev_file,
            "next_file": self.next_file,
            "save_file_as": self.save_file_as,
            "reload_file": self.reload_file,
            "toggle_mouse": self.toggle_mouse,
            "toggle_fullscreen": self.toggle_fullscreen,
        }

        # Bind our logger
        self.logger = logger
        self.logger.debug("Starting Suplemon...")

    def init(self):
        """Initialize the app."""
        # Load core components
        self.config = Config(self)
        if self.config_file:
            self.config.set_path(self.config_file)
        if not self.config.init():
            # Can't run without config
            return False
        self.config.load()

        # Unicode symbols don't play nice with Python 2 so disable them
        if sys.version_info[0] < 3:
            self.config["app"]["use_unicode_symbols"] = False

        # Configure logger
        self.debug = self.config["app"]["debug"]
        debug_level = self.config["app"]["debug_level"]
        self.logger.debug("Setting debug_level to {0}.".format(debug_level))
        self.logger.setLevel(debug_level)
        [handler.setLevel(debug_level) for handler in self.logger.handlers]

        # Load user interface
        self.ui = ui.UI(self)
        self.ui.init()

        # Load extension modules
        self.modules = module_loader.ModuleLoader(self)
        self.modules.load()

        # Load themes
        self.themes = themes.ThemeLoader(self)

        # Indicate that initialization is complete
        self.inited = 1

        return True

    def exit(self):
        """Stop the main loop and exit."""
        self.trigger_event_before("app_exit")
        self.running = 0

    def run(self):
        """Run the app via the ui wrapper."""
        self.ui.run(self.run_wrapped)

    def run_wrapped(self, *args):
        """Actually run the app and start mainloop.

        This shouldn't be called directly. Instead it's passed to the UI wich
        calls it in a safe curses wrapper.

        :param *args: Not used. Takes any args the wrapper might pass in.
        """
        # Load ui and files etc
        self.load()
        # Initial render
        self.get_editor().refresh()
        self.ui.refresh()
        # Start mainloop
        self.main_loop()
        self.trigger_event_after("app_exit")
        # Unload ui
        self.ui.unload()

    def load(self):
        """Load the app.

        Load the UI, open files in self.filenames and finally trigger
        the 'app_loaded' event.
        """
        self.ui.load()
        ver = sys.version_info
        if ver[0] < 3 or (ver[0] == 3 and ver[1] < 3):
            ver = ".".join(map(str, sys.version_info[0:2]))
            self.logger.warning("Running Suplemon with Python {version} "
                                "isn't officialy supported. Please use "
                                "Python 3.3 or higher."
                                .format(version=ver))
        self.load_files()
        self.running = 1
        self.trigger_event_after("app_loaded")

    def on_input(self, event):
        # Handle the input or give it to the editor
        if not self.handle_input(event):
            # Pass the input to the editor component
            self.get_editor().handle_input(event)

    def main_loop(self):
        """Run the terminal IO loop until exit() is called."""
        while self.running:
            # Update ui before refreshing it
            self.ui.update()
            self.block_rendering = True
            got_input = False

            # Run through max 100 inputs (so the view is updated at least every 100 characters)
            i = 0
            while i < self.max_input:
                event = self.ui.get_input(False)  # non-blocking

                if not event:
                    break  # no more inputs to process at this time

                i += 1
                got_input = True
                self.on_input(event)

            if not got_input:
                # Wait for input, since there were none already available
                event = self.ui.get_input(True)  # blocking

                if event:
                    got_input = True
                    self.on_input(event)  # PERF: Up to 30% processing time

            self.block_rendering = False

            self.trigger_event_after("mainloop")
            # Rendering happens here
            # TODO: Optimize performance. Can make up 45% of processing time in the loop.
            self.get_editor().refresh()
            self.ui.refresh()

    def get_status(self):
        """Get the current status message.

        :return: Current status message.
        :rtype: str
        """
        return self.status_msg

    def get_file_index(self, file_obj):
        """Return the index of file_obj in the file list.

        :param file_obj: File instance.
        :return: Index of file_obj.
        :rtype: int
        """
        return self.files.index(file_obj)

    def get_key_bindings(self):
        """Return the list of key bindings."""
        bindings = {}
        for binding in self.config.keymap:
            for key in binding["keys"]:
                bindings[key] = binding["command"]
        return bindings

    def get_event_bindings(self):
        """Return the dict of event bindings."""
        return self.event_bindings

    def set_key_binding(self, key, operation):
        """Bind a key to an operation.

        Bind operation to be run when key is pressed.

        :param key: What key or key combination to bind.
        :param str operation: Which operation to run.
        """
        self.config.keymap.prepend({"keys": [key], "command": operation})

    def set_event_binding(self, event, when, callback):
        """Bind a callback to be run before or after an event.

        Bind callback to run before or after event occurs. The when parameter
        should be 'before' or 'after'. If using 'before' the callback can
        inhibit running the event if it returns True

        :param str event: Event to bind to.
        :param str when: String with 'before' or 'after'.
        :param callback: Callback to bind.
        """
        event_bindings = self.get_event_bindings()
        if when not in event_bindings.keys():
            event_bindings[when] = {}
        if event in event_bindings[when].keys():
            event_bindings[when][event].append(callback)
        else:
            event_bindings[when][event] = [callback]

    def set_status(self, status):
        """Set app status message.

        :param str status: Status message to show in status bar.
        """
        self.status_msg = str(status)

    def unsaved_changes(self):
        """Return True if there are unsaved changes in any file."""
        for f in self.files:
            if f.is_changed():
                return True
        return False

    def reload_config(self):
        """Reload configuration."""
        self.config.reload()
        for f in self.files:
            self.setup_editor(f.editor)
        self.ui.resize()
        self.ui.refresh()

    def handle_input(self, event):
        """Handle an input event.

        Runs relevant actions based on the event received.

        :param event: An event instance.
        :return: Boolean indicating if the event was handled.
        :rtype: boolean
        """
        if not event:
            return False
        self.last_input = event
        if event.type == "key":
            return self.handle_key(event)
        elif event.type == "mouse":
            return self.handle_mouse(event)
        return False

    def handle_key(self, event):
        """Handle a key input event.

        :param event: Event instance.
        :return: Boolean indicating if event was handled.
        :rtype: boolean
        """
        key_bindings = self.get_key_bindings()

        operation = None
        if event.key_name in key_bindings.keys():
            operation = key_bindings[event.key_name]
        elif event.key_code in key_bindings.keys():
            operation = key_bindings[event.key_code]

        if operation in self.operations.keys():
            self.run_operation(operation)
            return True
        elif operation in self.modules.modules.keys():
            self.run_module(operation)

        return False

    def handle_mouse(self, event):
        """Handle a mouse input event.

        :param event: Event instance.
        :return: Boolean indicating if event was handled.
        :rtype: boolean
        """
        editor = self.get_editor()
        if event.mouse_code == 1:                    # Left mouse button release
            editor.set_single_cursor(event.mouse_pos)
        elif event.mouse_code == 4096:               # Right mouse button release
            editor.add_cursor(event.mouse_pos)
        elif event.mouse_code == 524288:             # Wheel up
            editor.jump_up()
        elif event.mouse_code == 134217728:          # Wheel down(and unfortunately left button drag)
            editor.jump_down()
        else:
            return False
        return True

    ###########################################################################
    # User Interactions
    ###########################################################################

    def help(self):
        """Open a new file with help text."""
        f = self.default_file()
        from . import help
        f.set_data(help.help_text)
        self.files.append(f)
        self.switch_to_file(self.last_file_index())

    def new_file(self, path=None):
        """Open a new empty file.

        Open a new file and optionally set it's path.

        :param str path: Optional. Path for file.
        """
        new_file = self.default_file()
        if path:
            new_file.set_path(path)
        self.files.append(new_file)
        self.current_file = self.last_file_index()
        return new_file

    def ask_exit(self):
        """Exit if no unsaved changes, else make sure the user really wants to exit."""
        if self.unsaved_changes():
            yes = self.ui.query_bool("Exit?")
            if yes:
                self.exit()
                return True
            return False
        self.exit()
        return True

    def switch_to_file(self, index):
        """Load a default file if no files specified."""
        self.current_file = index

    def next_file(self):
        """Switch to next file."""
        if len(self.files) < 2:
            return
        cur = self.current_file
        cur += 1
        if cur > len(self.files)-1:
            cur = 0
        self.switch_to_file(cur)

    def prev_file(self):
        """Switch to previous file."""
        if len(self.files) < 2:
            return
        cur = self.current_file
        cur -= 1
        if cur < 0:
            cur = len(self.files)-1
        self.switch_to_file(cur)

    def go_to(self):
        """Go to a line or a file (or a line in a specific file with 'name:lineno')."""
        input_str = self.ui.query("Go to:")
        lineno = None
        fname = None
        if input_str is False:
            return False
        if input_str.find(":") != -1:
            parts = input_str.split(":")
            fname = parts[0]
            lineno = parts[1]
            file_index = self.find_file(fname)
            if file_index != -1:
                self.switch_to_file(file_index)
                try:
                    input_str = int(lineno)
                    self.get_editor().go_to_pos(input_str)
                except:
                    pass
        else:
            try:
                line_no = int(input_str)
                self.get_editor().go_to_pos(line_no)
            except:
                file_index = self.find_file(input_str)
                if file_index != -1:
                    self.switch_to_file(file_index)

    def find_file(self, s):
        """Return index of file matching string."""
        # Case insensitive matching
        s = s.lower()
        i = 0
        # First match files beginning with s
        for file in self.files:
            if file.name.lower().startswith(s):
                return i
            i += 1
        i = 0
        # Then match files that contain s
        for file in self.files:
            if s in file.name.lower():
                return i
            i += 1
        return -1

    def run_command(self, data):
        """Run editor commands."""
        parts = data.split(" ")
        cmd = parts[0].lower()
        if cmd in self.operations.keys():
            return self.run_operation(cmd)

        args = " ".join(parts[1:])
        self.logger.debug("Looking for command '{0}'".format(cmd))
        if cmd in self.modules.modules.keys():
            self.logger.debug("Trying to run command '{0}'".format(cmd))
            self.get_editor().store_action_state(cmd)
            if not self.run_module(cmd, args):
                return False
        else:
            self.set_status("Command '{0}' not found.".format(cmd))
            return False
        return True

    def run_module(self, module_name, args=""):
        try:
            self.modules.modules[module_name].run(self, self.get_editor(), args)
            return True
        except:
            self.set_status("Running command failed!")
            self.logger.exception("Running command failed!")
            return False

    def run_operation(self, operation):
        """Run an app core operation."""
        # Support arbitrary callables. TODO: deprecate
        if hasattr(operation, "__call__"):
            return operation()

        if operation in self.operations.keys():
            cancel = self.trigger_event_before(operation)
            if not cancel:
                result = self.operations[operation]()
            self.trigger_event_after(operation)
            return result
        elif operation in self.modules.modules.keys():
            cancel = self.trigger_event_before(operation)
            if not cancel:
                result = self.modules.modules[operation].run(self, self.get_editor(), "")
            self.trigger_event_after(operation)
            return result

        return False

    def trigger_event(self, event, when):
        """Triggers event and runs registered callbacks."""
        status = False
        bindings = self.get_event_bindings()
        if when not in bindings.keys():
            return False
        if event in bindings[when].keys():
            callbacks = bindings[when][event]
            for cb in callbacks:
                try:
                    val = cb(event)
                except:
                    self.logger.error("Failed running callback: {0}".format(cb), exc_info=True)
                    continue
                if val:
                    status = True
        return status

    def trigger_event_before(self, event):
        return self.trigger_event(event, "before")

    def trigger_event_after(self, event):
        return self.trigger_event(event, "after")

    def toggle_fullscreen(self):
        """Toggle full screen editor."""
        display = self.config["display"]
        if display["show_top_bar"]:
            display["show_top_bar"] = 0
            display["show_bottom_bar"] = 0
            display["show_legend"] = 0
        else:
            display["show_top_bar"] = 1
            display["show_bottom_bar"] = 1
            display["show_legend"] = 1
        # Virtual curses windows need to be resized
        self.ui.resize()

    def toggle_mouse(self):
        """Toggle mouse support."""
        # Invert the boolean
        self.config["editor"]["use_mouse"] = not self.config["editor"]["use_mouse"]
        self.ui.setup_mouse()
        if self.config["editor"]["use_mouse"]:
            self.set_status("Mouse enabled")
        else:
            self.set_status("Mouse disabled")

    def query_command(self):
        """Run editor commands."""
        data = self.ui.query("Command:")
        if not data:
            return False
        self.run_command(data)

    ###########################################################################
    # Editor operations
    ###########################################################################

    def new_editor(self):
        """Create a new editor instance."""
        editor = Editor(self, self.ui.editor_win)
        self.setup_editor(editor)
        return editor

    def get_editor(self):
        """Return the current editor."""
        return self.files[self.current_file].editor

    def setup_editor(self, editor):
        """Setup an editor instance with configuration."""
        config = self.config["editor"]
        editor.set_config(config)
        editor.init()

    ###########################################################################
    # File operations
    ###########################################################################

    def open(self):
        """Ask for file name and try to open it."""
        name = self.ui.query_file("Open file:")
        if not name:
            return False
        exists = self.file_is_open(name)
        if exists:
            self.switch_to_file(self.files.index(exists))
            return True

        if not self.open_file(name):
            self.set_status("Failed to load '{0}'".format(name))
            return False
        self.switch_to_file(self.last_file_index())
        return True

    def close_file(self):
        """Close current file if user confirms action."""
        if self.get_file().is_changed():
            if not self.ui.query_bool("Close file?"):
                return False
        self.files.pop(self.current_file)
        if not len(self.files):
            self.new_file()
            return False
        if self.current_file == len(self.files):
            self.current_file -= 1

    def save_file(self, file=False, overwrite=False):
        """Save current file."""
        f = file or self.get_file()
        # Make sure the file has a name
        if not f.get_name():
            return self.save_file_as(f)
        # Warn if the file has changed on disk
        if not overwrite and f.is_changed_on_disk():
            if not self.ui.query_bool("The file was modified since you opened it, save anyway?"):
                return False
        # Save the file
        if f.save():
            self.set_status("Saved [{0}] '{1}'".format(helpers.curr_time_sec(), f.name))
            if f.path() == self.config.path() or f.path() == self.config.keymap_path():
                self.reload_config()
            return True
        self.set_status("Couldn't write to '{0}'".format(f.name))
        return False

    def save_file_as(self, file=False):
        """Save current file."""
        f = file or self.get_file()
        name = self.ui.query_file("Save as:", f.name)
        if not name:
            return False
        if os.path.exists(name):
            if not self.ui.query_bool("A file or directory with that name already exists. Overwrite it?"):
                return False
        target_dir = os.path.dirname(name)
        if target_dir and not os.path.exists(target_dir):
            if self.ui.query_bool("The path doesn't exist, do you want to create it?"):
                self.logger.debug("Creating missing folders in save path.")
                os.makedirs(target_dir)
            else:
                return False
        f.set_path(name)
        # We can just overwrite the file since the user already confirmed
        return self.save_file(f, overwrite=True)

    def reload_file(self):
        """Reload the current file."""
        if self.ui.query_bool("Reload '{0}'?".format(self.get_file().name)):
            if self.get_file().reload():
                return True
        return False

    def get_files(self):
        """Return list of open files."""
        return self.files

    def get_file(self):
        """Return the current file."""
        return self.files[self.current_file]

    def last_file_index(self):
        """Get index of last file."""
        cur = len(self.files)-1
        return cur

    def current_file_index(self):
        """Get index of current file."""
        return self.current_file

    def open_file(self, filename):
        """Open a file."""
        file = File(self)
        file.set_path(filename)
        file.set_editor(self.new_editor())
        if not file.load():
            return False
        self.files.append(file)
        return True

    def load_files(self):
        """Try to load all files specified in arguments."""
        if self.filenames:
            for name in self.filenames:
                if os.path.isdir(name):
                    continue
                if self.file_is_open(name):
                    continue
                if not self.open_file(name):
                    self.new_file(name)
        # If nothing was loaded
        if not self.files:
            self.load_default()

    def file_is_open(self, path):
        """Check if file is open. Returns the File object or False."""
        for file in self.files:
            if file.path() == os.path.abspath(path):
                return file
        return False

    def load_default(self):
        """Load a default file if no files specified."""
        file = self.default_file()
        self.files.append(file)

    def default_file(self):
        """Create the default file."""
        file = File(self)
        file.set_editor(self.new_editor())
        # Specify contents to avoid appearing as modified
        file.set_data("")
        # Set markdown as the default file type
        file.editor.set_file_extension("md")
        return file
