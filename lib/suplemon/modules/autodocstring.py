# -*- encoding: utf-8

from suplemon import helpers
from suplemon.suplemon_module import Module


class AutoDocstring(Module):
    """
    Simple module for adding docstring placeholders.

    This module is intended to generate docstrings for Python functions.
    It adds placeholders for descriptions, arguments and return data.
    Function arguments are crudely parsed from the function definition
    and return statements are scanned from the function body.
    """

    def init(self):
        self.init_logging(__name__)
        self.default_values = {
            "short_desc": "Short description.",
            "long_desc": "Long description.",
            "args": "",
            "returns": "",
        }
        self.docstring_template = "{short_desc}\n" + \
            "\n" + \
            "{long_desc}\n" + \
            "\n" + \
            "{args}" + \
            "{returns}"

    def run(self, app, editor, args):
        """Run the autosphinx command."""
        cursor = editor.get_cursor()
        line = editor.get_line(cursor.y)
        line_data = line.get_data()
        if not helpers.starts(line_data.strip(), "def "):
            app.set_status("Current line isn't a function definition.")
            return False

        func_args = self.get_function_args(line_data)
        func_returns = self.get_function_returns(editor, cursor.y)
        docstring = self.get_docstring(func_args=func_args, func_returns=func_returns)

        indent = self.get_docstring_indent(line_data)
        indent = indent * self.app.config["editor"]["tab_width"] * " "
        self.insert_docstring(editor, cursor.y+1, indent, docstring)

    def insert_docstring(self, editor, line_number, indent, docstring):
        """Insert a docstring at a specific line.

        Inserts the given docstring into editor at a specific
        line and indentation.

        :param editor: The editor to insert into
        :param int line_number: The first line number
        :param str indent: How much the docstring
        :param str docstring: The actual docstring
        """
        docstring = '"""{0}"""'.format(docstring)
        raw_lines = docstring.split("\n")
        lines = []
        for line in raw_lines:
            if not line.strip():
                lines.append("")
            else:
                lines.append(indent+line)
        editor.insert_lines_at(lines, line_number)

    def get_docstring_indent(self, line_data):
        """Get indent amount for docstring.

        Gets the indentation of the function definiton line, and
        adds +1 to account for the function body.

        :param line_data: The line of the function definition.
        """
        tab = self.app.config["editor"]["tab_width"]
        wspace = helpers.whitespace(line_data)
        indent = int(wspace/tab)+1
        return indent

    def get_docstring(self, **values):
        for key in self.default_values.keys():
            if key not in values.keys():
                values[key] = self.default_values[key]

        args = ""
        for arg in values["func_args"]:
            args += ":param {0}:\n".format(arg)
        values["args"] = args

        if values["func_returns"]:
            values["returns"] = ":return:\n"

        doc = self.docstring_template
        doc = doc.format(**values)
        return doc

    def get_function_name(self, line_data):
        """Get the name of function defined in line_data.

        :param str line_data: The line containing the function definition.
        """
        return helpers.get_string_between("def ", "(", line_data)

    def get_function_args(self, line_data):
        """Get list of arguments for function

        Parses a function definition in line_data and returns argument list.

        :param str line_data: The line containing the function definition.
        """
        func_name = self.get_function_name(line_data)
        raw_args = helpers.get_string_between(func_name+"(", "):", line_data)
        parts = raw_args.split(",")
        args = [part.strip() for part in parts]
        if "self" in args:
            args.pop(args.index("self"))
        return args

    def get_function_returns(self, editor, line_number):
        """Returns True if function at line_number returns something.

        :param editor: Editor instance to get lines from.
        :param line_number: Line number of the function definition.
        :return: Boolean indicating wether the function something.
        """
        i = line_number+1
        while i < len(editor.lines):
            line = editor.get_line(i)
            data = line.get_data().strip()
            if helpers.starts(data, "def "):
                break
            if helpers.starts(data, "return "):
                return True
            i += 1
        return False


module = {
    "class": AutoDocstring,
    "name": "autodocstring",
}
