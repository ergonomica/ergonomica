# -*- encoding: utf-8

from suplemon import helpers
from suplemon.suplemon_module import Module


class Comment(Module):
    """Toggles line commenting based on current file syntax."""

    def run(self, app, editor, args):
        """Comment the current line(s)."""
        try:
            # Try to get comment start and end syntax
            comment = editor.syntax.get_comment()
        except:
            return False
        line_nums = editor.get_lines_with_cursors()
        # Iterate through lines
        for lnum in line_nums:
            line = editor.lines[lnum]
            if not len(line):
                continue  # Skip empty lines
            # Look for comment syntax in stripped line (TODO:Make this smarter)
            target = str(line).strip()
            w = helpers.whitespace(line)  # Amount of whitespace at line start
            # If the line starts with comment syntax
            if helpers.starts(target, comment[0]):
                # Reconstruct the whitespace and add the line
                new_line = (" "*w) + line[w+len(comment[0]):]
                # If comment end syntax exists
                if comment[1]:
                    # Try to remove it from the end of the line
                    if helpers.ends(new_line, comment[1]):
                        new_line = new_line[:-1*len(comment[1])]
                # Store the modified line
                # editor.lines[lnum] = Line(new_line)
                editor.lines[lnum].set_data(new_line)
            # If the line isn't commented
            else:
                # Slice out the prepended whitespace
                new_line = line[w:]
                # Add the whitespace and starting comment
                new_line = (" "*w) + comment[0] + new_line
                if comment[1]:
                    # Add comment end syntax if needed
                    new_line += comment[1]
                # Store modified line
                # editor.lines[lnum] = Line(new_line)
                editor.lines[lnum].set_data(new_line)
        # Keep cursors under control, same as usual...
        editor.move_cursors()
        editor.store_action_state("comment")


module = {
    "class": Comment,
    "name": "comment",
}
