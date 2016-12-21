from suplemon import helpers
from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("# ", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        keywords = ["if", "elif", "else", "finally", "try", "except",
                    "for ", "while ", "continue", "pass", "break"]
        if helpers.starts(line, ["import", "from"]):
            color = color_map["blue"]
        elif helpers.starts(line, "class"):
            color = color_map["green"]
        elif helpers.starts(line, "def"):
            color = color_map["cyan"]
        elif helpers.starts(line, ["return", "yield"]):
            color = color_map["red"]
        elif helpers.starts(line, "self."):
            color = color_map["cyan"]
        elif helpers.starts(line, ["#", "//", "\"", "'", ":"]):
            color = color_map["magenta"]
        elif helpers.starts(line, keywords):
            color = color_map["yellow"]
        return color
