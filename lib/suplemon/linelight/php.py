from suplemon import helpers
from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("//", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        keywords = ["if", "else", "finally", "try", "catch", "foreach",
                    "while", "continue", "pass", "break"]
        if helpers.starts(line, ["include", "require"]):
            color = color_map["blue"]
        elif helpers.starts(line, ["class", "public", "private", "function"]):
            color = color_map["green"]
        elif helpers.starts(line, "def"):
            color = color_map["cyan"]
        elif helpers.starts(line, ["return"]):
            color = color_map["red"]
        elif helpers.starts(line, "$"):
            color = color_map["cyan"]
        elif helpers.starts(line, ["#", "//", "/*", "*/"]):
            color = color_map["magenta"]
        elif helpers.starts(line, keywords):
            color = color_map["yellow"]
        return color
