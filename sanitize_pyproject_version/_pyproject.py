from __future__ import annotations

from pathlib import Path

from addict import Dict as ADict
from toml import loads as toml_loads

__all__ = ["new_pyproject", "Pyproject"]


class Pyproject:
    def __init__(self, filepath: Path):
        self._filepath = filepath.resolve()
        self._toml = ADict(toml_loads(open(self._filepath).read()))

    @staticmethod
    def _backend(filepath: Path) -> str:
        toml = toml_loads(open(filepath).read())
        return str(toml["build-system"]["build-backend"])

    def module_dir(self) -> Path:
        return self._filepath.parent / str(self._toml.project.name).replace("-", "_")

    def static_version(self) -> str:
        return str(self._toml.project.version)

    def has_static_version(self) -> bool:
        return "version" in self._toml.project


class PoetryPyproject(Pyproject):
    def module_dir(self) -> Path:
        return self._filepath.parent / str(self._toml.project.name).replace("-", "_")

    def static_version(self) -> str:
        return str(self._toml.tool.poetry.version)

    def has_static_version(self) -> bool:
        return "version" in self._toml.tool.poetry


class FlitPyproject(Pyproject):
    def module_dir(self) -> Path:
        if "module" in self._toml.tool.flit:
            return self._filepath.parent / str(self._toml.tool.flit.module)
        return self._filepath.parent / str(self._toml.project.name)

    def static_version(self) -> str:
        return str(self._toml.project.version)

    def has_static_version(self) -> bool:
        return "version" in self._toml.project


def new_pyproject(filepath: Path) -> Pyproject:
    backend = Pyproject._backend(filepath)

    if backend.startswith("poetry"):
        return PoetryPyproject(filepath)

    if backend.startswith("flit"):
        return FlitPyproject(filepath)

    return Pyproject(filepath)
