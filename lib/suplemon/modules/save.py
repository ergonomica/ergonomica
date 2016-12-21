# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Save(Module):
    def run(self, app, editor, args):
        return app.save_file()


module = {
    "class": Save,
    "name": "save",
}
