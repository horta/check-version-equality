import re
from dataclasses import dataclass

__all__ = ["Version", "VERSION_PATTERN"]

# https://peps.python.org/pep-0440/
VERSION_PATTERN = r"([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?"


@dataclass
class Version:
    static: bool = True
    value: str = ""

    def is_canonical(self) -> bool:
        return re.match(r"^" + VERSION_PATTERN + r"$", self.value) is not None
