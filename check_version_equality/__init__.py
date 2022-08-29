"""
Checks whether the versions specified in pyproject.toml and project/__init__.py are equal.
"""
import ast
import os
from typing import Optional, Sequence, Union

import toml

__version__ = "0.0.1"


def fetch_dunder_version(source_code: str) -> Optional[str]:
    body = ast.parse(source_code).body
    assigns = [x for x in body if isinstance(x, ast.Assign)]
    for assign in assigns:
        named_targets = [x for x in assign.targets if isinstance(x, ast.Name)]
        ids = [x.id for x in named_targets]
        if next((True for x in ids if x == "__version__"), False):
            if not isinstance(assign.value, ast.Constant):
                raise AssertionError(
                    "Non-constant expression assigning to `__version__`."
                )
            return str(assign.value.value)
    return None


def main(argv: Union[Sequence[str], None] = None) -> int:
    del argv
    if not os.path.exists("pyproject.toml"):
        print("pyproject.toml not found.")
        return 1

    parsed_toml = toml.loads(open("pyproject.toml").read())
    try:
        pyproject_version = str(parsed_toml["tool"]["poetry"]["version"])
        package_dir = parsed_toml["tool"]["poetry"]["name"].replace("-", "_")
    except KeyError:
        return 0
    init_filepath = f"{package_dir}/__init__.py"

    init_version = fetch_dunder_version(open(init_filepath).read())
    if init_version is None:
        return 0

    if pyproject_version == init_version:
        return 0

    print("Versions diverge:")
    print(f"               pyproject.toml: {pyproject_version}")
    print(f"    {package_dir}/__init__.py: {init_version}")
    return 1
