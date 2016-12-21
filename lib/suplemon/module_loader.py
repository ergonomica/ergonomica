# -*- encoding: utf-8
"""
Addon module loader.
"""
import os
import imp
import logging


class ModuleLoader:
    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger(__name__)
        # The app root directory
        self.curr_path = os.path.dirname(os.path.realpath(__file__))
        # The modules subdirectory
        self.module_path = os.path.join(self.curr_path, "modules" + os.sep)
        # Module instances
        self.modules = {}

    def load(self):
        """Find and load available modules."""
        self.logger.debug("Loading modules...")
        dirlist = os.listdir(self.module_path)
        for item in dirlist:
            # Skip 'hidden' dot files
            if item[0] == ".":
                continue
            parts = item.split(".")
            if len(parts) < 2:
                continue
            name = parts[0]
            ext = parts[-1]

            # only load .py modules that don't begin with an underscore
            if ext == "py" and name[0] != "_":
                module = self.load_single(name)
                if module:
                    # Load and store the module instance
                    inst = self.load_instance(module)
                    if inst:
                        self.modules[module[0]] = inst

    def load_instance(self, module):
        """Initialize a module."""
        try:
            inst = module[1]["class"](self.app, module[0], module[1])  # Store the module instance
            return inst
        except:
            self.logger.error("Initializing module failed: {0}".format(module[0]), exc_info=True)
        return False

    def load_single(self, name):
        """Load single module file."""
        path = os.path.join(self.module_path, name+".py")
        try:
            mod = imp.load_source(name, path)
        except:
            self.logger.error("Failed loading module: {0}".format(name), exc_info=True)
            return False
        if "module" not in dir(mod):
            return False
        if "status" not in mod.module.keys():
            mod.module["status"] = False
        return name, mod.module


if __name__ == "__main__":
    ml = ModuleLoader()
    ml.load()
