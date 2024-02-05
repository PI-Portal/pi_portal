"""Stubs for the sqlitedict package."""

from collections import UserDict
from typing import Any

# isort: off


class SqliteDict(UserDict[str, Any]):
  ...

  def close(self) -> None:
    ...
