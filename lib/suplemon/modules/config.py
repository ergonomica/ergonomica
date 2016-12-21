# -*- encoding: utf-8

import os

from suplemon import config


class SuplemonConfig(config.ConfigModule):
    """Shortcut to openning the keymap config file."""
    def init(self):
        self.config_name = "defaults.json"
        self.config_default_path = os.path.join(self.app.path, "config", self.config_name)
        self.config_user_path = self.app.config.path()


module = {
    "class": SuplemonConfig,
    "name": "config",
}
