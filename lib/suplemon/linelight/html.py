from suplemon import helpers
from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("<!--", "-->")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        if helpers.starts(line, ["#", "//", "/*", "*/", "<!--"]):
            color = color_map["magenta"]
        elif helpers.ends(line, ["*/", "-->"]):
            color = color_map["magenta"]
        elif helpers.starts(line, "<"):
            color = color_map["cyan"]
        elif helpers.ends(line, ">"):
            color = color_map["cyan"]
        return color
