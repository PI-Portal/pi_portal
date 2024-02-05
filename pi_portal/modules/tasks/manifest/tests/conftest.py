"""Test fixtures for the task manifest implementations tests."""
# pylint: disable=redefined-outer-name

from collections import UserDict
from typing import TYPE_CHECKING, Dict, Type
from unittest import mock

import pytest
from .. import sqlite_dictionary

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask
  TypedUserDict = UserDict[str, TypeGenericTask]
else:
  TypedUserDict = UserDict


@pytest.fixture
def mocked_close_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_makedirs() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_path_exists() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_path_name() -> str:
  return "mocked_path_name"


@pytest.fixture
def mocked_sqlite_dictionary(
    mocked_vendor_dictionary: "Dict[str, TypeGenericTask]",
) -> mock.MagicMock:
  instance = mock.MagicMock()
  instance.return_value = mocked_vendor_dictionary
  return instance


@pytest.fixture
def mocked_table_name() -> str:
  return "mocked_table_name"


@pytest.fixture
def mocked_vendor_dictionary(
    mocked_close_implementation: mock.Mock,
) -> "TypedUserDict":

  class VendorMockImplementation(TypedUserDict):

    def close(self) -> None:
      mocked_close_implementation()

  return VendorMockImplementation()


@pytest.fixture
def sqlite_dict_manifest_class(
    mocked_os_makedirs: mock.Mock,
    mocked_os_path_exists: mock.Mock,
    mocked_sqlite_dictionary: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[sqlite_dictionary.SqliteDictManifest]:
  monkeypatch.setattr(
      sqlite_dictionary.__name__ + ".os.makedirs",
      mocked_os_makedirs,
  )
  monkeypatch.setattr(
      sqlite_dictionary.__name__ + ".os.path.exists",
      mocked_os_path_exists,
  )
  monkeypatch.setattr(
      sqlite_dictionary.__name__ + ".VendorDict",
      mocked_sqlite_dictionary,
  )
  return sqlite_dictionary.SqliteDictManifest


@pytest.fixture
def sqlite_dict_manifest_instance(
    sqlite_dict_manifest_class: Type[sqlite_dictionary.SqliteDictManifest],
    mocked_path_name: str,
    mocked_table_name: str,
) -> sqlite_dictionary.SqliteDictManifest:
  return sqlite_dict_manifest_class(mocked_path_name, mocked_table_name)
