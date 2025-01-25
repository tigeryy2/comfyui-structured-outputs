"""
Updates the requirements.txt file(s) with the latest dependencies.
"""

import subprocess
from pathlib import Path

from logs import LOGS_DIR
from python_template.utils.loggable import Loggable
from python_template.utils.utils import change_dir

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent.parent.resolve()
REQUIREMENTS_IN_FILES: list[str] = ["requirements.in", "requirements-dev.in"]


def main(root_dir: Path = PROJECT_ROOT_DIR):
    Loggable.log().info(f"Project root directory: {PROJECT_ROOT_DIR}")
    Loggable.log().info(f"Requirements files: {REQUIREMENTS_IN_FILES}")

    with change_dir(root_dir):
        for file_name in REQUIREMENTS_IN_FILES:
            file_path: Path = root_dir / file_name
            if not file_path.exists():
                Loggable.log().error(f"File '{file_path}' does not exist")
                continue

            req_txt_name: str = file_name.replace(".in", ".txt")
            compile_command: str = f"uv pip compile {file_name} > {req_txt_name}"

            Loggable.log().info(f"Compiling '{file_name}' to '{req_txt_name}'")
            try:
                Loggable.log().debug(f"Running command: {compile_command}")
                subprocess.run(compile_command, shell=True, check=True)
            except subprocess.CalledProcessError as err:
                Loggable.log().error(
                    f"Error compiling '{file_name}' to '{req_txt_name}': {err}"
                )


if __name__ == "__main__":
    Loggable.setup_logs(log_path=LOGS_DIR / "tests.log")
    main()
