# -*- encoding: utf-8

import os

from suplemon import config


class KeymapConfig(config.ConfigModule):
    """Shortcut to openning the keymap config file."""
    def init(self):
        self.config_name = "keymap.json"
        self.config_default_path = os.path.join(self.app.path, "config", self.config_name)
        self.config_user_path = self.app.config.keymap_path()


module = {
    "class": KeymapConfig,
    "name": "keymap",
}
