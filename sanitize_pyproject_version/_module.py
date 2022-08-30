from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["Module"]


class Module:
    def __init__(self, module_dir: Path):
        self._dir = module_dir

    def has_init(self) -> bool:
        return self._init_filepath.exists()

    def has_version(self):
        return self._get_version_assign() is not None

    def has_static_version(self) -> bool:
        assign = self._get_version_assign()
        assert assign is not None
        return isinstance(assign.value, ast.Constant)

    def static_version(self) -> str:
        assign = self._get_version_assign()
        assert assign is not None
        assert isinstance(assign.value, ast.Constant)
        return str(assign.value.value)

    def _get_ast_body(self) -> list[ast.stmt]:
        return ast.parse(open(self._init_filepath).read()).body

    def _get_version_assign(self) -> ast.Assign | None:
        body = self._get_ast_body()
        for assign in [x for x in body if isinstance(x, ast.Assign)]:
            named_targets = [x for x in assign.targets if isinstance(x, ast.Name)]
            ids = [x.id for x in named_targets]
            if next((True for x in ids if x == "__version__"), False):
                return assign
        return None

    @property
    def _init_filepath(self) -> Path:
        return self._dir / "__init__.py"
