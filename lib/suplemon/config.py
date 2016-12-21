# -*- encoding: utf-8
"""
Config handler.
"""

import os
import json
import logging

from . import helpers
from . import suplemon_module


class Config:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.default_config_filename = "defaults.json"
        self.default_keymap_filename = "keymap.json"
        self.config_filename = "suplemon-config.json"
        self.keymap_filename = "suplemon-keymap.json"
        self.home_dir = os.path.expanduser("~")
        self.config_dir = os.path.join(self.home_dir, ".config", "suplemon")

        self.defaults = {}
        self.keymap = {}
        self.config = {}

    def init(self):
        self.create_config_dir()
        return self.load_defaults()

    def path(self):
        return os.path.join(self.config_dir, self.config_filename)

    def keymap_path(self):
        return os.path.join(self.config_dir, self.keymap_filename)

    def set_path(self, path):
        parts = os.path.split(path)
        self.config_dir = parts[0]
        self.config_filename = parts[1]

    def load(self):
        path = self.path()
        config = False
        if not os.path.exists(path):
            self.logger.debug("Configuration file '{0}' doesn't exist.".format(path))
        else:
            config = self.load_config_file(path)
        if config:
            self.logger.debug("Loaded configuration file '{0}'".format(path))
            self.config = self.merge_defaults(config)
        else:
            self.logger.info("Failed to load config file '{0}'.".format(path))
            self.config = dict(self.defaults)
        self.load_keys()
        return config

    def load_keys(self):
        path = self.keymap_path()
        keymap = False
        if not os.path.exists(path):
            self.logger.debug("Keymap file '{0}' doesn't exist.".format(path))
            return False
        keymap = self.load_config_file(path)
        if not keymap:
            self.logger.info("Failed to load keymap file '{0}'.".format(path))
            return False
        # Prepend the user keys to the defaults to give the user config a higher priority
        keymap += self.keymap
        self.keymap = self.normalize_keys(keymap)
        return True

    def normalize_keys(self, keymap):
        """Normalize the order of modifier keys in keymap."""
        modifiers = ["shift", "ctrl", "alt", "meta"]  # The modifiers in correct order
        for item in keymap:
            new_keys = []
            for key_item in item["keys"]:
                parts = key_item.split("+")
                key = parts[-1]
                if len(parts) < 2:
                    new_keys.append(key)
                    continue
                normalized = ""
                for mod in modifiers:  # Add the used modifiers back in correct order
                    if mod in parts:
                        normalized += mod + "+"
                normalized += key
                new_keys.append(normalized)
            item["keys"] = new_keys
        return keymap

    def load_defaults(self):
        if not self.load_default_config() or not self.load_default_keys():
            return False
        return True

    def load_default_config(self):
        path = os.path.join(self.app.path, "config", self.default_config_filename)
        config = self.load_config_file(path)
        if not config:
            self.logger.error("Failed to load default config file '{0}'!".format(path))
            return False
        self.defaults = config
        return True

    def load_default_keys(self):
        path = os.path.join(self.app.path, "config", self.default_keymap_filename)
        config = self.load_config_file(path)
        if not config:
            self.logger.error("Failed to load default keymap file '{0}'!".format(path))
            return False
        self.keymap = config
        return True

    def reload(self):
        """Reload the config file."""
        return self.load()

    def store(self):
        """Write current config state to file."""
        data = json.dumps(self.config)
        f = open(self.config_filename)
        f.write(data)
        f.close()

    def merge_defaults(self, config):
        """Fill any missing config options with defaults."""
        for prim_key in self.defaults.keys():
            curr_item = self.defaults[prim_key]
            if prim_key not in config.keys():
                config[prim_key] = dict(curr_item)
                continue
            for sec_key in curr_item.keys():
                if sec_key not in config[prim_key].keys():
                    config[prim_key][sec_key] = curr_item[sec_key]
        return config

    def load_config_file(self, path):
        try:
            f = open(path)
            data = f.read()
            f.close()
            data = self.remove_config_comments(data)
            config = json.loads(data)
            return config
        except:
            return False

    def remove_config_comments(self, data):
        """Remove comments from a 'pseudo' JSON config file.

        Removes all lines that begin with '#' or '//' ignoring whitespace.

        :param data: Commented JSON data to clean.
        :return: Cleaned pure JSON.
        """
        lines = data.split("\n")
        cleaned = []
        for line in lines:
            line = line.strip()
            if helpers.starts(line, "//") or helpers.starts(line, "#"):
                continue
            cleaned.append(line)
        return "\n".join(cleaned)

    def create_config_dir(self):
        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir)
            except:
                self.app.logger.warning("Config folder '{0}' doesn't exist and couldn't be created.".format(
                                        self.config_dir))

    def __getitem__(self, i):
        """Get a config variable."""
        return self.config[i]

    def __setitem__(self, i, v):
        """Set a config variable."""
        self.config[i] = v

    def __str__(self):
        """Convert entire config array to string."""
        return str(self.config)

    def __len__(self):
        """Return length of top level config variables."""
        return len(self.config)


class ConfigModule(suplemon_module.Module):
    """Helper for shortcut for opening config files."""
    def init(self):
        self.config_name = "defaults.json"
        self.config_default_path = os.path.join(self.app.path, "config", self.config_name)
        self.config_user_path = self.app.config.path()

    def run(self, app, editor, args):
        if args == "defaults":
            # Open the default config in a new file only for viewing
            self.open(app, self.config_default_path, read_only=True)
        else:
            self.open(app, self.config_user_path)

    def open(self, app, path, read_only=False):
        if read_only:
            f = open(path)
            data = f.read()
            f.close()
            file = app.new_file()
            file.set_name(self.config_name)
            file.set_data(data)
            app.switch_to_file(app.last_file_index())
        else:
            # Open the user config file for editing
            f = app.file_is_open(path)
            if f:
                app.switch_to_file(app.get_file_index(f))
            else:
                if not app.open_file(path):
                    app.new_file(path)
                app.switch_to_file(app.last_file_index())
