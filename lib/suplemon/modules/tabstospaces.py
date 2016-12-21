# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class TabsToSpaces(Module):
    def run(self, app, editor, args):
        i = 0
        for line in editor.lines:
            new = line.data.replace("\t", " "*editor.config["tab_width"])
            editor.lines[i].set_data(new)
            i += 1


module = {
    "class": TabsToSpaces,
    "name": "tabstospaces",
}
