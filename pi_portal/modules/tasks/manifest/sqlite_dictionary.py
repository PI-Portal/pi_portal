"""Sqlite dictionary implementation of the task manifest."""

import os
from typing import TYPE_CHECKING, Dict, MutableMapping

from pi_portal.modules.tasks.manifest.bases.task_manifest_base import (
    TaskManifestBase,
)
from sqlitedict import SqliteDict as VendorDict

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class SqliteDictManifest(TaskManifestBase):
  """SQLite dictionary implementation of the task manifest.

  :param path: The path to database file that will be used.
  :param tablename: The name of the SQLite table that will be used.
  """

  cached_dict: "Dict[str, TypeGenericTask]"
  persistent_dict: VendorDict

  def __init__(self, path: str, tablename: str) -> None:
    self._path = path
    self._tablename = tablename
    if os.path.dirname(path) and not os.path.exists(os.path.dirname(path)):
      os.makedirs(os.path.dirname(path), exist_ok=True)
    self.persistent_dict = self._get_vendor_dict()
    super().__init__()

  def _get_vendor_dict(self) -> VendorDict:
    return VendorDict(
        filename=self._path,
        tablename=self._tablename,
        autocommit=True,
    )

  def _create_cache(self) -> "MutableMapping[str, TypeGenericTask]":
    return dict(self.persistent_dict)

  def close(self) -> None:
    """Close SQLite dictionary filehandle."""
    self.persistent_dict.close()
