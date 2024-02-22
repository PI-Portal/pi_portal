"""Test the file_system_copy module."""

import os

import pytest
from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import file_system_copy
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestFileSystemCopy(GenericTaskModuleTest):
  """Test the file_system_copy module."""

  expected_api_enabled = True
  expected_arg_class = file_system_copy.Args
  expected_return_type = None
  expected_type = enums.TaskType.FILE_SYSTEM_COPY
  mock_args = file_system_copy.Args(
      source=os.path.join(config.LOG_FILE_BASE_FOLDER, "file1"),
      destination=os.path.join(config.PATH_QUEUE_LOG_UPLOAD, "file1"),
  )
  module = file_system_copy

  def test_import__args_class__inheritance(self) -> None:
    assert issubclass(
        file_system_copy.Args,
        ArgFileSystemRestrictionMixin,
    )

  def test_import__args_class__whitelist(self) -> None:
    assert file_system_copy.Args.file_system_arg_restrictions == {
        "source": [config.LOG_FILE_BASE_FOLDER],
        "destination": [config.PATH_QUEUE_LOG_UPLOAD,]
    }

  def test_import__args_class__initialize_with_invalid_args(self) -> None:
    with pytest.raises(ValueError):
      file_system_copy.Args(source="invalid_path1", destination="invalid_path2")
