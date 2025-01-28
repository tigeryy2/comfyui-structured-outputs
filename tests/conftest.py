# ruff: noqa: E402
# disable enforcing module level import not at top of file
# we need to import this after the workaround
from pathlib import Path

import pytest

# to workaround the issue of the `__init__.py` file at the project root,
# which causes an `ImportError: attempted relative import with no known parent package",
# a super hacky fix to temp delete the `__init__.py` file
ROOT_INIT_FILE: Path = Path(__file__).parent.parent / "__init__.py"
if ROOT_INIT_FILE.exists():
    # read file contents, back it up, and then delete the file
    with open(ROOT_INIT_FILE) as file:
        contents = file.read()
    ROOT_INIT_FILE.unlink()


@pytest.fixture(autouse=True, scope="session")
def root_init_file_workaround():
    # first, run all the tests
    yield
    # then, restore the file
    if not ROOT_INIT_FILE.exists():
        ROOT_INIT_FILE.touch()
        # restore the file
        with open(ROOT_INIT_FILE, "w") as file:
            file.write(contents)


from comfyui_structured_outputs import DOTENV_FILE
from comfyui_structured_outputs.utils.loggable import Loggable
from comfyui_structured_outputs.utils.utils import dotenv_file_exists
from logs import LOGS_DIR


@pytest.fixture(scope="session", autouse=True)
def logger():
    Loggable.setup_logs(log_path=LOGS_DIR / "tests.log")


@pytest.fixture(params=[{}], scope="function")
def env_file_items(request) -> dict:
    """
    Fixture to temporarily update the .env file with the specified key-value pairs.

    Usage::

        @pytest.mark.parametrize("env_file_items", [{"SOME_KEY": "A_VALUE"}], indirect=True)
        def test_dotenv(env_file_items: dict):
            assert dotenv_file_exists()

            value1 = get_env("SOME_KEY")
            assert value1 == "A_VALUE"

    :param request:
    :return:
    """
    # save original .env file contents
    original_contents: list[str] | None = None
    if dotenv_file_exists():
        with open(DOTENV_FILE) as file:
            original_contents = file.readlines()

    # update .env file with new contents
    with open(DOTENV_FILE, "w") as file:
        for key, value in request.param.items():
            file.write(f"{key}={value}\n")

    yield request.param

    # teardown: restore original .env file contents
    if dotenv_file_exists():
        # delete .env file
        DOTENV_FILE.unlink()

    if original_contents is not None:
        with open(DOTENV_FILE, "w") as file:
            file.writelines(original_contents)
