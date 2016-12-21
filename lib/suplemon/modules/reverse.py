# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Reverse(Module):
    def run(self, app, editor, args):
        line_nums = []
        for cursor in editor.cursors:
            if cursor.y not in line_nums:
                line_nums.append(cursor.y)
                # Reverse string
                data = editor.lines[cursor.y].data[::-1]
                editor.lines[cursor.y].set_data(data)


module = {
    "class": Reverse,
    "name": "upper",
}
