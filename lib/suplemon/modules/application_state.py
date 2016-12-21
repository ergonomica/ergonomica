# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class ApplicationState(Module):
    def init(self):
        self.init_logging(__name__)
        self.bind_event_after("app_loaded", self.on_load)
        self.bind_event_before("app_exit", self.on_exit)

    def on_load(self, event):
        """Runs when suplemon is fully loaded."""
        self.restore_states()

    def on_exit(self, event):
        """Runs before suplemon is exits."""
        self.store_states()

    def get_file_states(self):
        """Get the state of currently opened files. Returns a dict with the file path as key and file state as value."""
        states = {}
        for file in self.app.get_files():
            states[file.get_path()] = self.get_file_state(file)
        return states

    def get_file_state(self, file):
        """Get the state of a single file."""
        editor = file.get_editor()
        state = {
            "cursors": [cursor.tuple() for cursor in editor.get_cursors()],
            "scroll_pos": editor.get_scroll_pos(),
        }
        return state

    def set_file_state(self, file, state):
        """Set the state of a file."""
        file.editor.set_cursors(state["cursors"])
        file.editor.set_scroll_pos(state["scroll_pos"])

    def store_states(self):
        """Store the states of opened files."""
        states = self.get_file_states()
        for path in states.keys():
            self.storage[path] = states[path]
        self.storage.store()

    def restore_states(self):
        """Restore the states of files that are currently open."""
        for file in self.app.get_files():
            path = file.get_path()
            if path in self.storage.get_data().keys():
                self.set_file_state(file, self.storage[path])


module = {
    "class": ApplicationState,
    "name": "application_state",
}
