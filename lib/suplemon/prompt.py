# -*- encoding: utf-8
"""
Promts based on the Editor class for querying user input.
"""

import os

from .editor import Editor


class Prompt(Editor):
    """An input prompt based on the Editor."""
    def __init__(self, app, window):
        Editor.__init__(self, app, window)
        self.ready = 0
        self.canceled = 0
        self.input_func = lambda: False
        self.caption = ""

    def init(self):
        Editor.init(self)
        # Remove the find feature, otherwise it can be invoked recursively
        del self.operations["find"]

    def set_config(self, config):
        """Set the configuration for the editor."""
        # Override showing line numbers
        config["show_line_nums"] = False
        Editor.set_config(self, config)

    def set_input_source(self, input_func):
        # Set the input function to use while looping for input
        self.input_func = input_func

    def on_ready(self):
        """Accepts the current input."""
        self.ready = 1
        return

    def on_cancel(self):
        """Cancels the input prompt."""
        self.set_data("")
        self.ready = 1
        self.canceled = 1
        return

    def line_offset(self):
        """Get the x coordinate of beginning of line."""
        return len(self.caption)+1

    def render_line_contents(self, line, pos, x_offset, max_len):
        """Render the prompt line."""
        x_offset = self.line_offset()
        # Render the caption
        self.window.addstr(pos[1], 0, self.caption)
        # Render input
        self.render_line_normal(line, pos, x_offset, max_len)

    def handle_input(self, event):
        """Handle special bindings for the prompt."""
        if event.key_name in ["ctrl+c", "escape"]:
            self.on_cancel()
            return False
        if event.key_name == "enter":
            self.on_ready()
            return False

        return Editor.handle_input(self, event)

    def get_input(self, caption="", initial=""):
        """Get text input from the user via the prompt."""
        self.caption = caption
        self.set_data(initial)
        self.end()  # Move to the end of the initial text

        self.refresh()
        success = self.input_loop()
        if success:
            return self.get_data()
        return False

    def input_loop(self):
        # Run the input loop until ready
        while not self.ready:
            event = self.input_func(True)  # blocking
            if event:
                self.handle_input(event)
            self.refresh()
        if not self.canceled:
            return True


class PromptBool(Prompt):
    """An input prompt for booleans based on Prompt."""

    def set_value(self, value):
        self.value = value

    def handle_input(self, event):
        """Handle special bindings for the prompt."""
        name = event.key_name
        if name.lower() == "y":
            self.set_value(True)
            self.on_ready()
            return False
        if name.lower() == "n":
            self.set_value(False)
            self.on_ready()
            return False
        Prompt.handle_input(self, event)

    def get_input(self, caption="", initial=False):
        """Get a boolean value from the user via the prompt."""

        indicator = "[y/N]"
        if initial:
            indicator = "[Y/n]"

        self.caption = caption + " " + indicator
        self.set_value(initial)
        self.end()  # Move to the end of the initial text

        self.refresh()

        # Run the input loop until ready
        success = self.input_loop()
        if success:
            return self.value
        return False


class PromptFile(Prompt):
    """An input prompt with path auto completion based on Prompt."""

    def __init__(self, app, window):
        Prompt.__init__(self, app, window)
        # Wether the autocomplete feature is active
        self.complete_active = 0
        # Index of last item that was autocompleted
        self.complete_index = 0
        # Input path to use for autocompletion (stored when autocompletion is activated)
        self.complete_data = ""

    def handle_input(self, event):
        """Handle special bindings for the prompt."""
        name = event.key_name
        if self.complete_active:
            # Allow accepting completed directories with enter
            if name == "enter":
                if os.path.isdir(self.get_data()):
                    self.deactivate_autocomplete()
                    return False
            # Revert auto completion with esc
            if name == "escape":
                self.revert_autocomplete()
                self.deactivate_autocomplete()
                return False
        if name == "tab":
            # Run auto completion when tab is pressed
            self.autocomplete()
            # Don't pass the event to the parent class
            return False
        else:
            # If any key other than tab is pressed deactivate the auto completer
            self.deactivate_autocomplete()
        Prompt.handle_input(self, event)

    def autocomplete(self):
        data = self.get_data()  # Use the current input by default
        if self.complete_active:  # If the completer is active use the its initial input value
            data = self.complete_data

        name = os.path.basename(data)
        items = self.get_path_contents(data)  # Get directory listing of input path

        # Filter the items by name if the input path contains a name
        if name:
            items = self.filter_items(items, name)
        if not items:
            # Deactivate completion if there's nothing to complete
            self.deactivate_autocomplete()
            return False

        if not self.complete_active:
            # Initialize the auto completor
            self.complete_active = 1
            self.complete_data = data
            self.complete_index = 0
        else:
            # Increment the selected item countor
            self.complete_index += 1
            if self.complete_index > len(items)-1:
                self.complete_index = 0

        item = items[self.complete_index]
        new_data = os.path.join(os.path.dirname(data), item)
        if len(items) == 1:
            self.deactivate_autocomplete()
        # Set the input data to the new path and move cursor to the end
        self.set_data(new_data)
        self.end()

    def deactivate_autocomplete(self):
        self.complete_active = 0
        self.complete_index = 0
        self.complete_data = ""

    def revert_autocomplete(self):
        if self.complete_data:
            self.set_data(self.complete_data)

    def filter_items(self, items, name):
        """Remove items that don't begin with name. Not case sensitive."""
        if not name:
            return items
        name = name.lower()
        return [item for item in items if item.lower().startswith(name)]

    def get_path_contents(self, path):
        path = os.path.dirname(os.path.expanduser(path))
        # If we get an empty path use the current directory
        if not path:
            path = os.getcwd()
        # In case we don't have sufficent permissions
        try:
            contents = os.listdir(path)
        except:
            return []
        contents.sort()
        items = []
        # Append directory separator to directories
        for item in contents:
            if os.path.isdir(os.path.join(path, item)):
                item = item + os.sep
            items.append(item)
        return items
