from suplemon import helpers
from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("//", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        if helpers.starts(line, "function"):
            color = color_map["cyan"]
        elif helpers.starts(line, ["return"]):
            color = color_map["red"]
        elif helpers.starts(line, "this."):
            color = color_map["cyan"]
        elif helpers.starts(line, ["//", "/*", "*/", "*"]):
            color = color_map["magenta"]
        elif helpers.starts(line, ["if", "else", "for ", "while ", "continue", "break"]):
            color = color_map["yellow"]
        return color
