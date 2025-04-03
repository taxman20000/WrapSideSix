# __init__.py

import logging

# Create a logger for your library
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# __all__ = ['Class']

def some_function():
    logger.debug("This is a debug message from my_library.")

# from .library import class or function
from .components.records_navigation_widget import NavWidget