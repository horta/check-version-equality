from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Sequence

from sanitize_pyproject_version._module import Module
from sanitize_pyproject_version._pyproject import Pyproject, new_pyproject
from sanitize_pyproject_version._version_pep440 import Version

__all__ = ["check_version_equality"]


def update_versions_pyproject(versions: Dict[str, Version], pyproject: Pyproject):
    if pyproject.has_static_version():
        version = Version(True, pyproject.static_version())
        if not version.is_canonical():
            print(f"Version {version.value} from pyproject.toml is not canonical.")
            sys.exit(1)
        versions["pyproject"] = version


def update_versions_module(versions: Dict[str, Version], module: Module):
    if module.has_init() and module.has_version():
        if module.has_static_version():
            version = Version(True, module.static_version())
            if not version.is_canonical():
                print(f"Version {version.value} from module is not canonical.")
                sys.exit(1)
            versions["module"] = version
        elif module.has_version():
            versions["module"] = Version(False)


def update_versions_tag(versions: Dict[str, Version], vtags: list[str]):
    if len(vtags) > 1:
        print("Multiple version tags.")
        sys.exit(1)

    if len(vtags) == 1:
        versions["tag"] = Version(True, vtags[0])


def check_version_equality(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project_dir",
        nargs="?",
        type=str,
        help="Directory path to a Python project.",
    )
    args = parser.parse_args(argv)
    if args.project_dir is None:
        project_path = Path(os.getcwd())
    else:
        project_path = Path(args.project_dir)

    project_path = project_path.resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("Project directory not found.")
        return 1

    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.exists():
        print("'pyproject.toml' not found.")
        return 1

    pyproject = new_pyproject(pyproject_path)
    module = Module(pyproject.module_dir())

    versions: Dict[str, Version] = {}

    update_versions_pyproject(versions, pyproject)
    update_versions_module(versions, module)

    version_set = set([version.value for version in versions.values()])
    if len(version_set) == 0:
        print("No version found.")
        return 1

    if len(version_set) > 1:
        print(f"Divergente versions: {versions}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(check_version_equality())
