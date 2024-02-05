"""Test the TaskManifestFactory class."""

import os
from unittest import mock

from pi_portal.modules import tasks
from pi_portal.modules.tasks.enums import TaskManifests
from ..task_manifest_factory import TaskManifestFactory


class TestTaskManifestFactory:
  """Test the TaskManifestFactory class."""

  def test_attributes(
      self,
      task_manifest_factory_class: TaskManifestFactory,
      mocked_vendor_class: mock.Mock,
  ) -> None:
    assert task_manifest_factory_class.vendor_class == mocked_vendor_class

  def test_create__calls_vendor_class(
      self,
      task_manifest_factory_class: TaskManifestFactory,
      mocked_vendor_class: mock.Mock,
  ) -> None:
    mock_manifest = TaskManifests.FAILED_TASKS

    return_value = task_manifest_factory_class.create(mock_manifest)

    mocked_vendor_class.assert_called_once_with(
        os.path.join(os.path.dirname(tasks.__file__), "db", "manifests"),
        mock_manifest.value,
    )
    assert return_value == mocked_vendor_class.return_value

  def test_create__called_twice__calls_vendor_class_once(
      self,
      task_manifest_factory_class: TaskManifestFactory,
      mocked_vendor_class: mock.Mock,
  ) -> None:
    mock_manifest = TaskManifests.FAILED_TASKS

    _ = task_manifest_factory_class.create(mock_manifest)
    return_value = task_manifest_factory_class.create(mock_manifest)

    mocked_vendor_class.assert_called_once_with(
        os.path.join(os.path.dirname(tasks.__file__), "db", "manifests"),
        mock_manifest.value,
    )
    assert return_value == mocked_vendor_class.return_value
