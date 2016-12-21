# -*- encoding: utf-8

import difflib

from suplemon.suplemon_module import Module


class Diff(Module):
    """View a diff of the current file compared to it's on disk version."""
    def run(self, app, editor, args):
        curr_file = app.get_file()
        curr_path = curr_file.get_path()
        if not curr_path:
            self.app.set_status("File hasn't been saved, can't show diff.")
            return False

        current_data = editor.get_data()
        f = open(curr_path)
        original_data = f.read()
        f.close()
        diff = self.get_diff(original_data, current_data)

        if not diff:
            self.app.set_status("The file in the editor and on disk are identical.")
            return False
        file = app.new_file()
        file.set_name(curr_file.get_name() + ".diff")
        file.set_data(diff)
        app.switch_to_file(app.last_file_index())

    def get_diff(self, a, b):
        a = a.splitlines(1)
        b = b.splitlines(1)
        diff = difflib.unified_diff(a, b)
        return "".join(diff)


module = {
    "class": Diff,
    "name": "diff",
}
