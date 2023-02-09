import logging
import os
from logging import FileHandler, StreamHandler


class LoggerObserver:
    """Observer class to add logging functionality to any class."""

    def __init__(self, name, level=logging.DEBUG):
        """Initialize a logger object with the given name and level."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

        # Create file handler
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = FileHandler(os.path.join(log_dir, f"{name}.log"))
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)

        # Create console handler
        console_handler = StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)