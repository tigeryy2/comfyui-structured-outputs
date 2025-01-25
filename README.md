# python-template
Template repo for Python projects

## Setup

### Quick Start
[uv](https://docs.astral.sh/uv/) and `pyproject.toml` are used for Python package setup and dependency management.

1. Clone the project using git
2. Create the venv: `uv sync`. This will create a virtual environment in the `.venv` directory, using python specified
   in the `.python-version` file.
   By default, this will include the `dev` dependencies.
3. Activate the venv: `source .venv/bin/activate` (Linux or MacOS)
4. Install the project in editable mode: `uv pip install -e .`
5. Install the pre-commit hooks: `pre-commit install`



## Processes

### Environment Management

`python-dotenv` is used to manage environment variables. These are stored in a `.env` file in the project root.
[`.env.example`](.env.example) is provided as a template for the `.env` file.

### Dependency Management

Dependencies are defined within `requirements.in` and `requirements-dev.in` files.
These are then compiled into `requirements.txt` and `requirements-dev.txt` files using `compile-reqs` command.

For best compatibility with and without `uv`, dependencies from `requirements.txt` and `requirements-dev.txt` are also
added to the `pyproject.toml` file using `uv add -r requirements.txt` and `uv add -r requirements-dev.txt --dev`.

This allows us to use `uv sync` to install the dependencies from the `pyproject.toml` file into the virtual environment.

As the `uv` ecosystem matures, the `requirements.txt` files may be phased out in favor of the `pyproject.toml` file.

#### Adding or Updating Dependencies
1. Add the package to the relevant `.in` file
2. Run `compile-reqs` (installed as project script) to compile the requirements files
3. Run `uv add -r requirements.txt` and/or `uv add -r requirements-dev.txt --dev`, to update the `pyproject.toml` file
   with the new dependencies.
4. Run `uv sync` to update the virtual environment with the new dependencies.

The complete list of installed packages can be shown using `uv tree`.

### Pre-commit Hooks

Pre-commit hooks are used to enforce code quality and style standards.
These are defined in the `.pre-commit-config.yaml` file.

To install the pre-commit hooks, run `pre-commit install`.