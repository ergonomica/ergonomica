# -*- encoding: utf-8

import re
import os
import threading
import subprocess

from suplemon.suplemon_module import Module


class Linter(Module):
    def init(self):
        self.init_logging(__name__)

        # TODO: Run linting in a seperate thread to avoid
        # blocking the UI when the app is loading

        # Lint all files after app is loaded
        self.bind_event_after("app_loaded", self.on_loaded)
        # Show linting messages in status bar
        self.bind_event_after("mainloop", self.mainloop)
        # Re-lint current file when appropriate
        self.bind_event_after("save_file", self.lint_current_file)
        self.bind_event_after("save_file_as", self.lint_current_file)
        self.bind_event_after("reload_file", self.lint_current_file)
        self.bind_event_after("open_file", self.lint_current_file)

    def run(self, app, editor, args):
        """Run the linting command."""
        editor = self.app.get_file().get_editor()
        count = self.get_msg_count(editor)
        status = "{0} lines with linting errors in this file.".format(str(count))
        self.app.set_status(status)

    def on_loaded(self, event):
        # Lint all files in a thread since it might take a while
        thread = threading.Thread(target=self.lint_all_files, args=(event,))
        thread.start()

    def mainloop(self, event):
        """Run the linting command."""
        file = self.app.get_file()
        editor = file.get_editor()
        cursor = editor.get_cursor()
        if len(editor.cursors) > 1:
            return False
        line_no = cursor.y + 1
        msg = self.get_msgs_on_line(editor, cursor.y)
        if msg:
            self.app.set_status("Line {0}: {1}".format(str(line_no), msg))

    def lint_current_file(self, event):
        self.lint_file(self.app.get_file())

    def lint_all_files(self, event):
        """Do linting check for all open files and store results."""
        for file in self.app.files:
            self.lint_file(file)
        return False

    def lint_file(self, file):
        path = file.get_path()
        if not path:  # Unsaved file
            return False

        ext = file.get_extension().lower()
        linter = False
        if ext == "py":
            linter = PyLint(self.logger)
        elif ext == "js":
            linter = JsLint(self.logger)
        elif ext == "php":
            linter = PhpLint(self.logger)

        if not linter:
            return False

        linting = linter.lint(path)
        if linting is False:
            return False

        editor = file.get_editor()
        line_no = 0
        while line_no < len(editor.lines):
            line = editor.lines[line_no]
            if line_no+1 in linting.keys():
                line.linting = linting[line_no+1]
                line.set_number_color(1)
            else:
                line.linting = False
                line.reset_number_color()
            line_no += 1

    def get_msgs_on_line(self, editor, line_no):
        line = editor.lines[line_no]
        if not hasattr(line, "linting") or not line.linting:
            return False
        return line.linting[0][1]

    def get_msg_count(self, editor):
        count = 0
        for line in editor.lines:
            if hasattr(line, "linting"):
                if line.linting:
                    count += 1
        return count


class BaseLint:
    def __init__(self, logger):
        self.logger = logger

    def lint(self, path):
        pass

    def get_file_linting(self, path):
        """Do linting check for given file path."""
        return {}

    def get_output(self, cmd):
        try:
            fnull = open(os.devnull, "w")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=fnull)
            fnull.close()
        except (OSError, EnvironmentError):  # can't use FileNotFoundError in Python 2
            self.logger.debug("Subprocess failed.")
            return False
        out, err = process.communicate()
        return out


class PyLint(BaseLint):
    def __init__(self, logger):
        BaseLint.__init__(self, logger)
        # Error codes to ignore e.g. 'E501' (line too long)
        self.ignore = []
        # Max length of line
        self.max_line_length = 120  # Default is 79

    def lint(self, path):
        if not self.has_flake8_support():
            self.logger.warning("Flake8 not available. Can't show linting.")
            return False
        self.logger.debug(self.has_flake8_support())
        return self.get_file_linting(path)

    def has_flake8_support(self):
        output = self.get_output(["flake8", "--version"])
        return output

    def get_file_linting(self, path):
        """Do linting check for given file path."""
        output = self.get_output(["flake8", "--max-line-length", str(self.max_line_length), path])
        if output is False:
            self.logger.warning("Failed to get linting for file '{0}'.".format(path))
            return False
        output = output.decode("utf-8")
        # Remove file paths from output
        output = output.replace(path+":", "")
        lines = output.split("\n")
        linting = {}
        for line in lines:
            if not line:
                continue
            try:
                parts = line.split(":")
                line_no = int(parts[0])
                char_no = int(parts[1])
                data = ":".join(parts[2:]).strip()
                err_code = data.split(" ")[0]
                if err_code in self.ignore:
                    continue
                if line_no not in linting.keys():
                    linting[line_no] = []
                linting[line_no].append((char_no, data, err_code))
            except:
                self.logger.debug("Failed to parse line:{0}".format(line))
        return linting


class JsLint(BaseLint):
    def __init__(self, logger):
        BaseLint.__init__(self, logger)

    def lint(self, path):
        return self.get_file_linting(path)

    def get_file_linting(self, path):
        """Do linting check for given file path."""
        output = self.get_output(["jshint", path])
        if output is False:
            self.logger.warning("Failed to get linting for file '{0}'.".format(path))
            return False
        output = output.decode("utf-8")
        # Remove file paths from output
        output = output.replace(path+": ", "")
        lines = output.split("\n")
        linting = {}
        for line in lines:
            if not line:
                continue
            try:
                parts = line.split(", ")
                if len(parts) < 3:
                    continue
                line_no = int(re.sub("\D", "", parts[0]))
                char_no = int(re.sub("\D", "", parts[1]))
                data = parts[2]
                err_code = None
                if line_no not in linting.keys():
                    linting[line_no] = []
                linting[line_no].append((char_no, data, err_code))
            except:
                self.logger.debug("Failed to parse line:{0}".format(line))
        return linting


class PhpLint(BaseLint):
    def __init__(self, logger):
        BaseLint.__init__(self, logger)

    def lint(self, path):
        return self.get_file_linting(path)

    def get_output(self, cmd, errors=False):
        # Need to override this since php reports the errors to stderr
        try:
            fnull = open(os.devnull, "w")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            fnull.close()
        except (OSError, EnvironmentError):  # can't use FileNotFoundError in Python 2
            self.logger.debug("Subprocess failed.")
            return False
        out, err = process.communicate()
        return err

    def get_file_linting(self, path):
        """Do linting check for given file path."""
        output = self.get_output(["php", "-l", path])
        if output is False:
            self.logger.warning("Failed to get linting for file '{0}'.".format(path))
            return False
        output = output.decode("utf-8")
        lines = output.split("\n")
        linting = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                parts = line.split(" in {0} on line ".format(path))
                self.logger.debug(parts)
                if len(parts) != 2:
                    continue
                line_no = int(parts[1])
                char_no = 0
                data = parts[0]
                err_code = None
                if line_no not in linting.keys():
                    linting[line_no] = []
                linting[line_no].append((char_no, data, err_code))
            except:
                self.logger.debug("Failed to parse line:{0}".format(line))
        return linting


module = {
    "class": Linter,
    "name": "linter",
}
