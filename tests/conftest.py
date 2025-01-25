import pytest

from logs import LOGS_DIR
from python_template import DOTENV_FILE
from python_template.utils.loggable import Loggable
from python_template.utils.utils import dotenv_file_exists


@pytest.fixture(scope="session")
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
