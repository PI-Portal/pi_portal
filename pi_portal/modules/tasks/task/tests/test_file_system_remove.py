"""Test the file_system_remove module."""

import os

import pytest
from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import file_system_remove
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestFileSystemRemove(GenericTaskModuleTest):
  """Test the file_system_remove module."""

  expected_api_enabled = False
  expected_arg_class = file_system_remove.Args
  expected_return_type = None
  expected_routing_label = enums.RoutingLabel.FILE_SYSTEM
  expected_type = enums.TaskType.FILE_SYSTEM_REMOVE
  mock_args = file_system_remove.Args(
      path=os.path.join(config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD, "file1")
  )
  module = file_system_remove

  def test_import__args_class__inheritance(self) -> None:
    assert issubclass(
        file_system_remove.Args,
        ArgFileSystemRestrictionMixin,
    )

  def test_import__args_class__whitelist(self) -> None:
    assert file_system_remove.Args.file_system_arg_restrictions == {
        "path":
            [
                config.PATH_CAMERA_CONTENT,
                config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD,
                config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
            ]
    }

  def test_import__args_class__initialize_with_invalid_args(self) -> None:
    with pytest.raises(ValueError):
      file_system_remove.Args(path="invalid_path")
