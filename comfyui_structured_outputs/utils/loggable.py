"""
Provides logging utilities.

Inherit from `Loggable` to get a `log()` classmethod that returns a logger for the parent class.
"""

from __future__ import annotations

import logging
import sys
from logging import handlers
from pathlib import Path


class Loggable:
    """Inherit from this class to get a `log()` classmethod that returns a logger for the parent class."""

    @staticmethod
    def setup_logs(
        log_path: Path | None = None,
        console_log_level: int = logging.INFO,
        file_log_level: int = logging.DEBUG,
        format: str = "[%(asctime)s] [%(levelname)s] %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
    ) -> None:
        """
        Setup logging to file and console.
        Uses a rotating file handler to limit log file size.
        Optionally, configure the logging levels for the console and file handlers.


        :param log_path: Path to log directory
        :param console_log_level: Log level for console logging
        :param file_log_level: log level for file logging
        :param format: Log format
        :param date_format: Log date format

        """
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt=format,
            datefmt=date_format,
        )

        if log_path is not None:
            # setup logging to file
            file_handler = handlers.RotatingFileHandler(
                log_path, maxBytes=1000000, backupCount=5
            )
            file_handler.setLevel(file_log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        # setup logging to console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    @property
    def logger(self) -> logging.Logger:
        """Returns a logger for the parent class."""
        return logging.getLogger(self.__class__.__name__)

    @classmethod
    def log(cls) -> logging.Logger:
        """Returns a logger for the parent class."""
        return logging.getLogger(cls.__name__)
