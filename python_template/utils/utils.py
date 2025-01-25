"""
General Utilities
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv

from python_template import DOTENV_FILE
from python_template.utils.loggable import Loggable


@contextmanager
def change_dir(new_dir: Path):
    """
    Changes the current working directory to the specified directory, then changes it back to the original directory.
    """
    original_dir = Path.cwd()
    Loggable.log().debug(
        f"Original directory is '{original_dir}', changing to '{new_dir}'"
    )
    try:
        os.chdir(new_dir)
        yield
    finally:
        os.chdir(original_dir)
        Loggable.log().debug("Reverted to original directory")


def dotenv_file_exists(dotenv_path: Path = DOTENV_FILE) -> bool:
    """
    Returns True if the .env file exists, False otherwise.
    """
    return dotenv_path.exists()


def get_env(key: str, dotenv_path: Path = DOTENV_FILE) -> str | None:
    """
    Returns the value of the specified environment variable key, loading it from the .env file if necessary.
    """
    if value := os.getenv(key):
        return value

    if not dotenv_file_exists():
        Loggable.log().error(f"File '{dotenv_path}' does not exist")
        return None

    load_dotenv(dotenv_path)
    return os.getenv(key)
