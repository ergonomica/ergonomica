# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class LStrip(Module):
    def run(self, app, editor, args):
        # TODO: move cursors in sync with line contents
        line_nums = editor.get_lines_with_cursors()
        for n in line_nums:
            line = editor.lines[n]
            line.data = line.data.lstrip()


module = {
    "class": LStrip,
    "name": "lstrip",
}
