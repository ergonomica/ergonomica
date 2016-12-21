"""
Basic logging to delay printing until curses is unloaded.
"""
from __future__ import print_function
import os
import logging
from logging.handlers import BufferingHandler, RotatingFileHandler
import sys


# Define an mix of BufferingHandler and MemoryHandler which store records internally and flush on `close`
# https://docs.python.org/3.3/library/logging.handlers.html#logging.handlers.BufferingHandler
# https://docs.python.org/3.3/library/logging.handlers.html#logging.handlers.MemoryHandler
class BufferingTargetHandler(BufferingHandler):
    # Set up capacity and target for MemoryHandler
    def __init__(self, capacity, fd_target):
        """
        :param int capacity: Amount of records to store in memory
            https://github.com/python/cpython/blob/3.3/Lib/logging/handlers.py#L1161-L1176
        :param object fd_target: File descriptor to write output to (e.g. `sys.stdout`)
        """
        # Call our BufferingHandler init
        if issubclass(BufferingTargetHandler, object):
            super(BufferingTargetHandler, self).__init__(capacity)
        else:
            BufferingHandler.__init__(self, capacity)

        # Save target for later
        self._fd_target = fd_target

    def close(self):
        """Upon `close`, flush our internal info to the target"""
        # Flush our buffers to the target
        # https://github.com/python/cpython/blob/3.3/Lib/logging/handlers.py#L1185
        # https://github.com/python/cpython/blob/3.3/Lib/logging/handlers.py#L1241-L1256
        self.acquire()
        try:
            for record in self.buffer:
                if record.levelno < self.level:
                    continue
                msg = self.format(record)
                print(msg, file=self._fd_target)
        finally:
            self.release()

        # Then, run our normal close actions
        if issubclass(BufferingTargetHandler, object):
            super(BufferingTargetHandler, self).close()
        else:
            BufferingHandler.close(self)


# Initialize logging
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.handlers = []

# Generate and configure handlers
log_filepath = os.path.join(os.path.expanduser("~"), ".config", "suplemon", "output.log")
logger_handlers = [
    # Buffer 64k records in memory at a time
    BufferingTargetHandler(64 * 1024, fd_target=sys.stderr),
]

# Error recovery when log_filepath isn't writable
try:
    if not os.path.exists(os.path.dirname(log_filepath)):
        os.makedirs(os.path.dirname(log_filepath))
    # Output up to 4MB of records to `~/.config/suplemon/output.log` for live debugging
    # https://docs.python.org/3.3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
    # DEV: We use append mode to prevent erasing out logs
    # DEV: We use 1 backup count since it won't truncate otherwise =/
    rfh = RotatingFileHandler(log_filepath, mode="a+", maxBytes=(4 * 1024 * 1024), backupCount=1)
    logger_handlers.append(rfh)
except:
    # Can't recover and can't log this error
    pass

fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger_formatter = logging.Formatter(fmt)
for logger_handler in logger_handlers:
    logger_handler.setFormatter(logger_formatter)

# Save handlers for our logger
for logger_handler in logger_handlers:
    logger.addHandler(logger_handler)
