import tempfile
from pathlib import Path

import pytest

from python_template.utils.utils import change_dir, dotenv_file_exists, get_env


def test_change_dir_succeeds():
    original_dir = Path.cwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir).resolve()
        with change_dir(temp_dir):
            assert Path.cwd() == temp_dir
        # Ensure we returned to the original directory
        assert Path.cwd() == original_dir


def test_change_dir_handles_exception():
    original_dir = Path.cwd()
    with (
        tempfile.TemporaryDirectory() as temp_dir,
        pytest.raises(AssertionError),
        change_dir(Path(temp_dir)),
    ):
        # Ensure the directory was changed
        assert Path.cwd() == Path(temp_dir).resolve()
        # Raise an exception to trigger the finally
        raise AssertionError()

    # Ensure we returned to the original directory
    assert Path.cwd() == original_dir


@pytest.mark.parametrize("env_file_items", [{"SOME_KEY": "A_VALUE"}], indirect=True)
def test_dotenv(env_file_items: dict):
    assert dotenv_file_exists()

    value1 = get_env("SOME_KEY")
    assert value1 == "A_VALUE"
