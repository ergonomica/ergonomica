# -*- encoding: utf-8
"""
Cursor object for storing cursor data.
"""


class Cursor:
    def __init__(self, x=0, y=0):
        """Initialize Cursor.

        :param x: Cursor x coordinate or x,y tuple. Defaults to 0.
        :param y: Cursor y coordinate. Defaults to 0.
        """
        # Handle coords as a tuple
        if isinstance(x, tuple) or isinstance(x, list):
            x, y = x
            self.x = x
            self.y = y
        # Handle coords from existing Cursor
        elif isinstance(x, Cursor):  # Handle arguments as a cursor
            self.x = x.x
            self.y = x.y
        # Handle coords as plain ints
        else:
            self.x = x
            self.y = y
        # Store the desired x position and
        # use it if the line is long enough
        self.persistent_x = self.x

    def get_x(self):
        """Return the x coordinate of the cursor.

        :return: Cursor x coordinate.
        :rtype: int
        """
        return self.x

    def get_y(self):
        """Return the y coordinate of the cursor.

        :return: Cursor y coordinate.
        :rtype: int
        """
        return self.y

    def set_x(self, x):
        """Set the x coordinate of the cursor."""
        self.x = x
        self.persistent_x = x

    def set_y(self, y):
        """Set the y coordinate of the cursor."""
        self.y = y

    def move_left(self, delta=1):
        """Move the cursor left by delta steps.

        :param int delta: How much to move. Defaults to 1.
        """
        self.x -= delta
        if self.x < 0:
            self.x = 0
        self.persistent_x = self.x
        return

    def move_right(self, delta=1):
        """Move the cursor right by delta steps.

        :param int delta: How much to move. Defaults to 1.
        """
        self.x += delta
        # Check in case of negative values
        if self.x < 0:
            self.x = 0
        self.persistent_x = self.x
        return

    def move_up(self, delta=1):
        """Move the cursor up by delta steps.

        :param int delta: How much to move. Defaults to 1.
        """
        self.y -= 1
        if self.y < 0:
            self.y = 0
        return

    def move_down(self, delta=1):
        """Move the cursor down by delta steps.

        :param int delta: How much to move. Defaults to 1.
        """
        self.y += delta
        return

    def __getitem__(self, i):
        # TODO: Deprecate in favor of proper access methods.
        """Get coordinates with list indices.

        :param i: 0 or 1 for x or y
        :return: x or y coordinate of cursor.
        :rtype: int
        """
        if i == 0:
            return self.x
        elif i == 1:
            return self.y

    def __eq__(self, item):
        """Check cursor for equality."""
        if isinstance(item, Cursor):
            if item.x == self.x and item.y == self.y:
                return True
        return False

    def __ne__(self, item):
        """Check cursor for unequality."""
        if isinstance(item, Cursor):
            if item.x != self.x or item.y != self.x:
                return False

    def __str__(self):
        return "Cursor({x},{y})".format(x=self.x, y=self.y)

    def __repr__(self):
        return self.__str__()

    def tuple(self):
        """Return the cursor as a tuple.

        :return: Tuple with x and y coordinates of cursor.
        :rtype: tuple
        """
        return (self.x, self.y)
