# -*- encoding: utf-8

import subprocess

from suplemon.suplemon_module import Module


class SystemClipboard(Module):
    def init(self):
        self.init_logging(__name__)
        if not self.has_xsel_support():
            self.logger.warning("Can't use system clipboard. Install 'xsel' for system clipboard support.")
            return False
        self.bind_event_before("insert", self.insert)
        self.bind_event_after("copy", self.copy)
        self.bind_event_after("cut", self.copy)

    def copy(self, event):
        lines = self.app.get_editor().get_buffer()
        data = "\n".join([str(line) for line in lines])
        self.set_clipboard(data)

    def insert(self, event):
        data = self.get_clipboard()
        lines = data.split("\n")
        self.app.get_editor().set_buffer(lines)

    def get_clipboard(self):
        try:
            data = subprocess.check_output(["xsel", "-b"], universal_newlines=True)
            return data
        except:
            return False

    def set_clipboard(self, data):
        try:
            p = subprocess.Popen(["xsel", "-i", "-b"], stdin=subprocess.PIPE)
            out, err = p.communicate(input=bytes(data, "utf-8"))
            return out
        except:
            return False

    def has_xsel_support(self):
        output = self.get_output(["xsel", "--version"])
        return output

    def get_output(self, cmd):
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        except (OSError, EnvironmentError):  # can't use FileNotFoundError in Python 2
            return False
        out, err = process.communicate()
        return out


module = {
    "class": SystemClipboard,
    "name": "system_clipboard",
}
