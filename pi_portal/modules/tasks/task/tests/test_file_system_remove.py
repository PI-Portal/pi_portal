"""Test the file_system_remove module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import file_system_remove
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestFileSystemRemove(GenericTaskModuleTest):
  """Test the file_system_remove module."""

  expected_api_enabled = False
  expected_arg_class = file_system_remove.Args
  expected_return_type = None
  expected_type = enums.TaskType.FILE_SYSTEM_REMOVE
  mock_args = file_system_remove.Args(path="/mock/path")
  module = file_system_remove
