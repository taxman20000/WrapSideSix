# icons/__init__.py

import logging

# Create a logger for your library
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from . import icons_mat_des as icons_resource


# __all__ = ['Class']

def some_function():
    logger.debug("This is a debug message from my_library.")

# from .library import class or function
