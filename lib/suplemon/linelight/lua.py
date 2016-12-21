from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("-- ", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        return color
