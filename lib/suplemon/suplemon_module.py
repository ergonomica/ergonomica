# -*- encoding: utf-8
"""
Base class for extension modules to inherit.
"""

import os
import json
import logging


class Storage:
    """
    Semi-automatic key/value store for suplemon modules.
    """
    def __init__(self, module):
        self.data = {}
        self.automatic = False
        self.module = module
        self.data_subdir = "modules"
        self.extension = "json"
        self.storage_dir = os.path.join(self.module.app.config.config_dir, self.data_subdir)
        if not os.path.exists(self.storage_dir):
            try:
                os.makedirs(self.storage_dir)
            except:
                self.module.app.logger.warning(
                  "Module storage folder '{0}' doesn't exist and couldn't be created.".format(
                                               self.storage_dir))

    def __getitem__(self, i):
        """Get a storage key value."""
        return self.data[i]

    def __setitem__(self, i, v):
        """Set a storage key value."""
        self.data[i] = v
        if self.automatic:
            self.store()

    def __str__(self):
        """Convert entire data dict to string."""
        return str(self.data)

    def __len__(self):
        """Return length of data dict."""
        return len(self.data)

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def get_path(self):
        """Get the storage file path."""
        if self.module.get_name():
            return os.path.join(self.storage_dir, self.module.get_name() + "." + self.extension)
        return False

    def get_data(self):
        """Get the storage data."""
        return self.data

    def set_data(self, data):
        """Set the storage data."""
        self.data = data

    def set_automatic(self, auto):
        """Set wether the data should be stored automatically when changed."""
        self.automatic = auto

    def store(self):
        """Store the storage data to disk."""
        try:
            data = json.dumps(self.data)
            f = open(self.get_path(), "w")
            f.write(data)
            f.close()
        except:
            self.module.logger.exception("Storing module storage failed.")

    def load(self):
        """Load the storage data from disk."""
        if os.path.exists(self.get_path()):
            try:
                f = open(self.get_path())
                data = f.read()
                f.close()
            except:
                self.module.logger.debug("Loading module storage failed.")
                return False
        else:
            return False

        try:
            self.data = json.loads(data)
            return True
        except:
            self.module.logger.exception("Parsing module storage failed.")
        return False


class Module:
    def __init__(self, app, name, options=None):
        self.app = app
        self.name = name
        self.options = options
        self.logger = None
        self.storage = Storage(self)
        self.init_logging(self.get_name())
        self.storage.load()
        self.init()

    def init(self):
        """Initialize the module.

        This function is run when the module is loaded and can be
        reimplemented for module specific initializations.
        """

    def get_name(self):
        """Get module name."""
        return self.name

    def get_options(self):
        """Get module options."""
        return self.options

    def set_name(self, name):
        """Set module name."""
        self.name = name

    def set_options(self, options):
        """Set module options."""
        self.options = options

    def init_logging(self, name):
        """Initialize the module logger (self.logger).

        Should be called before the module uses logging.
        Always pass __name__ as the value to name, for consistency.

        Args:
        :param name: should be specified as __name__
        """
        if not self.logger:
            self.logger = logging.getLogger("module.{0}".format(name))

    def run(self, app, editor, args):
        """This is called each time the module is run.

        Called when command is issued via prompt or key binding.

        Args:
        :param app: the app instance
        :param editor: the current editor instance
        """
        pass

    def bind_key(self, key):
        """Shortcut for binding run method to a key.

        Args:
        :param key:
        """
        self.app.set_key_binding(key, self._proxy_run)

    def bind_event(self, event, callback):
        """Bind a callback to be called before event is run.

        If the callback returns True the event will be canceled.

        :param event: The event name
        :param callback: Function to be called
        """
        self.app.set_event_binding(event, "before", callback)

    def bind_event_before(self, event, callback):
        """Bind a callback to be called before event is run.

        If the callback returns True the event will be canceled.

        :param event: The event name
        :param callback: Function to be called
        """
        self.app.set_event_binding(event, "before", callback)

    def bind_event_after(self, event, callback):
        """Bind a callback to be called after event is run.

        :param event: The event name
        :param callback: Function to be called
        """
        self.app.set_event_binding(event, "after", callback)

    def _proxy_run(self):
        """Calls the run method with necessary arguments."""
        self.run(self.app, self.app.get_editor(), "")
