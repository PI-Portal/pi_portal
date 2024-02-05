"""Test the SqliteDictManifest class."""

import os
from typing import TYPE_CHECKING, Dict, Type
from unittest import mock

import pytest
from pi_portal.modules.tasks.manifest.bases.task_manifest_base import (
    TaskManifestBase,
)
from pi_portal.modules.tasks.manifest.sqlite_dictionary import (
    SqliteDictManifest,
)

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class TestSqliteDictManifest:
  """Test the SqliteDictManifest class."""

  def test_initialize__attributes(
      self, sqlite_dict_manifest_instance: SqliteDictManifest,
      mocked_vendor_dictionary: "Dict[str, TypeGenericTask]"
  ) -> None:
    assert sqlite_dict_manifest_instance.cached_dict == (
        mocked_vendor_dictionary
    )
    assert sqlite_dict_manifest_instance.persistent_dict == (
        mocked_vendor_dictionary
    )

  def test_initialize__inheritance(
      self,
      sqlite_dict_manifest_instance: SqliteDictManifest,
  ) -> None:
    assert isinstance(
        sqlite_dict_manifest_instance,
        TaskManifestBase,
    )

  @pytest.mark.parametrize("mutated_dict", ["cached_dict", "persistent_dict"])
  def test_initialize__dictionaries_are_independent(
      self,
      sqlite_dict_manifest_instance: SqliteDictManifest,
      mutated_dict: str,
  ) -> None:
    setattr(sqlite_dict_manifest_instance, mutated_dict, {"1": mock.Mock()})

    assert sqlite_dict_manifest_instance.cached_dict != (
        sqlite_dict_manifest_instance.persistent_dict
    )

  def test_initialize__creates_vendor_dict(
      self,
      sqlite_dict_manifest_instance: SqliteDictManifest,
      mocked_path_name: str,
      mocked_sqlite_dictionary: mock.MagicMock,
      mocked_table_name: str,
  ) -> None:
    assert sqlite_dict_manifest_instance.cached_dict == (
        mocked_sqlite_dictionary.return_value
    )
    mocked_sqlite_dictionary.assert_called_once_with(
        filename=mocked_path_name,
        tablename=mocked_table_name,
        autocommit=True,
    )

  @pytest.mark.parametrize("db_path_exists", [True, False])
  @pytest.mark.parametrize(
      "db_path", ["/with_parent/file.db", "with_out_parent_file.db"]
  )
  def test_initialize__creates_database_directory(
      self,
      sqlite_dict_manifest_class: Type[SqliteDictManifest],
      mocked_os_makedirs: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      db_path_exists: bool,
      db_path: str,
  ) -> None:
    mocked_os_path_exists.return_value = db_path_exists

    sqlite_dict_manifest_class(db_path, "mock_table")

    created = mocked_os_makedirs.mock_calls == [
        mock.call(
            os.path.dirname(db_path),
            exist_ok=True,
        )
    ]
    not_created = mocked_os_makedirs.mock_calls == []
    has_dirname = os.path.dirname(db_path) != ""
    assert created is (not db_path_exists and has_dirname)
    assert not_created is (db_path_exists or not has_dirname)

  def test_close__calls_vendor_implementation(
      self,
      sqlite_dict_manifest_instance: SqliteDictManifest,
      mocked_close_implementation: mock.Mock,
  ) -> None:
    sqlite_dict_manifest_instance.close()

    mocked_close_implementation.assert_called_once_with()
