from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("/*", "*/")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = str(raw_line)
        if line.startswith("+"):
            color = color_map["green"]
        elif line.startswith("-"):
            color = color_map["red"]
        elif line.startswith("@@"):
            color = color_map["blue"]
        return color
