"""Test the file_system_move module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import file_system_move
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestFileSystemMove(GenericTaskModuleTest):
  """Test the file_system_move module."""

  expected_api_enabled = False
  expected_arg_class = file_system_move.Args
  expected_return_type = None
  expected_type = enums.TaskType.FILE_SYSTEM_MOVE
  mock_args = file_system_move.Args(
      source="/mock1/path1",
      destination="/mock2/path2",
  )
  module = file_system_move
