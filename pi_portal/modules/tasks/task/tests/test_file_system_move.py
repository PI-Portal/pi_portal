"""Test the file_system_move module."""

import os

import pytest
from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import file_system_move
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestFileSystemMove(GenericTaskModuleTest):
  """Test the file_system_move module."""

  expected_api_enabled = False
  expected_arg_class = file_system_move.Args
  expected_return_type = None
  expected_routing_label = enums.RoutingLabel.FILE_SYSTEM
  expected_type = enums.TaskType.FILE_SYSTEM_MOVE
  mock_args = file_system_move.Args(
      source=os.path.join(config.PATH_CAMERA_CONTENT, "file1"),
      destination=os.path.join(config.PATH_QUEUE_VIDEO_UPLOAD, "file1"),
  )
  module = file_system_move

  def test_import__args_class__inheritance(self) -> None:
    assert issubclass(
        file_system_move.Args,
        ArgFileSystemRestrictionMixin,
    )

  def test_import__args_class__whitelist(self) -> None:
    assert file_system_move.Args.file_system_arg_restrictions == {
        "source": [config.PATH_CAMERA_CONTENT],
        "destination":
            [
                config.PATH_QUEUE_LOG_UPLOAD,
                config.PATH_QUEUE_VIDEO_UPLOAD,
            ]
    }

  def test_import__args_class__initialize_with_invalid_args(self) -> None:
    with pytest.raises(ValueError):
      file_system_move.Args(source="invalid_path1", destination="invalid_path2")
