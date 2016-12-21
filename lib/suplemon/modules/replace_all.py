# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class ReplaceAll(Module):
    def run(self, app, editor, args):
        r_from = self.app.ui.query("Replace text:")
        if not r_from:
            return False
        r_to = self.app.ui.query("Replace with:")
        if not r_to:
            return False
        for file in app.get_files():
            file.editor.replace_all(r_from, r_to)


module = {
    "class": ReplaceAll,
    "name": "replace_all",
}
