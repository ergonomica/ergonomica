# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Eval(Module):
    def run(self, app, editor, args):
        if not args:
            return self.evaluate_lines(editor)
        else:
            return self.evaluate_input(args)

    def evaluate_input(self, inp):
        try:
            value = eval(inp)
        except:
            self.app.set_status("Eval failed.")
            return False
        self.app.set_status("Result:{0}".format(value))
        return True

    def evaluate_lines(self, editor):
        line_nums = editor.get_lines_with_cursors()
        for num in line_nums:
            line = editor.get_line(num)
            try:
                value = eval(line.get_data())
            except:
                continue
            line.set_data(str(value))


module = {
    "class": Eval,
    "name": "eval",
}
