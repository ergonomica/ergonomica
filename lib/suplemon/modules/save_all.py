# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class SaveAll(Module):
    def run(self, app, editor, args):
        if not self.app.ui.query_bool("Save all files?", False):
            return False
        for file in app.get_files():
            file.save()


module = {
    "class": SaveAll,
    "name": "save_all",
}
