"""Test fixtures for the task manifest base classes tests."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, Dict, MutableMapping, Type
from unittest import mock

import pytest
from .. import task_manifest_base

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask

initial_contents_values = [{}, {"mocked_task_id": mock.Mock()}]


@pytest.fixture
def mocked_cache_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_close_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_vendor_dictionary() -> "Dict[str, TypeGenericTask]":
  return {}


@pytest.fixture
def concrete_task_manifest_class(
    mocked_cache_implementation: mock.Mock,
    mocked_close_implementation: mock.Mock,
    mocked_vendor_dictionary: mock.MagicMock,
) -> Type[task_manifest_base.TaskManifestBase]:

  class ConcreteTaskManifest(task_manifest_base.TaskManifestBase):

    def __init__(self) -> None:
      self.persistent_dict = mocked_vendor_dictionary
      super().__init__()

    def _create_cache(self) -> "MutableMapping[str, TypeGenericTask]":
      mocked_cache_implementation()
      return dict(self.persistent_dict)

    def close(self) -> None:
      mocked_close_implementation()

  return ConcreteTaskManifest


@pytest.fixture
def concrete_task_manifest_instance(
    concrete_task_manifest_class: Type[task_manifest_base.TaskManifestBase],
) -> task_manifest_base.TaskManifestBase:
  return concrete_task_manifest_class()
