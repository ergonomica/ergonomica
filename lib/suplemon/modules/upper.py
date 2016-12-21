# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Upper(Module):
    def run(self, app, editor, args):
        line_nums = []
        for cursor in editor.cursors:
            if cursor.y not in line_nums:
                line_nums.append(cursor.y)
                data = editor.lines[cursor.y].get_data().upper()
                editor.lines[cursor.y].set_data(data)


module = {
    "class": Upper,
    "name": "upper",
}
