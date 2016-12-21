#!/usr/bin/env python3
# -*- encoding: utf-8
"""
Start a Suplemon instance in the current window
"""

from .main import App, __version__


def main(filenames):
    """Handle CLI invocation"""
    # Parse our CLI arguments

    # Generate and start our application
    app = App(filenames=filenames)
    if app.init():
        app.run()

    # Output log info
    if app.debug:
        for logger_handler in app.logger.handlers:
            logger_handler.close()


if __name__ == "__main__":
    main()
