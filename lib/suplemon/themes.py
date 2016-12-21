# -*- encoding: utf-8
"""
Theme loader
"""
import os
import logging

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

from . import hex2xterm

# Map scope name to its color pair index
scope_to_pair = {
    "global": 21,
    "comment": 22,
    "string": 23,
    "constant.numeric": 24,
    "constant.language": 25,
    "constant.character": 26,
    "constant.other": 27,
    "variable": 28,
    "keyword": 29,
    "storage": 30,
    "storage.type": 31,
    "entity.name.class": 32,
    "entity.other.inherited-class": 33,
    "entity.name.function": 34,
    "variable.parameter": 35,
    "entity.name.tag": 36,
    "entity.other.attribute-name": 37,
    "support.function": 38,
    "support.constant": 39,
    "support.type": 40,
    "support.class": 41,
    "support.other.variable": 42,
    "invalid": 43,
    "invalid.deprecated": 44,
    "meta.structure.dictionary.json string.quoted.double.json": 45,
    "meta.diff": 46,
    "meta.diff.header": 47,
    "markup.deleted": 48,
    "markup.inserted": 49,
    "markup.changed": 50,
    "constant.numeric.line-number.find-in-files - match": 51,
    "entity.name.filename.find-in-files": 52,
}


class Theme:
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid
        self.scopes = {}


class ThemeLoader:
    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger(__name__)

        self.curr_path = os.path.dirname(os.path.realpath(__file__))
        # The themes subdirectory
        self.theme_path = os.path.join(self.curr_path, "themes" + os.sep)
        # Module instances
        self.themes = {}
        self.current_theme = None

    def load(self, name):
        fullpath = "".join([self.theme_path, name, ".tmTheme"])
        if not os.path.exists(fullpath):
            self.logger.warning("fullpath '{0}' doesn't exist!".format(fullpath))
            return None

        self.logger.debug("Loading theme '{0}'.".format(name))
        try:
            tree = ET.parse(fullpath)
        except:
            self.logger.error("Couldn't parse theme '{}'. Falling back to line based highlighting.".format(name))
            return None
        root = tree.getroot()

        for child in root:
            config = self.parse(child)
            if config is None:
                return None

        name = config.get("name")
        uuid = config.get("uuid")

        theme = Theme(name, uuid)

        try:
            settings = config["settings"]
        except:
            return None
        self.set_theme(theme, settings)

        return theme

    def use(self, name):
        theme = None
        try:
            theme = self.themes[name]
        except:
            theme = self.load(name)
            self.themes[name] = theme
        if theme is None:
            return
        self.current_theme = theme

    def get_scope(self, name):
        if self.current_theme:
            return self.current_theme.scopes.get(name)
        return False

    def set_theme(self, theme, settings):
        for entry in settings:
            if not isinstance(entry, dict):
                continue
            scope_str = entry.get("scope") or "global"
            scopes = scope_str.split(",")
            settings = entry.get("settings")
            if settings is not None:
                for scope in scopes:
                    theme.scopes[scope.strip()] = settings

    def parse(self, node):
        if node.tag == "dict":
            return self.parse_dict(node)
        elif node.tag == "array":
            return self.parse_array(node)
        elif node.tag == "string":
            return self.parse_text(node)

        return None

    def parse_dict(self, node):
        d = {}
        key = None
        value = None

        for child in node:
            if key is None:
                if child.tag != "key":  # key expected
                    return None
                key = child.text
            else:
                value = self.parse(child)
                if value is not None:
                    d[key] = value

                key = None
                value = None

        return d

    def parse_array(self, node):
        l = []
        for child in node:
            value = self.parse(child)
            if value is not None:
                l.append(value)

        return l

    def parse_text(self, node):
        # If the node text is a hex color convert it to an xterm equivalent
        if node.text:
            color = self.convert_color(node.text)
            if color is not False:
                return color

        return node.text

    def convert_color(self, text):
        if text[0] != "#":
            return False
        # Validate length e.g. #F90, #FF9900, #FF990055
        if len(text) not in [4, 7, 9]:
            return False
        # Strip alpha channel
        hex_color = text
        if len(hex_color) == 9:
            hex_color = hex_color[:7]
        # If the color only has one character per channel convert them to two
        if len(hex_color) == 4:
            hex_color = "#{}{}{}".format(hex_color[1:2]*2, hex_color[2:3]*2, hex_color[3:4]*2)
        # Convert the color
        try:
            xterm_color = int(hex2xterm.hex_to_xterm(hex_color))
            return xterm_color
        except:
            self.logger.exception("Failed to convert color: {}".format(text))

        return False
