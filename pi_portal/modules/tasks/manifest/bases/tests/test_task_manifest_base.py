"""Test the TaskManifestBase class."""

from typing import TYPE_CHECKING, Dict
from unittest import mock

import pytest
from pi_portal.modules.tasks.manifest.bases.task_manifest_base import (
    TaskManifestBase,
)
from .conftest import initial_contents_values

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class TestTaskManifestBase:
  """Test the TaskManifestBase class."""

  def test_initialize__attributes(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mocked_cache_implementation: mock.Mock,
      mocked_vendor_dictionary: "Dict[str, TypeGenericTask]",
  ) -> None:
    assert concrete_task_manifest_instance.cached_dict == (
        mocked_vendor_dictionary
    )
    assert concrete_task_manifest_instance.persistent_dict == (
        mocked_vendor_dictionary
    )
    mocked_cache_implementation.assert_called_once_with()

  def test_initialize__inheritance(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
  ) -> None:
    assert isinstance(
        concrete_task_manifest_instance,
        TaskManifestBase,
    )

  @pytest.mark.parametrize("mutated_dict", ["cached_dict", "persistent_dict"])
  def test_initialize__dictionaries_are_independent(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mutated_dict: str,
  ) -> None:
    setattr(concrete_task_manifest_instance, mutated_dict, {"1": mock.Mock()})

    assert concrete_task_manifest_instance.cached_dict != (
        concrete_task_manifest_instance.persistent_dict
    )

  @pytest.mark.parametrize("initial_contents", initial_contents_values)
  def test_add__updates_vendor_dictionary(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mocked_vendor_dictionary: "Dict[str, TypeGenericTask]",
      initial_contents: "Dict[str, TypeGenericTask]",
  ) -> None:
    mocked_vendor_dictionary.update(initial_contents)
    mocked_task = mock.Mock()

    concrete_task_manifest_instance.add(mocked_task)

    assert concrete_task_manifest_instance.\
        persistent_dict[str(mocked_task)] == mocked_task
    for key, value in initial_contents.items():
      assert concrete_task_manifest_instance.persistent_dict[key] == value

  @pytest.mark.parametrize("initial_contents", initial_contents_values)
  def test_add__updates_cached_dictionary(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mocked_vendor_dictionary: "Dict[str, TypeGenericTask]",
      mocked_cache_implementation: mock.Mock,
      initial_contents: "Dict[str, TypeGenericTask]",
  ) -> None:
    mocked_vendor_dictionary.update(initial_contents)
    mocked_task = mock.Mock()

    concrete_task_manifest_instance.add(mocked_task)

    assert concrete_task_manifest_instance.\
        cached_dict[str(mocked_task)] == mocked_task
    for key, value in concrete_task_manifest_instance.cached_dict.items():
      assert concrete_task_manifest_instance.cached_dict[key] == value
    assert mocked_cache_implementation.call_count == 2

  def test_close__calls_mocked_implementation(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mocked_close_implementation: mock.Mock,
  ) -> None:
    concrete_task_manifest_instance.close()

    mocked_close_implementation.assert_called_once_with()

  def test_contents__returns_cached_dictionary(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mocked_vendor_dictionary: "Dict[str, TypeGenericTask]",
  ) -> None:
    mocked_vendor_dictionary.update({"mock_task_id": mock.Mock()})

    return_value = concrete_task_manifest_instance.contents

    assert return_value != list(
        concrete_task_manifest_instance.persistent_dict.values()
    )
    assert return_value == list(
        concrete_task_manifest_instance.cached_dict.values()
    )

  @pytest.mark.parametrize("initial_contents", initial_contents_values)
  def test_remove__updates_vendor_dictionary(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mocked_vendor_dictionary: "Dict[str, TypeGenericTask]",
      initial_contents: "Dict[str, TypeGenericTask]",
  ) -> None:
    mocked_vendor_dictionary.update(initial_contents)
    mocked_task = mock.Mock()
    mocked_vendor_dictionary.update({str(mocked_task): mocked_task})

    concrete_task_manifest_instance.remove(mocked_task)

    assert (
        str(mocked_task) not in concrete_task_manifest_instance.persistent_dict
    )
    assert concrete_task_manifest_instance.persistent_dict == initial_contents

  @pytest.mark.parametrize("initial_contents", initial_contents_values)
  def test_remove__updates_cached_dictionary(
      self,
      concrete_task_manifest_instance: TaskManifestBase,
      mocked_cache_implementation: mock.Mock,
      mocked_vendor_dictionary: "Dict[str, TypeGenericTask]",
      initial_contents: "Dict[str, TypeGenericTask]",
  ) -> None:
    mocked_vendor_dictionary.update(initial_contents)
    mocked_task = mock.Mock()
    mocked_vendor_dictionary.update({str(mocked_task): mocked_task})

    concrete_task_manifest_instance.remove(mocked_task)

    assert str(mocked_task) not in concrete_task_manifest_instance.cached_dict
    assert concrete_task_manifest_instance.cached_dict == initial_contents
    assert mocked_cache_implementation.call_count == 2
