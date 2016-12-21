# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class ToggleWhitespace(Module):
    def run(self, app, editor, args):
        # Toggle the boolean
        new_value = not self.app.config["editor"]["show_white_space"]
        self.app.config["editor"]["show_white_space"] = new_value


module = {
    "class": ToggleWhitespace,
    "name": "toggle_whitespace",
}
