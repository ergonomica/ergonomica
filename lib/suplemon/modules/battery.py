# -*- encoding: utf-8

import os
import time
import subprocess

from suplemon import helpers
from suplemon.suplemon_module import Module


class Battery(Module):
    """Shows remaining battery capacity in the top status bar if available."""

    def init(self):
        self.last_value = -1
        self.checked = time.time()
        self.interval = 10

    def value(self):
        """Get the battery charge percent and cache it."""
        if self.last_value == -1:
            state = self.battery_status()
        elif time.time()-self.checked > self.interval:
            state = self.battery_status()
        else:
            return self.last_value
        self.last_value = state
        return state

    def value_str(self):
        """Return formatted value string to show in the UI."""
        val = self.value()
        if val:
            if self.app.config["app"]["use_unicode_symbols"]:
                return "\u26A1{0}%".format(str(val))
            else:
                return "BAT {0}%".format(str(val))
        return ""

    def get_status(self):
        """Called by app when showing status bar contents."""
        return self.value_str()

    def battery_status(self):
        """Attempts to get the battery charge percent."""
        value = None
        methods = [
            self.battery_status_read,
            self.battery_status_acpi,
            self.battery_status_upower
        ]
        for m in methods:
            value = m()
            if value is not None:
                break
        return value

    def battery_status_read(self):
        """Get the battery status via proc/acpi."""
        try:
            path_info = self.readf("/proc/acpi/battery/BAT0/info")
            path_state = self.readf("/proc/acpi/battery/BAT0/state")
        except:
            return None
        try:
            max_cap = float(helpers.get_string_between("last full capacity:", "mWh", path_info))
            cur_cap = float(helpers.get_string_between("remaining capacity:", "mWh", path_state))
            return int(cur_cap / max_cap * 100)
        except:
            return None

    def battery_status_acpi(self):
        """Get the battery status via acpi."""
        try:
            fnull = open(os.devnull, "w")
            raw_str = subprocess.check_output(["acpi"], stderr=fnull)
            fnull.close()
        except:
            return None
        raw_str = raw_str.decode("utf-8")
        part = helpers.get_string_between(",", "%", raw_str)
        if part:
            try:
                return int(part)
            except:
                return None
        return None

    def battery_status_upower(self):
        """Get the battery status via upower."""
        path = "/org/freedesktop/UPower/devices/battery_BAT0"
        try:
            raw_str = subprocess.check_output(["upower", "-i", path])
        except:
            return None
        raw_str = raw_str.decode("utf-8")
        raw_str = raw_str.splitlines()[0]
        part = helpers.get_string_between("percentage:", "%", raw_str)
        if part:
            try:
                return int(part)
            except:
                return None
        return None

    def readf(self, path):
        """Read and return file contents at path."""
        f = open(path)
        data = f.read()
        f.close()
        return data


module = {
    "class": Battery,
    "name": "battery",
    "status": "top",
}
